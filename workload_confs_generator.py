from fnmatch import fnmatch
import os
import itertools
##### (1)P/(N-1)C #####
import random
secure_random = random.SystemRandom()

"""
    Generate conf lines where the consumer rate is fixed to 10milisec and the producer changes
"""


def get_confs():
    c_dir = "./configuration/"
    confs = []
    for path, subdirs, files in os.walk(c_dir):
        if not list(subdirs):
            xx = [os.path.join(path, x) for x in files]
            xx = " ".join(xx)
            confs.append(xx)
    return confs

c = get_confs()
c = "\n".join(c)
print(c)
