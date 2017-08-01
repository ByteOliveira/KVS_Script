from fnmatch import fnmatch
import os
import itertools
##### (1)P/(N-1)C #####
import random
secure_random = random.SystemRandom()

"""
    Generate conf lines where the consumer rate is fixed to 10milisec and the producer changes
"""


def get_consumer_confs_c(r, c):
    confs_consumers_dir = "./configuration/1PnC/consumer"

    _confs_consumers_redis = []
    _confs_consumers_tomp2p = []

    for path, subdirs, files in os.walk(confs_consumers_dir):
        for name in files:
            if fnmatch(name, "*rate_"+str(r)+"_*") and fnmatch(name, "*churn_False*"):
                if path.find("Redis") > 0:
                    _confs_consumers_redis.append(os.path.join(path, name))
                else:
                    _confs_consumers_tomp2p.append(os.path.join(path, name))
    return _confs_consumers_redis, _confs_consumers_tomp2p

def get_consumer_confs(r):
    confs_consumers_dir = "./configuration/1PnC/consumer"

    _confs_consumers_redis = []
    _confs_consumers_tomp2p = []

    for path, subdirs, files in os.walk(confs_consumers_dir):
        for name in files:
            if fnmatch(name, "*rate_"+str(r)+"_*"):
                if path.find("Redis") > 0:
                    _confs_consumers_redis.append(os.path.join(path, name))
                else:
                    _confs_consumers_tomp2p.append(os.path.join(path, name))
    return _confs_consumers_redis, _confs_consumers_tomp2p


def get_producer_confs_c():
    confs_producer_dir = "./configuration/1PnC/producer"

    _confs_producer_redis = []
    _confs_producer_tomp2p = []

    for path, subdirs, files in os.walk(confs_producer_dir):
        for name in files:
            if fnmatch(name, "*churn_False*"):
                if path.find("Redis") > 0:
                    _confs_producer_redis.append(os.path.join(path, name))
                else:
                    _confs_producer_tomp2p.append(os.path.join(path, name))
    return _confs_producer_redis, _confs_producer_tomp2p

def get_producer_confs():
    confs_producer_dir = "./configuration/1PnC/producer"

    _confs_producer_redis = []
    _confs_producer_tomp2p = []

    for path, subdirs, files in os.walk(confs_producer_dir):
        for name in files:
            if path.find("Redis") > 0:
                _confs_producer_redis.append(os.path.join(path, name))
            else:
                _confs_producer_tomp2p.append(os.path.join(path, name))
    return _confs_producer_redis, _confs_producer_tomp2p

prod = get_producer_confs_c()
cons = get_consumer_confs_c(10, False)
max_clients = [1, 3, 7]

## redis
prod_redis = prod[0]
cons_redis = cons[0]

for i in max_clients:

    confs = [prod_redis]
    for k in range(i):
        confs.append(cons_redis)
    ## print(confs)
    tomp2p_t = (list(itertools.product(*confs)))

    if not os.path.exists("./workloads/redis/1PnC"):
        os.makedirs("./workloads/redis/1PnC")

    file = open("./workloads/redis/1PnC/1P"+str(i)+"C", "w")

    confs1 = []

    for k in tomp2p_t:
        bench = k
        if bench not in confs1:
            s = ' '.join(map(str, bench))
            confs1.append(s)
        else:
            k -= 1
    file.write("\n".join(confs1))

## tomp2p
prod_tomp2p = prod[1]
cons_tomp2p = cons[1]
confs = [prod_tomp2p]
for i in max_clients:

    confs = [prod_tomp2p]
    for k in range(i):
        confs.append(cons_tomp2p)

    tomp2p_t = (list(itertools.product(*confs)))
    if not os.path.exists("./workloads/tomp2p/1PnC"):
        os.makedirs("./workloads/tomp2p/1PnC")

    file = open("./workloads/tomp2p/1PnC/1P"+str(i)+"C", "w")

    confs1 = []

    for k in tomp2p_t:
        s = ' '.join(map(str, k))
        file.write(s+"\n")


##### (N-1)P/(1)C #####

"""
    Generate conf lines where the consumer rate is fixed to 10milisec and the producer changes
"""


def get_consumer_confs(r):
    confs_consumers_dir = "./configuration/nP1C/consumer"

    _confs_consumers_redis = []
    _confs_consumers_tomp2p = []

    for path, subdirs, files in os.walk(confs_consumers_dir):
        for name in files:
            if fnmatch(name, "*rate_"+str(r)+"_*"):
                if path.find("Redis") > 0:
                    _confs_consumers_redis.append(os.path.join(path, name))
                else:
                    _confs_consumers_tomp2p.append(os.path.join(path, name))
    return _confs_consumers_redis, _confs_consumers_tomp2p


def get_producer_confs():
    confs_producer_dir = "./configuration/nP1C/producer"

    _confs_producer_redis = []
    _confs_producer_tomp2p = []

    for path, subdirs, files in os.walk(confs_producer_dir):
        for name in files:
            if path.find("Redis") > 0:
                _confs_producer_redis.append(os.path.join(path, name))
            else:
                _confs_producer_tomp2p.append(os.path.join(path, name))
    return _confs_producer_redis, _confs_producer_tomp2p

def get_consumer_confs_c(r):
    confs_consumers_dir = "./configuration/nP1C/consumer"

    _confs_consumers_redis = []
    _confs_consumers_tomp2p = []

    for path, subdirs, files in os.walk(confs_consumers_dir):
        for name in files:
            if fnmatch(name, "*churn_False*"):
                if fnmatch(name, "*rate_"+str(r)+"_*"):
                    if path.find("Redis") > 0:
                        _confs_consumers_redis.append(os.path.join(path, name))
                    else:
                        _confs_consumers_tomp2p.append(os.path.join(path, name))
    return _confs_consumers_redis, _confs_consumers_tomp2p


def get_producer_confs_c():
    confs_producer_dir = "./configuration/nP1C/producer"

    _confs_producer_redis = []
    _confs_producer_tomp2p = []

    for path, subdirs, files in os.walk(confs_producer_dir):
        for name in files:
            if fnmatch(name, "*churn_False*"):
                if path.find("Redis") > 0:
                    _confs_producer_redis.append(os.path.join(path, name))
                else:
                    _confs_producer_tomp2p.append(os.path.join(path, name))
    return _confs_producer_redis, _confs_producer_tomp2p

prod = get_producer_confs_c()
cons = get_consumer_confs_c(10)

## redis
prod_redis = prod[0]
cons_redis = cons[0]

print()
for i in max_clients:
    print(i)
    # # print(cons_redis)
    cr = [x for x in cons_redis if x.find("keysCount_"+str(i)) >= 0]
    confs = [cr]
    pr = [x for x in prod_redis if int(x[-6]) <= i-1]
    prl = list(itertools.combinations(pr,i))
    prl = [" ".join(x) for x in prl]
    confs.append(prl)
    tomp2p_t = (list(itertools.product(*confs)))

    if not os.path.exists("./workloads/redis/nP1C"):
        os.makedirs("./workloads/redis/nP1C")

    file = open("./workloads/redis/nP1C/"+str(i)+"P1C", "w")

    lines = []
    confs1 = []
    print(len(tomp2p_t))
    for rt in tomp2p_t:
        # print("--------------------------")
        #print(rt)
        st = set(rt)
        #print(st)
        # print("--------------------------")
        if len(st) == len(rt):
            #print(len(rt))
            keys=[]
            for j in range(1, len(rt)):
                keys.append(rt[j][-6])
            #print(keys)
            if len(set(keys)) == len(rt)-1:
                s = ' '.join(map(str, rt))
                # file.write(s+"\n")
                lines.append(s)

    print(len(lines))
    file.write("\n".join(lines))


print("tomp2p")
## tomp2p
prod_tomp2p = prod[1]
cons_tomp2p = cons[1]
for i in max_clients:
    print(i)
    # # print(cons_redis)
    cr = [x for x in cons_tomp2p if x.find("keysCount_" + str(i)) >= 0]
    confs = [cr]
    pr = [x for x in prod_tomp2p if int(x[-6]) <= i - 1]
    print(len(pr))
    prl = list(itertools.combinations(pr, i))
    prl = [" ".join(x) for x in prl]
    confs.append(prl)
    tomp2p_t = (list(itertools.product(*confs)))

    if not os.path.exists("./workloads/tomp2p/nP1C"):
        os.makedirs("./workloads/tomp2p/nP1C")

    file = open("./workloads/tomp2p/nP1C/"+str(i)+"P1C", "w")

    lines = []
    confs1 = []

    print(len(tomp2p_t))
    for rt in tomp2p_t:
        # print("--------------------------")
        # print(rt)
        st = set(rt)
        # print(st)
        # print("--------------------------")
        if len(st) == len(rt):
            # print(len(rt))
            keys = []
            for j in range(1, len(rt)):
                keys.append(rt[j][-6])
            # print(keys)
            if len(set(keys)) == len(rt) - 1:
                s = ' '.join(map(str, rt))
                # file.write(s+"\n")
                lines.append(s)

    print(len(lines))
    file.write("\n".join(lines))



#############
############
##################

def get_consumer_confs_c(r, c):
    confs_consumers_dir = "./configuration/1PnC/consumer"

    _confs_consumers_redis = []
    _confs_consumers_tomp2p = []

    for path, subdirs, files in os.walk(confs_consumers_dir):
        for name in files:
            if fnmatch(name, "*rate_"+str(r)+"_*") and fnmatch(name, "*churn_True*"):
                if path.find("Redis") > 0:
                    _confs_consumers_redis.append(os.path.join(path, name))
                else:
                    _confs_consumers_tomp2p.append(os.path.join(path, name))
    return _confs_consumers_redis, _confs_consumers_tomp2p

def get_producer_confs_c():
    confs_producer_dir = "./configuration/1PnC/producer"

    _confs_producer_redis = []
    _confs_producer_tomp2p = []

    for path, subdirs, files in os.walk(confs_producer_dir):
        for name in files:
            if fnmatch(name, "*churn_True*"):
                if path.find("Redis") > 0:
                    _confs_producer_redis.append(os.path.join(path, name))
                else:
                    _confs_producer_tomp2p.append(os.path.join(path, name))
    return _confs_producer_redis, _confs_producer_tomp2p


prod = get_producer_confs_c()
cons = get_consumer_confs_c(10, False)
max_clients = [1, 3, 7]

## redis
prod_redis = prod[0]
cons_redis = cons[0]

for i in max_clients:

    confs = [prod_redis]
    for k in range(i):
        confs.append(cons_redis)
    ## print(confs)
    tomp2p_t = (list(itertools.product(*confs)))

    if not os.path.exists("./workloads/redis/1PnC"):
        os.makedirs("./workloads/redis/1PnC")

    file = open("./workloads/redis/1PnC/1P"+str(i)+"C-Churn", "w")

    confs1 = []

    for k in tomp2p_t:
        bench = k
        if bench not in confs1:
            s = ' '.join(map(str, bench))
            confs1.append(s)
        else:
            k -= 1
    file.write("\n".join(confs1))

## tomp2p
prod_tomp2p = prod[1]
cons_tomp2p = cons[1]
confs = [prod_tomp2p]
for i in max_clients:

    confs = [prod_tomp2p]
    for k in range(i):
        confs.append(cons_tomp2p)

    tomp2p_t = (list(itertools.product(*confs)))
    if not os.path.exists("./workloads/tomp2p/1PnC"):
        os.makedirs("./workloads/tomp2p/1PnC")

    file = open("./workloads/tomp2p/1PnC/1P"+str(i)+"C-Churn", "w")

    confs1 = []

    for k in tomp2p_t:
        s = ' '.join(map(str, k))
        file.write(s+"\n")


##### (N-1)P/(1)C #####

"""
    Generate conf lines where the consumer rate is fixed to 10milisec and the producer changes
"""


def get_consumer_confs_c(r):
    confs_consumers_dir = "./configuration/nP1C/consumer"

    _confs_consumers_redis = []
    _confs_consumers_tomp2p = []

    for path, subdirs, files in os.walk(confs_consumers_dir):
        for name in files:
            if fnmatch(name, "*churn_True*"):
                if fnmatch(name, "*rate_"+str(r)+"_*"):
                    if path.find("Redis") > 0:
                        _confs_consumers_redis.append(os.path.join(path, name))
                    else:
                        _confs_consumers_tomp2p.append(os.path.join(path, name))
    return _confs_consumers_redis, _confs_consumers_tomp2p


def get_producer_confs_c():
    confs_producer_dir = "./configuration/nP1C/producer"

    _confs_producer_redis = []
    _confs_producer_tomp2p = []

    for path, subdirs, files in os.walk(confs_producer_dir):
        for name in files:
            if fnmatch(name, "*churn_True*"):
                if path.find("Redis") > 0:
                    _confs_producer_redis.append(os.path.join(path, name))
                else:
                    _confs_producer_tomp2p.append(os.path.join(path, name))
    return _confs_producer_redis, _confs_producer_tomp2p

prod = get_producer_confs_c()
cons = get_consumer_confs_c(10)

## redis
prod_redis = prod[0]
cons_redis = cons[0]

print()
for i in max_clients:
    print(i)
    # # print(cons_redis)
    cr = [x for x in cons_redis if x.find("keysCount_"+str(i)) >= 0]
    confs = [cr]
    pr = [x for x in prod_redis if int(x[-6]) <= i-1]
    prl = list(itertools.combinations(pr,i))
    prl = [" ".join(x) for x in prl]
    confs.append(prl)
    tomp2p_t = (list(itertools.product(*confs)))

    if not os.path.exists("./workloads/redis/nP1C"):
        os.makedirs("./workloads/redis/nP1C")

    file = open("./workloads/redis/nP1C/"+str(i)+"P1C-Churn", "w")

    lines = []
    confs1 = []
    print(len(tomp2p_t))
    for rt in tomp2p_t:
        # print("--------------------------")
        #print(rt)
        st = set(rt)
        #print(st)
        # print("--------------------------")
        if len(st) == len(rt):
            #print(len(rt))
            keys=[]
            for j in range(1, len(rt)):
                keys.append(rt[j][-6])
            #print(keys)
            if len(set(keys)) == len(rt)-1:
                s = ' '.join(map(str, rt))
                # file.write(s+"\n")
                lines.append(s)

    print(len(lines))
    file.write("\n".join(lines))


print("tomp2p")
## tomp2p
prod_tomp2p = prod[1]
cons_tomp2p = cons[1]
for i in max_clients:
    print(i)
    # # print(cons_redis)
    cr = [x for x in cons_tomp2p if x.find("keysCount_" + str(i)) >= 0]
    confs = [cr]
    pr = [x for x in prod_tomp2p if int(x[-6]) <= i - 1]
    print(len(pr))
    prl = list(itertools.combinations(pr, i))
    prl = [" ".join(x) for x in prl]
    confs.append(prl)
    tomp2p_t = (list(itertools.product(*confs)))

    if not os.path.exists("./workloads/tomp2p/nP1C"):
        os.makedirs("./workloads/tomp2p/nP1C")

    file = open("./workloads/tomp2p/nP1C/"+str(i)+"P1C-Churn", "w")

    lines = []
    confs1 = []

    print(len(tomp2p_t))
    for rt in tomp2p_t:
        # print("--------------------------")
        # print(rt)
        st = set(rt)
        # print(st)
        # print("--------------------------")
        if len(st) == len(rt):
            # print(len(rt))
            keys = []
            for j in range(1, len(rt)):
                keys.append(rt[j][-6])
            # print(keys)
            if len(set(keys)) == len(rt) - 1:
                s = ' '.join(map(str, rt))
                # file.write(s+"\n")
                lines.append(s)

    print(len(lines))
    file.write("\n".join(lines))
