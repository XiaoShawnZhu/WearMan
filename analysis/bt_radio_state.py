import sys
from matplotlib import pyplot as plt
from helper.metrics.state import *

infname = 'btsnoop_hci.log'

def state_plot(state):
	x = []
	y = []
	for key in sorted(state):
		x.append(key/1000.0)
		y.append(state[key])
	plt.xlabel("Time (s)")
	plt.ylabel("State")
	plt.step(x, y)
	plt.show()

state = get_radio_state_from_snoop(infname)
state_plot(state)