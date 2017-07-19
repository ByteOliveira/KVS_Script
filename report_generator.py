import os
import configparser
import subprocess
from prettytable import PrettyTable
import sys
from os.path import isdir , join, isfile


def calc_avg(rates_dic, rates_dic_it, wk, rk):
    return float("{0:.2f}".format(rates_dic[wk][rk]/rates_dic_it[wk][rk]))


def do_table(pk, pkt, keys, property_dic):

    print(pk.upper()+" "+pkt.upper()+" (avg for all tests)")

    read_keys = []
    write_keys = []
    for key in keys:
        read_keys.append(key.split("/")[1].replace("(", "").replace(")", ""))
        write_keys.append(key.split("/")[0].replace("(", "").replace(")", ""))

    read_keys = list(sorted(set(read_keys)))
    write_keys = list(sorted(set(write_keys)))

    table = PrettyTable(["WR/RR"]+read_keys)

    rates_dic = {}
    rates_dic_it = {}

    for v in property_dic[pk]:
        if v[0] not in rates_dic:
            rates_dic[v[0]] = {}
            rates_dic_it[v[0]] = {}
        if v[1] not in rates_dic[v[0]]:
            rates_dic[v[0]][v[1]] = float(v[2][pkt])
            rates_dic_it[v[0]][v[1]] = 0
        else:
            rates_dic[v[0]][v[1]] += float(v[2][pkt])
        rates_dic_it[v[0]][v[1]] += 1

    for wk in write_keys:
        row = [wk]
        for rk in read_keys:
            if rk in rates_dic[wk]:
                row.append(calc_avg(rates_dic, rates_dic_it, wk, rk))
            else:
                row.append(None)
        table.add_row(row)

    print(table)


cwd = os.getcwd()
days = [f for f in os.listdir(cwd+"/benchmarks") if isdir(join(cwd+"/benchmarks", f))]
bench_dirs = []
for d in days:
    bench_dirs += [cwd+"/benchmarks/"+d+"/"+f for f in os.listdir(cwd+"/benchmarks/"+d) if isdir(join(cwd+"/benchmarks/"+d, f))]

keys = []

conf_count = int(sys.argv[1])

property_dic = {"latency": [], "time lag": [], "version lag": [], "read errors": []}

for b in bench_dirs:
    conf_files = [b+"/"+f for f in os.listdir(b) if isfile(join(b, f)) and f.find(".conf") != -1 and f.find("type.conf") == -1]
    if len(conf_files) == conf_count:
        write_rates = []
        read_rates = []
        for c in conf_files:
            with open(c, 'r') as f:
                config_string = '[dummy_section]\n' + f.read()
            config = configparser.ConfigParser()
            config.read_string(config_string)

            rate = int(config.get("dummy_section", "workload.rate"))
            ratio = int(config.get("dummy_section", "workload.readRatio"))

            if ratio == 1:
                read_rates.append(str(rate))
            else:
                write_rates.append(str(rate))
        read_rates = list(sorted(read_rates))
        write_rates = list(sorted(write_rates))
        key = "("+",".join(write_rates)+")/("+",".join(read_rates)+")"
        write_key = ",".join(write_rates)
        read_key = ",".join(read_rates)
        keys.append(key)

        rp = subprocess.check_output(['tail', '-4', b + "/report.txt"])
        rp = rp.decode("ascii")
        rp = rp.split("\n")
        rp = rp[:-1]

        for line in rp:
            vl = line.split("|")
            key_p = vl[0]
            count = vl[1].split("=")[1]
            avg = vl[2].split("=")[1]
            stddev = vl[3].split("=")[1]
            min = vl[4].split("=")[1]
            max = vl[5].split("=")[1]
            # add the rest later
            if count != '0':
                property_dic[key_p].append((write_key, read_key, {"count": count, "avg":avg, "stddev":stddev, "min":min, "max":max}))


all_pk = ["latency", "time lag", "version lag", "read errors"]
all_pt = ["count", "avg", "stddev", "min", "max"]


for pk in all_pk:
    for pt in all_pt:
        do_table(pk, pt, keys, property_dic)

