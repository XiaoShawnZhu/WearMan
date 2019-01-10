from helper.filter.snoop_filter import *
import numpy as np

SNIFF_MODE = 0
ACTIVE_MODE = 1

NO_NETWORK = 0
BT_AVAILABLE = 1
BT_CONNECTED = 2
WIFI_AVAILABLE = 3
WIFI_CONNECTED = 4
WIFI_A_BT_A = 5
WIFI_A_BT_C = 6
WIFI_C_BT_A = 7
WIFI_C_BT_C = 8

def get_radio_state_from_snoop(fname):
    state = {}
    initial_state = SNIFF_MODE
    evt_change2active = hci_evt_change2active_timestamp(fname)
    evt_change2sniff = hci_evt_change2sniff_timestamp(fname)
    for key in evt_change2active:
        state[key] = SNIFF_MODE # state previous to change
    for key in evt_change2sniff:
        state[key] = ACTIVE_MODE
    return state

def get_connectivity_state_from_log(fname):
    state = {}
    f = open(fname, 'r')
    line = f.readline()
    while line:
	    if len(line.split()) == 1:
	    	# no network
	    	ts_ms = int(line.split()[0])
	    	state[ts_ms] = NO_NETWORK
	    elif len(line.split()) == 7:
	    	# one network
	    	ts_ms = int(line.split()[0])
	    	if line.split()[2] == "COMPANION_PROXY":
	    		if line.split()[5] == "true":
	    			state[ts_ms] = BT_CONNECTED
	    		else:
	    			state[ts_ms] = BT_AVAILABLE
	    	elif line.split()[2] == "WIFI":
	    		if line.split()[5] == "true":
	    			state[ts_ms] = WIFI_CONNECTED
	    		else:
	    			state[ts_ms] = WIFI_AVAILABLE
	    elif len(line.split()) == 13:
	    	# two networks
	    	ts_ms = int(line.split()[0])
	    	if line.split()[2] == "WIFI":
	    		if line.split()[5] == "true" and line.split()[11] == "true":
	    			state[ts_ms] = WIFI_C_BT_C
	    		elif line.split()[5] == "true" and line.split()[11] == "false":
	    			state[ts_ms] = WIFI_C_BT_A
	    		elif line.split()[5] == "false" and line.split()[11] == "false":
	    			state[ts_ms] = WIFI_A_BT_A
	    		elif line.split()[5] == "false" and line.split()[11] == "true":
	    			state[ts_ms] = WIFI_A_BT_C
	    line = f.readline()
    return state
