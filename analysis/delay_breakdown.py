import sys
from matplotlib import pyplot as plt
import numpy as np

from helper.metrics.delay import *

svr_fn = "server.pcap"
phone_recv_fn = "phone.pcap"
phone_send_fn = "logcat.txt"
wear_fn = "wear.pcap"
kernel_fn = "dmesg.txt"
svr_ip = "141.212.110.129"
svr_port = "4000"

def write_delay(send_time, dly, name):
	cnt = 0
	f = open(name, 'w')
	while cnt < len(send_time):
		f.write(str(send_time[cnt])+'\t'+str(dly[cnt])+'\n')
		cnt += 1

def plot_delay(ylabel, x, y):
	plt.ylabel(ylabel)
	plt.xlabel("Time elapsed (ms)")
	plt.plot(x, y)
	plt.show()

# OWD from server to wearable (should be the sum of the below ones)
s2w_dly = get_delay(E2E, svr_fn, wear_fn, svr_ip, svr_port, 0, 0, [])
# OWD from server to phone
s2p_dly = get_delay(SVR2PHONE, svr_fn, phone_recv_fn, svr_ip, svr_port, 0, 0, [])
# OWD spent in TCP/IP recv buffer
rcv_dly = get_delay(TCP_RCV, phone_recv_fn, kernel_fn, svr_ip, svr_port, 0, 500, [])
# OWD spent in proxy app
tx_dly = get_delay(PROXY, kernel_fn, phone_send_fn, svr_ip, svr_port, 0, 500, [3, 0, 0, 0, 113])
# OWD for BT transmission
p2w_dly = get_delay(PHONE2WEAR, phone_send_fn, wear_fn, svr_ip, svr_port, 0, 0, [3, 0, 0, 0, 113])

time_length = min(len(s2w_dly[0]), len(s2p_dly[0]), len(rcv_dly[0]), len(p2w_dly[0]), len(tx_dly[0]))
send_time = s2w_dly[2][:time_length]

plot_delay("Time from server to wear (ms)", send_time, s2w_dly[1][:time_length])
write_delay(s2w_dly[2], s2w_dly[1], "s2w.txt")

plot_delay("Time from server to phone (ms)", send_time, s2p_dly[1][:time_length])
write_delay(send_time, s2p_dly[1][:time_length], "s2p.txt")

plot_delay("Time from phone to wear (ms)", send_time, p2w_dly[1][:time_length])
write_delay(send_time, p2w_dly[1][:time_length], "p2w.txt")

plot_delay("Time spent in TCP/IP rcv (ms)", send_time, rcv_dly[1][:time_length])
write_delay(send_time, rcv_dly[1][:time_length], "rcv.txt")

plot_delay("Time spent in app buf (ms)", send_time, tx_dly[1][:time_length])
write_delay(send_time, tx_dly[1][:time_length], "app.txt")