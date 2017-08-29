import configparser
import os
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import subprocess
from os.path import isfile, join, isdir

import sys


def get_stats(li, pt):

    total = 0
    count = len(li)
    mmin= sys.maxsize
    maxe=0
    for i in li:
        p = i[pt]
        total += p
        if p < mmin:
            mmin = p
        if p > maxe:
            maxe = p

    return total/count, mmin,maxe


cwd = os.getcwd()
days = [f for f in os.listdir(cwd+"/benchmarks") if isdir(join(cwd+"/benchmarks", f))]
bench_dirs = []
for d in days:
    bench_dirs += [cwd+"/benchmarks/"+d+"/"+f for f in os.listdir(cwd+"/benchmarks/"+d) if isdir(join(cwd+"/benchmarks/"+d, f))]

keys = []

conf_count = int(4)
sub_property_dic = {"read Count":{}, "operation Count":{},"latency": {}, "time lag": {}, "version lag": {}, "read errors": {}}
sub_property_dic1 = {"read Count":{}, "operation Count":{},"latency": {}, "time lag": {}, "version lag": {}, "read errors": {}}
property_dic = {"tomp2p":sub_property_dic,"redis":sub_property_dic1}


for b in bench_dirs:
    conf_files = [b+"/"+f for f in os.listdir(b) if isfile(join(b, f)) and f.find(".conf") != -1 and f.find("type.conf") == -1]
    if len(conf_files) == conf_count:
        write_rates = []
        for c in conf_files:
            with open(c, 'r') as f:
                config_string = '[dummy_section]\n' + f.read()
            config = configparser.ConfigParser()
            config.read_string(config_string)

            rate = int(config.get("dummy_section", "workload.rate"))
            ratio = float(config.get("dummy_section", "workload.readRatio"))
            kvs = config.get("dummy_section","general.kvs")
            if ratio == 0:
                write_rates.append(str(rate))

        write_rates = list(sorted(write_rates))
        key = "("+",".join(write_rates)+")"
        write_key = ",".join(write_rates)
        keys.append(key)

        rp = subprocess.check_output(['tail', '-6', b + "/report.txt"])
        rp = rp.decode("ascii")
        rp = rp.split("\n")
        rp = rp[:-1]
        #print("redis "+str(property_dic["redis"]))
        #print("tomp2p "+str(property_dic["tomp2p"]))
        for line in rp:
            vl = line.split("|")
            key_p = vl[0]
            count = vl[1].split("=")[1]
            avg = vl[2].split("=")[1]
            stddev = vl[3].split("=")[1]
            min1 = vl[4].split("=")[1]
            max1 = vl[5].split("=")[1]
            if kvs.find("redis") < 0:
                kvs = "redis"
            else:
                kvs = "tomp2p"
            if str(write_key) not in property_dic[kvs][key_p]:
                property_dic[kvs][key_p][str(write_key)] = []
            property_dic[kvs][key_p][str(write_key)].append({"count": count, "avg":avg, "stddev":stddev, "min":min1, "max":max1})


all_pk = ["read Count", "operation Count", "latency", "time lag", "version lag", "read errors"]
all_pt = ["count", "avg", "stddev", "min", "max"]




for k in all_pk:
    data = []
    data1 = []
    print(k)
    for t in ["redis", "tomp2p"]:
        print(t)
        yd = []
        ymax = []
        ymin = []
        yper = []
        yerrmax = []
        yerrmin = []
        for r in ["10","100","1000"]:
            sd = [float(c["avg"]) for c in property_dic[t][k][r]]
            sd3 = [float(c["stddev"]) for c in property_dic[t][k][r]]
            sd1 = [float(c["max"]) for c in property_dic[t][k][r]]
            sd2 = [float(c["min"]) for c in property_dic[t][k][r]]
            sd4 = [float(c["count"]) for c in property_dic[t][k][r]]
            yd.append(sum(sd)/len(sd))
            ymax.append(max(sd1))
            ymin.append(min(sd2))
            yerrmax.append(abs(sum(sd)/len(sd)-sum(sd3)/len(sd3)))
            yerrmin.append(abs(sum(sd3)/len(sd3)-sum(sd)/len(sd)))

            op_c = sum([int(x["count"]) for x in property_dic[t]["read Count"][r]])

            yper.append(sum(sd4) / op_c * 100)
            print(k + " " + t + " " + str(yd))
            # plotly.tools.set_credentials_file(username='jaroaro', api_key='aTsxDQbnrWO7mR4pHWBa')
        print(k+" "+t+" "+str(yd))
        data += [
            go.Bar(
                x=["10","100","1000"],
                y=list(yd),
                error_y=dict(
                    type="data",
                    array=yerrmax,
                    arrayminus=yerrmin
                ),
                name=t
            ),
            go.Scatter(
                x=["10","100","1000"],
                y=ymax,
                mode="markers+lines",
                name=t+" max"
            ),
            go.Scatter(
                x=["10","100","1000"],
                y=ymin,
                mode="markers+lines",
                name=t + " min"
            ),
        ]

        data1 += [
            go.Bar(
                x=["10","100","1000"],
                y=yper,
                name=t + " count"
            )
        ]

    layout = go.Layout(
        title=k,                            # all "layout" attributes: /python/reference/#layout
        xaxis=dict(                 # all "layout's" "xaxis" attributes: /python/reference/#layout-xaxis
            type="category"            # more about "layout's" "xaxis's" "title": /python/reference/#layout-xaxis-title
        )
    )
    layout1 = go.Layout(
        title=k+" count (in % of reads done)",  # all "layout" attributes: /python/reference/#layout
        xaxis=dict(  # all "layout's" "xaxis" attributes: /python/reference/#layout-xaxis
            type="category"  # more about "layout's" "xaxis's" "title": /python/reference/#layout-xaxis-title
        )
    )

    figure = go.Figure(data=data, layout=layout)
    figure1 = go.Figure(data=data1, layout=layout1)

    plotly.offline.plot(figure, filename=k)
    plotly.offline.plot(figure1, filename=k+"_count")
