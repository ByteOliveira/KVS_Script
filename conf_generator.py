import os


def freq_to_rate_per_milisec(hz):
    return int(1000/hz)

#####################################################################################################################


def gen_producer(d, deviceID, kvs, freq, churn, min_key, num_keys):
    d += kvs + "/Rate_" + str(freq) + "_hz/Churn_"+str(churn)+"/"

    r = int(freq_to_rate_per_milisec(freq))

    conf = "general.deviceId="+str(deviceID)+"\n"+ \
           "workload.initialKey="+str(min_key)+"\n"+ \
           "workload.duration=90000\n"+ \
           "workload.readRatio=0\n"\
           "workload.numberOfKeys="+str(num_keys)+"\n"\
           "general.churn.enable="+str(churn)+"\n"\
           "workload.rate=" + str(r) + "\n"\
           "general.kvs="+kvs+"\n"

    if not os.path.exists(d):
        os.makedirs(d)

    f = open(d + "d" + str(deviceID)+".conf", "w")
    print(d + "d" + str(deviceID) + ".conf")

    f.write(conf)
    f.close()


def gen_consumer(d, deviceID, kvs, freq, churn, min_key, num_keys):
    d += kvs + "/Rate_" + str(freq) + "_hz/Churn_" + str(churn) + "/"

    r = int(freq_to_rate_per_milisec(freq))

    conf = "general.deviceId=" + str(deviceID) + "\n" + \
           "workload.initialKey=" + str(min_key) + "\n" + \
           "workload.duration=90000\n" + \
           "workload.readRatio=1\n" \
           "workload.numberOfKeys=" + str(num_keys) + "\n" \
           "general.churn.enable=" + str(churn) + "\n" \
           "workload.rate=" + str(10) + "\n"\
           "general.kvs="+kvs+"\n"

    if not os.path.exists(d):
        os.makedirs(d)

    f = open(d + "d" + str(deviceID) + ".conf", "w")

    f.write(conf)
    f.close()

    if not os.path.exists(d):
        os.makedirs(d)

    print(d + "d" + str(deviceID) + ".conf")

    f = open(d + "d" + str(deviceID) + ".conf", "w")

    f.write(conf)
    f.flush()
    f.close()


def gen_consumerProducer(d, deviceID, kvs, freq, churn, min_key, num_keys,generator):
    d += kvs + "/Rate_" + str(freq) + "_hz/Churn_" + str(churn) + "/"

    conf = "general.deviceId=" + str(deviceID) + "\n" \
           "workload.initialKey=" + str(min_key) + "\n" \
           "workload.duration=90000\n" \
           "workload.readRatio=0.5\n" \
           "workload.numberOfKeys=" + str(num_keys) + "\n" \
           "general.churn.enable=" + str(churn) + "\n" \
           "workload.rate=" + str(freq_to_rate_per_milisec(freq)) + "\n"\
           "general.kvs="+kvs+"\n"\
           "general.generator="+generator+"\n"

    if not os.path.exists(d):
        os.makedirs(d)

    print(d + "d" + str(deviceID) + ".conf")

    f = open(d + "d" + str(deviceID) + ".conf", "w")

    f.write(conf)
    f.close()

#######################################################################################################################

freqs = [1, 10, 100]

kvs_pos = ["kvsca.tomp2p.TomP2P", "kvsca.redis.JedisImp"]

churn_pos = [True, False]

clients_max = [2, 4]

base_dir = "./configuration/"


def gen_1PnC(d, kvs, freq, churn):
    d += "1PnC/"

    if kvs == "kvsca.redis.JedisImp" and churn:
        return

    for cm in clients_max:
        d1 = d+"1P" + str(cm) + "C/"
        gen_producer(d1, 1, kvs, freq, churn, 0, 1)
        for i in range(2, cm+1):
            gen_consumer(d1, i, kvs, freq, churn, 0, 1)


def gen_nP1C(d, kvs, freq, churn):
    d += "nP1C/"

    if kvs == "kvsca.redis.JedisImp" and churn:
        return

    for cm in clients_max:
        d1 = d + str(cm)+"P1C/"
        gen_consumer(d1, 1, kvs, freq, churn, 0, cm-1)
        for i in range(2, cm + 1):
            gen_producer(d1, i, kvs, freq, churn, i-2, 1)


def gen_nPC(d, kvs, freq, churn):
    d += "nPC/"

    if kvs == "kvsca.redis.JedisImp" and churn:
        return

    generator = "kvsca.SimpleWorkload_nPC"
    for cm in clients_max:
        d1 = d + str(cm) + "PC/"
        for i in range(1, cm + 1):
            gen_consumerProducer(d1, i, kvs, freq, churn, 1, cm,generator)

for fs in freqs:
    for k in kvs_pos:
        for c in churn_pos:
            gen_1PnC(base_dir, k, fs, c)
            gen_nP1C(base_dir, k, fs, c)
            gen_nPC(base_dir, k, fs, c)

