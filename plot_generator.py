import configparser
import os
from os.path import isfile, join, isdir
import subprocess
from property_dic import Property_dic as prodic
from property_dic import ppd as pp
import sys
import plotly.graph_objs as go
import plotly


def get_stats(li, pt):
    total = 0
    count = len(li)
    mmin = sys.maxsize
    maxe = 0
    for i in li:
        p = i[pt]
        total += p
        if p < mmin:
            mmin = p
        if p > maxe:
            maxe = p

    return total / count, mmin, maxe


conf_counts = [2, 4]
ntt = "1PnC"

property_dic_nPC = {"tomp2p": prodic().sub_property_dict_churn, "redis": prodic().sub_property_dicr_churn,
                    "tomp2pc": prodic().sub_property_dict_churn}
property_dic_1PnC = {"tomp2p": prodic().sub_property_dict_churn, "redis": prodic().sub_property_dicr_churn,
                     "tomp2pc": prodic().sub_property_dict_churn}
property_dic_nP1C = {"tomp2p": prodic().sub_property_dict_churn, "redis": prodic().sub_property_dicr_churn,
                     "tomp2pc": prodic().sub_property_dict_churn}

property_dic = {"nPC": pp().property_dic_nPC, "1PnC": pp().property_dic_1PnC, "nP1C": pp().property_dic_nP1C}

cwd = os.getcwd()
days = [f for f in os.listdir(cwd + "/benchmarks") if isdir(join(cwd + "/benchmarks", f))]
bench_dirs = []
for d in days:
    bench_dirs += [cwd + "/benchmarks/" + d + "/" + f for f in os.listdir(cwd + "/benchmarks/" + d) if
                   isdir(join(cwd + "/benchmarks/" + d, f))]

print(bench_dirs)

property_dic_devices = {2: {}, 4: {}}
for conf_count in conf_counts:
    property_dic = {"nPC": pp().property_dic_nPC, "1PnC": pp().property_dic_1PnC, "nP1C": pp().property_dic_nP1C}
    for b in bench_dirs:
        conf_files = [b + "/" + f for f in os.listdir(b) if
                      isfile(join(b, f)) and f.find(".conf") != -1 and f.find("type.conf") == -1]
        tf = open(b + "/type.conf")
        cl = 1
        for l in tf:
            if cl == 2:
                ntl = l
            cl += 1
        if len(conf_files) == conf_count:
            for c in conf_files:
                with open(c, 'r') as f:
                    config_string = '[dummy_section]\n' + f.read()
                config = configparser.ConfigParser()
                config.read_string(config_string)

                rate = int(config.get("dummy_section", "workload.rate"))
                ratio = float(config.get("dummy_section", "workload.readRatio"))
                kvs = config.get("dummy_section", "general.kvs")
                churn_p = config.get("dummy_section", "general.churn.enable")

                if churn_p == "True":
                    churn = "True"
                else:
                    churn = "False"

                nt = ""
                if ntl.find("1PnC") > 0:
                    nt = "1PnC"
                    # print("1PnC")
                elif ntl.find("nP1C") > 0:
                    nt = "nP1C"
                    # print("nP1C")
                else:
                    nt = "nPC"
                    # print("nPC")

                if kvs.find("redis") > 0:
                    kvs = "redis"
                else:
                    kvs = "tomp2p"

                if kvs == "tomp2p" and churn == "True":
                    kvs = "tomp2pc"

                rp = subprocess.check_output(['tail', '-6', b + "/report.txt"])
                rp = rp.decode("ascii")
                rp = rp.split("\n")
                rp = rp[:-1]
                # print("redis "+str(property_dic["redis"]))
                # print("tomp2p "+str(property_dic["tomp2p"]))
                for line in rp:

                    vl = line.split("|")
                    key_p = vl[0]
                    count = vl[1].split("=")[1]
                    avg = vl[2].split("=")[1]
                    stddev = vl[3].split("=")[1]
                    min1 = vl[4].split("=")[1]
                    max1 = vl[5].split("=")[1]

                    if rate not in property_dic[nt][kvs][key_p]:
                        property_dic[nt][kvs][key_p][rate] = []
                    property_dic[nt][kvs][key_p][rate].append(
                        {"count": count, "avg": avg, "stddev": stddev, "min": min1, "max": max1})

    property_dic_devices[conf_count] = property_dic

all_pk = ["latency", "time lag", "version lag", "read errors"]
all_pt = ["count", "avg", "stddev", "min", "max"]

result1 = {}

for d in [2, 4]:
    for k in all_pk:
        data = []
        data1 = []
        print(" " + k)
        for t in ["redis", "tomp2p", "tomp2pc"]:
            yd = []
            ymax = []
            ymin = []
            yper = []
            yerrmax = []
            yerrmin = []

            print("     " + t)
            for r in [10, 100, 1000]:
                for n in ["nPC", "1PnC", "nP1C"]:
                    print("         rate: " + str(r))
                    print("             " + k)

                    pp = sorted([float(c["avg"]) for c in property_dic_devices[d][n][t][k][r]])

                    sd = [float(c["avg"]) for c in property_dic_devices[d][n][t][k][r]]
                    sd3 = [float(c["stddev"]) for c in property_dic_devices[d][n][t][k][r]]
                    sd1 = [float(c["max"]) for c in property_dic_devices[d][n][t][k][r]]
                    sd2 = [float(c["min"]) for c in property_dic_devices[d][n][t][k][r]]
                    sd4 = [float(c["count"]) for c in property_dic_devices[d][n][t][k][r]]
                    yd.append(sum(sd) / len(sd))
                    print("                 avg: " + str(sum(sd) / len(sd)))
                    print("                 stddev: " + str(max(sd3)))
                    print("                 max: " + str(max(sd1)))
                    print("                 min: " + str(min(sd2)))
                    print("                 count: " + str(int(sum(sd4) / len(sd4))))
                    ymax.append(max(sd1))
                    ymin.append(min(sd2))
                    yerrmax.append(abs(sum(sd) / len(sd) - max(sd3)))
                    yerrmin.append(abs(min(sd3) - sum(sd) / len(sd)))

                    op_c = sum([int(x["count"]) for x in property_dic_devices[d][n][t]["read Count"][r]])

                    yper.append(sum(sd4) / op_c * 100)

            data += [
                go.Bar(
                    x=["10", "100", "1000"],
                    y=list(yd),
                    error_y=dict(
                        type="data",
                        array=yerrmax,
                        arrayminus=yerrmin
                    ),
                    name=t
                ),
                go.Scatter(
                    x=["10", "100", "1000"],
                    y=ymax,
                    mode="markers+lines",
                    name=t + " max"
                )
            ]

            data1 += [
                go.Bar(
                    x=["10", "100", "1000"],
                    y=yper,
                    name=t + " count"
                )
            ]

        layout = go.Layout(
            title=k + " for " + str(d) + " devices",  # all "layout" attributes: /python/reference/#layout
            xaxis=dict(  # all "layout's" "xaxis" attributes: /python/reference/#layout-xaxis
                type="category"  # more about "layout's" "xaxis's" "title": /python/reference/#layout-xaxis-title
            )
        )
        layout1 = go.Layout(
            title=k + " count (in % of reads done) for " + str(d) + " devices",
            # all "layout" attributes: /python/reference/#layout
            xaxis=dict(  # all "layout's" "xaxis" attributes: /python/reference/#layout-xaxis
                type="category"  # more about "layout's" "xaxis's" "title": /python/reference/#layout-xaxis-title
            )
        )

        plotly.tools.set_credentials_file(username='jaroaro', api_key='aTsxDQbnrWO7mR4pHWBa')

        figure = go.Figure(data=data, layout=layout)
        figure1 = go.Figure(data=data1, layout=layout1)
        plotly.offline.plot(figure, filename=k + str(d) + ".html")
        plotly.offline.plot(figure1, filename=k + str(d) + "_count.html")
