from helper.decoder.decode_snoop import *


def hci_cmd_sniff_timestamp(snoop_fname):
    # filter the 14-byte HCI CMD -- (enter) SNIFF MODE
    cmd_sniff = {}  # map time to packet size
    all_data = read_Snoop(snoop_fname)
    pktno = 0
    while pktno < len(all_data) - 1:
        pkt_length = packet_length(all_data[pktno])
        if is_hci_cmd_sniff(all_data[pktno]):
            pkt_time = packet_time(all_data[pktno])
            cmd_sniff[pkt_time] = pkt_length
        pktno += 1
    return cmd_sniff

def hci_cmd_exitsniff_timestamp(snoop_fname):
    cmd_exitsniff = {}
    all_data = read_Snoop(snoop_fname)
    pktno = 0
    while pktno < len(all_data) - 1:
        pkt_length = packet_length(all_data[pktno])
        if is_hci_cmd_exit(all_data[pktno]):
            pkt_time = packet_time(all_data[pktno])
            cmd_exitsniff[pkt_time] = pkt_length
        pktno += 1
    return cmd_exitsniff

def hci_cmd_timestamp(snoop_fname):
    cmd ={}
    all_data = read_Snoop(snoop_fname)
    pktno = 0
    while pktno < len(all_data) - 1:
        pkt_length = packet_length(all_data[pktno])
        if is_hci_cmd(all_data[pktno]):
            pkt_time = packet_time(all_data[pktno])
            cmd[pkt_time] = pkt_length
        pktno += 1
    return cmd

def hci_cmd_create_timestamp(snoop_fname):
    # HCI Command: Create Connection
    cmd_create = {}
    all_data = read_Snoop(snoop_fname)
    pktno = 0
    while pktno < len(all_data) - 1:
        pkt_length = packet_length(all_data[pktno])
        if is_hci_cmd_create(all_data[pktno]):
            pkt_time = packet_time(all_data[pktno])
            cmd_create[pkt_time] = pkt_length
        pktno += 1
    return cmd_create

def hci_evt_change2active_timestamp(snoop_fname):
    # filter the 9-byte HCI Event -- Mode Change to active
    evt_change2active = {} 
    all_data = read_Snoop(snoop_fname)
    pktno = 0
    while pktno < len(all_data) - 1:
        pkt_length = packet_length(all_data[pktno])
        if packet_length(all_data[pktno])==9 and is_hci_evt_change2active(all_data[pktno]):
            pkt_time = packet_time(all_data[pktno])
            evt_change2active[pkt_time] = pkt_length
        pktno += 1
    return evt_change2active

def hci_evt_change2sniff_timestamp(snoop_fname):
    # filter the 9-byte HCI Event -- Mode Change to active
    evt_change2active = {} 
    all_data = read_Snoop(snoop_fname)
    pktno = 0
    while pktno < len(all_data) - 1:
        pkt_length = packet_length(all_data[pktno])
        if packet_length(all_data[pktno])==9 and is_hci_evt_change2sniff(all_data[pktno]):
            pkt_time = packet_time(all_data[pktno])
            evt_change2active[pkt_time] = pkt_length
        pktno += 1
    return evt_change2active

def hci_evt_timestamp(snoop_fname):
    evt = {}
    all_data = read_Snoop(snoop_fname)
    pktno = 0
    while pktno < len(all_data) - 1:
        pkt_length = packet_length(all_data[pktno])
        if is_hci_evt(all_data[pktno]):
            pkt_time = packet_time(all_data[pktno])
            evt[pkt_time] = pkt_length
        pktno += 1
    return evt
    
def hci_evt_number_timestamp(snoop_fname):
    # HCI Event: Number of Completed Packtes
    evt_number = {}
    all_data = read_Snoop(snoop_fname)
    pktno = 0
    while pktno < len(all_data) - 1:
        pkt_length = packet_length(all_data[pktno])
        if is_hci_evt_number(all_data[pktno]):
            pkt_time = packet_time(all_data[pktno])
            evt_number[pkt_time] = pkt_length
        pktno += 1
    return evt_number

def hci_evt_change_timestamp(snoop_fname):
    # HCI Event: Mode Change
    evt_change = {}
    all_data = read_Snoop(snoop_fname)
    pktno = 0
    while pktno < len(all_data) - 1:
        pkt_length = packet_length(all_data[pktno])
        if is_hci_evt_change(all_data[pktno]):
            pkt_time = packet_time(all_data[pktno])
            evt_change[pkt_time] = pkt_length
        pktno += 1
    return evt_change

def hci_evt_status_timestamp(snoop_fname):
    evt_status = {}
    all_data = read_Snoop(snoop_fname)
    pktno = 0
    while pktno < len(all_data) - 1:
        pkt_length = packet_length(all_data[pktno])
        if is_hci_evt_status(all_data[pktno]):
            pkt_time = packet_time(all_data[pktno])
            evt_status[pkt_time] = pkt_length
        pktno += 1
    return evt_status

def hci_evt_subrating_timestamp(snoop_fname):
    evt_subrating = {}
    all_data = read_Snoop(snoop_fname)
    pktno = 0
    while pktno < len(all_data) - 1:
        pkt_length = packet_length(all_data[pktno])
        if is_hci_evt_subrating(all_data[pktno]):
            pkt_time = packet_time(all_data[pktno])
            evt_subrating[pkt_time] = pkt_length
        pktno += 1
    return evt_subrating
