from matplotlib import pyplot as plt
from helper.metrics.thrpt import *
from helper.metrics.state import *

pcap_fname = "wear.pcap"
connectivity_fname = "connectivity.log"
svr_ip = "141.212.110.129"
svr_port = "4000"
outfile = open("thrpt.txt", 'w')

def state_plot(state):
	x = []
	y = []
	for key in sorted(state):
		x.append(key/1000.0)
		y.append(state[key])
	plt.xlabel("Time (s)")
	plt.ylabel("State")
	plt.plot(x, y)
	plt.show()

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
	ax1.plot(state_x, state_y, 'b')
	ax2 = ax1.twinx()
	ax2.set_ylabel("Throughput (kbps)")
	ax2.plot(thrpt[0], thrpt[1], 'r')
	plt.show()

thrpt = get_thrpt_kbps_from_pcap(pcap_fname, svr_ip, svr_port, 200)
state = get_connectivity_state_from_log(connectivity_fname)
# state_plot(state)
correlate_plot(state, thrpt)