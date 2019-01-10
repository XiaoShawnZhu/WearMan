import sys
from matplotlib import pyplot as plt
from helper.filter.snoop_filter import *

infname = 'btsnoop_hci.log'

def event_plot(state):
	x = []
	y = []
	for key in sorted(state):
		x.append(key)
		y.append(state[key])
	plt.xlabel("Time (ms)")
	plt.ylabel("Packet size (bytes)")
	plt.plot(x, y, 'x')
	plt.show()
	
sniff_req = hci_cmd_sniff_timestamp(infname)
exitsniff_req = hci_cmd_exitsniff_timestamp(infname)
cmd = hci_cmd_timestamp(infname)
cmd_create = hci_cmd_create_timestamp(infname)
evt_change2active = hci_evt_change2active_timestamp(infname)
evt_change2sniff = hci_evt_change2sniff_timestamp(infname)
evt = hci_evt_timestamp(infname)
evt_number_of_comp = hci_evt_number_timestamp(infname)
evt_mode_change = hci_evt_change_timestamp(infname)
evt_cmd_status = hci_evt_status_timestamp(infname)
evt_subrating = hci_evt_subrating_timestamp(infname)

event_plot(sniff_req)
event_plot(exitsniff_req)
event_plot(cmd)
event_plot(cmd_create)
event_plot(evt_change2active)
event_plot(evt_change2sniff)
event_plot(evt)
event_plot(evt_number_of_comp)
event_plot(evt_mode_change)
event_plot(evt_cmd_status)
event_plot(evt_subrating)