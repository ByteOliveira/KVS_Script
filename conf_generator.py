
import itertools
import os

freqs = [1, 10, 100]


def freq_to_rate_per_milisec(hz):
    return int(1000/hz)

rates = [freq_to_rate_per_milisec(f) for f in freqs]

print(rates)

kvs = ["kvsca.tomp2p.TomP2P", "kvsca.redis.JedisImp"]

churn = [True, False]

clients_max = 8

producer_pos = [rates, kvs, churn]
consumer_pos = [rates, kvs, churn]

producer_confs = list(itertools.product(*producer_pos))
consumer_confs = list(itertools.product(*consumer_pos))

print(producer_confs)
print(consumer_confs)

general_conf = "general.deviceId=1\n" \
        "workload.initialKey=0\n" \
        "workload.duration=90000\n" \
        "workload.numberOfKeys=1\n" \
        "workload.readRatio=0\n"

for pc in producer_confs:
    if pc[1] == 'kvsca.tomp2p.TomP2P':
        k = "TomP2P"
    else:
        k = "Redis"

    if not os.path.exists("./configuration/1PnC/producer/"+k):
        os.makedirs("./configuration/1PnC/producer/"+k)
    if pc[2]:
        churn_state = "true"
    else:
        churn_state = "false"

    if (k == "Redis" and not pc[2]) or k == "TomP2P":
        file = open("./configuration/1PnC/producer/" + k + "/conf_rate_" + str(pc[0]) + "_churn_" + str(pc[2]) + ".conf",
                    "w")
        file.write(general_conf)
        file.write("general.churn.enable="+churn_state+'\n')
        file.write("workload.rate="+str(pc[0])+"\n")
        file.write("general.kvs="+pc[1])
        file.close()

general_conf = "general.deviceId=1\n" \
        "workload.initialKey=0\n" \
        "workload.duration=90000\n" \
        "workload.numberOfKeys=1\n" \
        "workload.readRatio=1\n"

for cc in consumer_confs:
    if cc[1] == 'kvsca.tomp2p.TomP2P':
        k = "TomP2P"
    else:
        k = "Redis"

    if not os.path.exists("./configuration/1PnC/consumer/"+k):
        os.makedirs("./configuration/1PnC/consumer/"+k)
    if cc[2]:
        churn_state = "true"
    else:
        churn_state = "false"

    if (k == "Redis" and not cc[2]) or k == "TomP2P":
        file = open(
            "./configuration/1PnC/consumer/" + k + "/conf_rate_" + str(cc[0]) + "_churn_" + str(cc[2]) + ".conf", "w")
        file.write(general_conf)
        file.write("general.churn.enable="+churn_state+'\n')
        file.write("workload.rate="+str(cc[0])+"\n")
        file.write("general.kvs="+cc[1])
        file.close()

#####################################################################################################################

keys = [0, 1, 2, 3, 4, 5, 6, 7]

keys_c = [1, 2, 3, 4, 5, 6, 7, 8]

rates = [freq_to_rate_per_milisec(f) for f in freqs]

print(rates)

kvs = ["kvsca.tomp2p.TomP2P", "kvsca.redis.JedisImp"]

churn = [True, False]

clients_max = 8

producer_pos = [rates, kvs, churn, keys]
consumer_pos = [rates, kvs, churn, keys_c]

producer_confs = list(itertools.product(*producer_pos))
consumer_confs = list(itertools.product(*consumer_pos))

print(producer_confs)
print(consumer_confs)

general_conf = "general.deviceId=1\n" \
               "workload.duration=90000\n" \
               "workload.numberOfKeys=1\n" \
               "workload.readRatio=0\n"

for pc in producer_confs:
    if pc[1] == 'kvsca.tomp2p.TomP2P':
        k = "TomP2P"
    else:
        k = "Redis"

    if not os.path.exists("./configuration/nP1C/producer/" + k):
        os.makedirs("./configuration/nP1C/producer/" + k)

    if pc[2]:
        churn_state = "true"
    else:
        churn_state = "false"

    if (k == "Redis" and not pc[2]) or k == "TomP2P":
        file = open(
            "./configuration/nP1C/producer/" + k + "/conf_rate_" + str(pc[0]) + "_churn_" + str(pc[2]) + "_key_" + str(
                pc[3]) + ".conf",
            "w")
        file.write(general_conf)
        file.write("general.churn.enable=" + churn_state + '\n')
        file.write("workload.rate=" + str(pc[0]) + "\n")
        file.write("general.kvs=" + pc[1]+"\n")
        file.write("workload.initialKey="+str(pc[3]))
        file.close()

general_conf = "general.deviceId=1\n" \
               "workload.initialKey=0\n" \
               "workload.duration=90000\n" \
               "workload.readRatio=1\n"

for cc in consumer_confs:
    if cc[1] == 'kvsca.tomp2p.TomP2P':
        k = "TomP2P"
    else:
        k = "Redis"

    if not os.path.exists("./configuration/nP1C/consumer/" + k):
        os.makedirs("./configuration/nP1C/consumer/" + k)

    if cc[2]:
        churn_state = "true"
    else:
        churn_state = "false"

    if (k == "Redis" and not cc[2]) or k == "TomP2P":
        file = open("./configuration/nP1C/consumer/" + k + "/conf_rate_" + str(cc[0]) + "_churn_" + str(cc[2])
                    + "_keysCount_" + str(cc[3]) + ".conf", "w")
        file.write(general_conf)
        file.write("general.churn.enable=" + churn_state + '\n')
        file.write("workload.rate=" + str(cc[0]) + "\n")
        file.write("general.kvs=" + cc[1]+"\n")
        file.write("workload.numberOfKeys="+str(cc[3]))
        file.close()


