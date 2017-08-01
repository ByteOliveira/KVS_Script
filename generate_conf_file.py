import itertools
from fnmatch import fnmatch
import os
import random
secure_random = random.SystemRandom()

confs_consumers_dir ="/Users/jaro/IdeaProjects/KSV_CA/conf/consumers"

_confs_consumers = []

for path, subdirs, files in os.walk(confs_consumers_dir):
    for name in files:
        if fnmatch(name, "*.conf"):
            _confs_consumers.append(os.path.join(path, name))



confs_producers_dir ="/Users/jaro/IdeaProjects/KSV_CA/conf/producers"

_confs_producers = []

for path, subdirs, files in os.walk(confs_producers_dir):
    for name in files:
        if fnmatch(name, "*.conf"):
            _confs_producers.append(os.path.join(path, name))

obj = [_confs_consumers, _confs_consumers, _confs_producers]

######################################################################

li = open("./workloads/redis/nP1C/4P1C","r")
ff = []
for line in li:
    ff.append(line)


confs=[]

size = 0
if len(ff) < 100:
    size = len(ff)
else:
    size = 100

for i in range(0, 100):
    bench = ""
    #bench = secure_random.choice(ff)
    if bench not in confs:
        confs.append(bench)
    else:
        i -= 1


print("".join(confs))
