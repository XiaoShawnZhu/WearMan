import sys
import numpy as np
from matplotlib import pyplot as plt

from helper.metrics.thrpt import *

pcap_fname = "wear.pcap"
svr_ip = "141.212.110.129"
svr_port = "4000"
outfile = open("thrpt.txt", 'w')

def thrpt_plot(thrpt):
    x = thrpt[0]
    # x[:] = [m - thrpt[0][0] for m in x]
    y = thrpt[1]
    plt.xlabel("Time (s)")
    plt.ylabel("Throughput(kbps)")
    plt.plot(x, y)
    plt.show()

def thrpt_save(thrpt, outfile):
    x = thrpt[0]
    y = thrpt[1]
    i = 0
    while i < len(x):
        outfile.write(str(x[i])+'\t'+str(y[i])+'\n')
        i += 1

def thrpt_analyze(thrpt):
    cnt = 0
    for item in thrpt[1]:
        # print(item)
        if item == 0:
            cnt += 1
    print("No transmission time accounts for: ", int(100*cnt/len(thrpt[1])), "%")

thrpt = get_thrpt_kbps_from_pcap(pcap_fname, svr_ip, svr_port, 200)
thrpt_plot(thrpt)
thrpt_analyze(thrpt)
thrpt_save(thrpt, outfile)