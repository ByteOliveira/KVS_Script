import configparser
import os
from os.path import isfile, join, isdir
import subprocess
from property_dic import Property_dic as prodic
from property_dic import ppd as pp
import sys
import plotly.graph_objs as go
import plotly
import math
import plotly.plotly as py


def myround(n):
    if n == 0:
        return 0
    sgn = -1 if n < 0 else 1
    scale = int(-math.floor(math.log10(abs(n))))
    if scale <= 0:
        scale = 1
    factor = 10**scale
    return sgn*math.floor(abs(n)*factor)/factor

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

conf_counts = [2,4]
ntt="1PnC"

property_dic_nPC = {"Tomp2p": prodic().sub_property_dict_churn,"Redis": prodic().sub_property_dicr_churn,"Tomp2p with Churn": prodic().sub_property_dict_churn}
property_dic_1PnC = {"Tomp2p": prodic().sub_property_dict_churn,"Redis": prodic().sub_property_dicr_churn,"Tomp2p with Churn": prodic().sub_property_dict_churn}
property_dic_nP1C = {"Tomp2p": prodic().sub_property_dict_churn,"Redis": prodic().sub_property_dicr_churn,"Tomp2p with Churn": prodic().sub_property_dict_churn}

property_dic = {"nPC": pp().property_dic_nPC, "1PnC": pp().property_dic_1PnC, "nP1C":pp().property_dic_nP1C}

cwd = os.getcwd()
days = [f for f in os.listdir(cwd+"/benchmarks") if isdir(join(cwd+"/benchmarks", f))]
bench_dirs = []
for d in days:
    bench_dirs += [cwd+"/benchmarks/"+d+"/"+f for f in os.listdir(cwd+"/benchmarks/"+d) if isdir(join(cwd+"/benchmarks/"+d, f))]

print(bench_dirs)

property_dic_devices = {2:{} , 4:{}}
for conf_count in conf_counts:
    property_dic = {"nPC": pp().property_dic_nPC, "1PnC": pp().property_dic_1PnC, "nP1C":pp().property_dic_nP1C}
    for b in bench_dirs:
        conf_files = [b + "/" + f for f in os.listdir(b) if isfile(join(b, f)) and f.find(".conf") != -1 and f.find("type.conf") == -1]
        tf = open(b+"/type.conf")
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
                kvs = config.get("dummy_section","general.kvs")
                churn_p = config.get("dummy_section","general.churn.enable")

                if churn_p == "True":
                    churn = "True"
                else:
                    churn = "False"

                nt = ""
                if ntl.find("1PnC")>0:
                    nt="1PnC"
                    #print("1PnC")
                elif ntl.find("nP1C")>0:
                    nt="nP1C"
                    #print("nP1C")
                else:
                    nt="nPC"
                    #print("nPC")

                if kvs.find("redis") > 0:
                    kvs = "Redis"
                else:
                    kvs = "Tomp2p"

                if kvs == "Tomp2p" and churn == "True":
                    kvs = "Tomp2p with Churn"

                rp = subprocess.check_output(['tail', '-6', b + "/report.txt"])
                rp = rp.decode("ascii")
                rp = rp.split("\n")
                rp = rp[:-1]
                # print("Redis "+str(property_dic["Redis"]))
                # print("Tomp2p "+str(property_dic["Tomp2p"]))
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
                    property_dic[nt][kvs][key_p][rate].append({"count": count, "avg": avg, "stddev": stddev, "min": min1, "max": max1})

    property_dic_devices[conf_count] = property_dic

all_pk = ["latency", "time lag", "version lag"]
all_pt = ["count", "avg", "stddev", "min", "max"]

result1 = {}

for k in all_pk:
    print("" + k)
    for t in ["Redis", "Tomp2p", "Tomp2p with Churn"]:
        data = []
        data1 = []
        print("" + t)
        for d in [2, 4]:
            yd = []
            ymax = []
            ymin = []
            yper = []
            yerrmax = []
            yerrmin = []
            print("     devices: " + str(d))
            for r in [10, 100, 1000]:
                print("         rate: " + str(r))
                for n in ["nPC", "1PnC", "nP1C"]:
                    print("             "+n)


                    sd = [float(c["avg"]) for c in property_dic_devices[d][n][t][k][r]]
                    sd3 = [float(c["stddev"]) for c in property_dic_devices[d][n][t][k][r]]
                    sd1 = [float(c["max"]) for c in property_dic_devices[d][n][t][k][r]]
                    yd.append(sum(sd) / len(sd))
                    print("                 avg: " + str(sum(sd) / len(sd)))
                    print("                 stddev: " + str(max(sd3)))
                    print("                 max: " + str(max(sd1)))
                    ymax.append(max(sd1))
                    yerrmax.append(abs(max(sd3)))
                    yerrmin.append(abs(min(sd3)))
            data += [
                go.Bar(
                    x=["10", "100", "1000"],
                    y=list(yd),
                    text=list([myround(x) for x in yd]),
                    textposition='auto',
                    error_y=dict(
                        type="data",
                        array=yerrmax,
                        arrayminus=yerrmin
                    ),
                    name=str(d)
                ),
                go.Scatter(
                    x=["10", "100", "1000"],
                    y=ymax,
                    text=list([myround(x) for x in ymax]),
                    textposition='top',
                    mode="markers+lines+text",
                    name=str(d) + " max"
                )
            ]

        if k == "latency":
            layout = go.Layout(
                title="Latency" + " with "+str(t),  # all "layout" attributes: /python/reference/#layout
                xaxis=dict(  # all "layout's" "xaxis" attributes: /python/reference/#layout-xaxis
                    type="category",  # more about "layout's" "xaxis's" "title": /python/reference/#layout-xaxis-title
                    title = "Rate in ms"
                ),
                barmode='group',
                yaxis=dict(
                    title=chr(916)+" ms"
                ),
                legend = dict(
                    tracegroupgap = 35,
                    y=0.5
                )
            )
        elif k== "time lag":
            layout = go.Layout(
                title="Time lag ("+chr(916)+"-atomicity)" + " with " + str(t),  # all "layout" attributes: /python/reference/#layout
                xaxis=dict(  # all "layout's" "xaxis" attributes: /python/reference/#layout-xaxis
                    type="category",  # more about "layout's" "xaxis's" "title": /python/reference/#layout-xaxis-title
                    title="Rate in ms"
                ),
                barmode='group',
                yaxis=dict(
                    title=chr(916) + " ms"
                ),
                legend = dict(
                    tracegroupgap = 35,
                    y=0.5
                )
            )
        else:
            layout = go.Layout(
                title="Version Lag (k-atomicity)" + " with " + str(t),
                # all "layout" attributes: /python/reference/#layout
                xaxis=dict(  # all "layout's" "xaxis" attributes: /python/reference/#layout-xaxis
                    type="category",  # more about "layout's" "xaxis's" "title": /python/reference/#layout-xaxis-title
                    title="Rate in ms"
                ),
                barmode='group',
                yaxis=dict(
                    title=chr(916) + " versions"
                ),
                legend = dict(
                    tracegroupgap = 35,
                    y=0.5
                )
            )

        plotly.tools.set_credentials_file(username='jaroaro', api_key='aTsxDQbnrWO7mR4pHWBa')

        figure = go.Figure(data=data, layout=layout)
        py.plot(figure, filename=k+str(t), image='png')
