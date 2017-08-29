import os

import subprocess

JAR_PATH = "/Users/jaro/IdeaProjects/KSV_CA/target/kvsca-1.0-SNAPSHOT.jar"

c_dir = "./benchmarks"

xx= []

analiser = ["java", "-cp", JAR_PATH,
                    "kvsca.analysis.Analysis"]


for path, subdirs, files in os.walk(c_dir):
    if not list(subdirs):
        xx = [os.path.join(path, x) for x in files if x.find(".log")>0]
        runnner = analiser + xx
        pro = subprocess.Popen(runnner, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = pro.communicate()
        pro.wait()
        f = open(path + "/" + "report.txt", "wb")
        f.write(out)
        f.close()
