import itertools
from fnmatch import fnmatch
import os

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

obj = []
obj.append(_confs_consumers)
obj.append(_confs_consumers)
obj.append(_confs_producers)

li = list(itertools.product(*obj))
print(li)
for line in li:
    print(str(line[0])+" "+str(line[1])+" "+str(line[2]))


