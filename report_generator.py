import os
import configparser
import subprocess
from prettytable import PrettyTable
from os.path import isdir , join, isfile

def calc_avg(dic,dic_it,key):
    return float("{0:.2f}".format(dic[key]/dic_it[key]))


cwd = os.getcwd()
days = [f for f in os.listdir(cwd+"/benchmarks") if isdir(join(cwd+"/benchmarks", f))]
bench_dirs = []
for d in days:
    bench_dirs += [cwd+"/benchmarks/"+d+"/"+f for f in os.listdir(cwd+"/benchmarks/"+d) if isdir(join(cwd+"/benchmarks/"+d, f))]

write_rates = []
read_rates = []

property_dic = {"latency": [], "time lag": [], "version lag": [], "read errors": []}

for b in bench_dirs:
    conf_files = [b+"/"+f for f in os.listdir(b) if isfile(join(b, f)) and f.find(".conf") != -1 and f.find("type.conf") == -1]

    if len(conf_files) == 2:
        write_rate = 0
        read_rate = 0
        for conf in conf_files:
            with open(conf, 'r') as f:
                config_string = '[dummy_section]\n' + f.read()
            config = configparser.ConfigParser()
            config.read_string(config_string)

            rate = int(config.get("dummy_section","workload.rate"))
            ratio = int(config.get("dummy_section","workload.readRatio"))

            if ratio == 1:
                read_rate = rate
                read_rates.append(rate)
            else:
                write_rate = rate
                write_rates.append(rate)

        k = str(write_rate) + "/" + str(read_rate)

        rp = subprocess.check_output(['tail', '-4', b+"/report.txt"])
        rp = rp.decode("ascii")
        rp = rp.split("\n")
        rp = rp[:-1]
        for line in rp:
            vl = line.split("|")
            key = vl[0]
            count = vl[1].split("=")[1]
            avg = vl[2].split("=")[1]
            stddev = vl[3].split("=")[1]
            min = vl[4].split("=")[1]
            max = vl[5].split("=")[1]
            # add the rest later
            property_dic[key].append((k, {"count": count,"avg":avg,"stddev":stddev,"min":min,"max":max}))

print()
print("Read errors count (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["read errors"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = int(v[1]["count"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += int(v[1]["count"])
    rates_dic_it[v[0]]+=1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

###################### VERSION #########################

print()
print("Version lag count (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["version lag"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = int(v[1]["count"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += int(v[1]["count"])
    rates_dic_it[v[0]]+=1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

print()
print("Version lag avg lag (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["version lag"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = float(v[1]["avg"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += float(v[1]["avg"])
    rates_dic_it[v[0]] += 1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

print()
print("Version lag stddev lag (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["version lag"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = float(v[1]["stddev"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += float(v[1]["stddev"])
    rates_dic_it[v[0]] += 1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

print()
print("Version lag min lag (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["version lag"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = float(v[1]["min"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += float(v[1]["min"])
    rates_dic_it[v[0]] += 1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

print()
print("Version lag max lag (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["version lag"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = float(v[1]["max"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += float(v[1]["max"])
    rates_dic_it[v[0]] += 1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

###################### VERSION #########################


###################### TIME #########################


print()
print("time lag count (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["time lag"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = int(v[1]["count"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += int(v[1]["count"])
    rates_dic_it[v[0]]+=1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

print()
print("time lag avg lag (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["time lag"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = float(v[1]["avg"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += float(v[1]["avg"])
    rates_dic_it[v[0]] += 1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

print()
print("time lag stddev lag (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["time lag"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = float(v[1]["stddev"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += float(v[1]["stddev"])
    rates_dic_it[v[0]] += 1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

print()
print("time lag min lag (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["time lag"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = float(v[1]["min"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += float(v[1]["min"])
    rates_dic_it[v[0]] += 1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

print()
print("time lag max lag (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["time lag"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = float(v[1]["max"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += float(v[1]["max"])
    rates_dic_it[v[0]] += 1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

###################### TIME #########################

###################### LATENCY #########################



print()
print("latency count (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["latency"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = int(v[1]["count"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += int(v[1]["count"])
    rates_dic_it[v[0]]+=1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

print()
print("latency avg lag (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["latency"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = float(v[1]["avg"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += float(v[1]["avg"])
    rates_dic_it[v[0]] += 1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

print()
print("latency stddev lag (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["latency"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = float(v[1]["stddev"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += float(v[1]["stddev"])
    rates_dic_it[v[0]] += 1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

print()
print("latency min lag (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["latency"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = float(v[1]["min"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += float(v[1]["min"])
    rates_dic_it[v[0]] += 1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)

print()
print("latency max lag (avg for all tests)")
table = PrettyTable(["WR/RR"]+list(sorted(set(read_rates))))

rates_dic = {}
rates_dic_it = {}

for v in property_dic["latency"]:
    if v[0] not in rates_dic:
        rates_dic[v[0]] = float(v[1]["max"])
        rates_dic_it[v[0]] = 0
    else:
        rates_dic[v[0]] += float(v[1]["max"])
    rates_dic_it[v[0]] += 1

table.add_row(["10  ",calc_avg(rates_dic,rates_dic_it,"10/10"),calc_avg(rates_dic,rates_dic_it,"10/40"),calc_avg(rates_dic,rates_dic_it,"10/200"),calc_avg(rates_dic,rates_dic_it,"10/1000")])
table.add_row(["40  ",calc_avg(rates_dic,rates_dic_it,"40/10"),calc_avg(rates_dic,rates_dic_it,"40/40"),calc_avg(rates_dic,rates_dic_it,"40/200"),calc_avg(rates_dic,rates_dic_it,"40/1000")])
table.add_row(["200 ",calc_avg(rates_dic,rates_dic_it,"200/10"),calc_avg(rates_dic,rates_dic_it,"200/40"),calc_avg(rates_dic,rates_dic_it,"200/200"),calc_avg(rates_dic,rates_dic_it,"200/1000")])
table.add_row(["1000",calc_avg(rates_dic,rates_dic_it,"1000/10"),calc_avg(rates_dic,rates_dic_it,"1000/40"),calc_avg(rates_dic,rates_dic_it,"1000/200"),calc_avg(rates_dic,rates_dic_it,"1000/1000")])

print(table)