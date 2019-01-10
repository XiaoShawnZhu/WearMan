import sys
from matplotlib import pyplot as plt

from helper.metrics.state import *
from helper.metrics.thrpt import *

hci_name = 'btsnoop_hci.log'
pcap_fname = "wear.pcap"
svr_ip = "141.212.110.129"
svr_port = "4000"


def correlate_plot(state, thrpt):
	state_x = []
	state_y = []
	for key in sorted(state):
		state_x.append(key/1000.0)
		state_y.append(state[key])
	fig, ax1 = plt.subplots()
	ax1.set_xlabel("Time (s)")
	ax1.set_ylabel("State")
	ax1.set_yticks([0, 1])
	ax1.step(state_x, state_y, 'b')
	ax2 = ax1.twinx()
	ax2.set_ylabel("Throughput (kbps)")
	ax2.plot(thrpt[0], thrpt[1], 'r')
	plt.show()


state = get_radio_state_from_snoop(hci_name)
thrpt = get_thrpt_kbps_from_pcap(pcap_fname, svr_ip, svr_port, 200)
correlate_plot(state, thrpt)
