from adb import ADB
import subprocess
import time
import os
from os import listdir
from os.path import isdir, join
from termcolor import colored
import configparser

def update_progress(conf_count,max_conf,progress,elps_time):

    s = ""

    if progress%2 == 0:
        s = "■" * int(progress / 2) + "-" * int((50 - progress / 2))
    else:
        s = "■" * int(progress / 2) + "-" * int(((50 - progress / 2)+1))

    s1 = "■"*int(conf_count)+"-"*int(max_conf-conf_count)
    p1 = colored(" [{0}] {1:.2f}% ".format(s, progress),"blue","on_grey")
    p2 = colored(' [{0}] {1:.2f}% ({2} of {3}) '.format(s1, conf_count/max_conf*100,conf_count,max_conf),"cyan","on_grey")
    p3 = colored(" "+str(elps_time)+"s ","red","on_grey")
    print('\r{0} of {1}, delta time: {2}'.format(p1,p2,p3), end='')
    pass

FNULL = open(os.devnull, 'w')

cwd = os.getcwd()
date = time.strftime("%Y-%m-%d")
onlydirs = []
if(isdir("./"+date)):
    onlydirs = [f for f in listdir("./"+date) if isdir(join("./"+date, f))]

f = open("confs","r")
count_line=1
conf_c = sum(1 for line in f)

f = open("confs", "r")

print (colored(" BENCHMARKs STARTED","blue"),end="\n\n")

for line in f:
    print (colored(" BENCHMARK "+str(count_line)+" STARTED", "blue"),end="\n\n")

    server = ["java", "-cp" ,"/Users/jaro/IdeaProjects/KSV_CA/target/kvsca-1.0-SNAPSHOT.jar", "kvsca.net.test.TestManager"]
    line = line.replace("\n", "")
    line = line.split(" ")


    max_runtime=0

    for conf in line:
        print(colored(" "+conf,"magenta"),end="")
        with open(conf, 'r') as f:
            config_string = '[dummy_section]\n' + f.read()
        config = configparser.ConfigParser()
        config.read_string(config_string)
        temp = int(config.get("dummy_section","workload.duration"))
        if temp > max_runtime:
            max_runtime = temp

    print("",end="\n")

    server += line
    pro = subprocess.Popen(server,stdout=FNULL,stderr=FNULL)

    time.sleep(3)

    adb = ADB()

    devices = adb.devices()
    if (len(devices)==0):
        print(colored(" with no Android device","red"),end="\n\n")
    else:
        print(colored(" with "+str(len(devices))+" Android devices","magenta"),end="\n\n")
    time.sleep(1)
    if len(devices) >= 1:
        for d in devices:
            print ("wifi")
            #print (adb.call("-s "+d+" adb tcpip 5555"))
            #print (adb.call("-s "+d+"shell ip -f inet addr show wlan0 | grep inet | cut -d ' ' -f 6 | cut -d '/' -f 1"))
            print ("tcp")
            print (adb.call("-s "+d+" reverse tcp:8000 tcp:8000"))
            print ("install")
            print (adb.call("-s "+d+" install -r -t /Users/jaro/AndroidStudioProjects/TestKVS/app/build/outputs/apk/app-debug.apk"))
            print ("start")
            print (adb.call(("-s "+d+" shell am start com.example.jaro.testkvs/.MainActivity")))
            print ("begin")
            print (adb.call("-s "+d+" shell input keyevent 21"))
            print ("acabou")


    if len(devices) < len(line):
        worker = ["java", "-cp" ,"/Users/jaro/IdeaProjects/KSV_CA/target/kvsca-1.0-SNAPSHOT.jar", "kvsca.net.test.TestWorker"]
        diff = len(line)-len(devices)
        for i in range(0,diff):
            subprocess.Popen(worker,stdout=FNULL,stderr=FNULL)

    ini = time.monotonic()

    while True:
        i = time.monotonic()
        update_progress(count_line,conf_c, int((i-ini)/(max_runtime/1000)*100),int(i-ini))
        time.sleep(1)
        if i-ini >= max_runtime/1000:
            break

    while pro.poll() is None :
        i = time.monotonic()
        update_progress(count_line, conf_c, 99, int(i - ini))
        time.sleep(1)

    update_progress(count_line, conf_c, 100, int(i - ini))
    print(colored(" BENCHMARK DONE","green"),end="\n\n")

    print(colored(" ANALISE STARTED", "blue"), end="\n\n")

    onlydirs_after = []
    if isdir("./" + date):
        onlydirs_after = [f for f in listdir("./" + date) if isdir(join("./" + date, f))]

    dirs = list(set(onlydirs_after) - set(onlydirs))

    analiser = ["java", "-cp", "/Users/jaro/IdeaProjects/KSV_CA/target/kvsca-1.0-SNAPSHOT.jar",
                "kvsca.analysis.Analysis"]

    for d in dirs:
        fi = [cwd + "/" + date + "/" + d + "/" + f for f in listdir("./" + date + "/" + d) if f.find(".log") != -1]
        runnner = analiser + fi
        pro = subprocess.Popen(runnner, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = pro.communicate()
        print(str(out))
        pro.wait()
        type_file = open(cwd + "/" + date + "/" + d + "/type.conf", "w")
        type_file.write("kvs.type = redis\n")
        type_file.write("conf.array = " + ", ".join(line) + "\n")
        type_file.close()

        f = open(cwd + "/" + date + "/" + d + "/" + "report.txt", "w")
        f.write(str(out))
        f.close()

    onlydirs = onlydirs_after
    print(colored(" ANALISE DONE", "green"), end="\n\n")
    count_line += 1

print(colored(" BENCHMARKs DONE WITH A TOTAL OF "+str(count_line-1)+" BENCHMARKs","green"),end="\n\n")









