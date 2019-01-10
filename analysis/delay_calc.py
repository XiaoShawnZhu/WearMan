import sys
import numpy as np
from matplotlib import pyplot as plt
from helper.metrics.delay import *

svr_fn = "server.pcap"
wear_fn = "wear.pcap"
svr_ip = "141.212.110.129"
svr_port = "4000"

s2w_dly = get_delay(E2E, svr_fn, wear_fn, svr_ip, svr_port, 0, 0, [])
plt.ylabel("Time from server to wear (ms)")
plt.xlabel("Time sent (ms)")
plt.plot(s2w_dly[2], s2w_dly[1])
plt.show()