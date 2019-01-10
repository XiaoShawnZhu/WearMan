import sys

from helper.filter.pcap_filter import *
from helper.filter.snoop_filter import *

E2E = 0
SVR2PHONE = 1
TCP_RCV = 2
PROXY = 3
PHONE2WEAR = 4

def get_delay(_type, tx_fn, rx_fn, svr_ip, svr_port, offset, pkt_size, signature):
    # map send and recv data from the very beginning
    send_data, recv_data = 0, 0 
    # track the data accumulation
    rx_acc, tx_acc = {}, {}
    # timestamp to payload size map
    tx_timelog, rx_timelog = [], []
    # payload byte mapping 
    cnt, rx_pos, tx_pos = 0, 0, 0
    # store delay values
    delay_list, delay_send_t, delay_recv_t = [], [], []
    # decide delay type
    return_type = 0
    if _type == E2E or _type == SVR2PHONE:
        tx_timelog = pcap_payload_timestamp(tx_fn, svr_ip, svr_port, True)
        rx_timelog = pcap_payload_timestamp(rx_fn, svr_ip, svr_port, False)
        if _type == E2E:
            return_type = 1
    elif _type == TCP_RCV:
        tx_timelog = pcap_payload_timestamp(tx_fn, svr_ip, svr_port, False)
        rx_timelog = kernel_payload_timestamp(rx_fn, svr_ip, svr_port, pkt_size)
    elif _type == PROXY:
        tx_timelog = kernel_payload_timestamp(tx_fn, svr_ip, svr_port, pkt_size)
        rx_timelog = android_payload_timestamp(rx_fn, signature)
    elif _type == PHONE2WEAR:
        tx_timelog = android_payload_timestamp(tx_fn, signature)
        rx_timelog = pcap_payload_timestamp(rx_fn, svr_ip, svr_port, False)
    else:
        print("[ERROR] NO SUCH DELAY TYPE !!!")
        sys.exit(0)
    rx_key_sorted = sorted(list(rx_timelog.keys()))
    tx_key_sorted = sorted(list(tx_timelog.keys()))
    for key in tx_key_sorted:
        send_data += tx_timelog[key]
        tx_acc[key] = send_data
    for key in rx_key_sorted:
        recv_data += rx_timelog[key]
        rx_acc[key] = recv_data
    # calculate delay every 1000 bytes
    while cnt < recv_data/1000:
        for i in range(rx_pos, len(rx_key_sorted)):
            key = rx_key_sorted[i]
            if rx_acc[key] >= cnt*1000:
                rx_time = key
                rx_pos = i
                break
        for i in range(tx_pos, len(tx_key_sorted)):
            key = tx_key_sorted[i]
            if tx_acc[key] >= cnt*1000:
                tx_time = key
                tx_pos = i
                break
        delay_send_t.append(tx_time)
        delay_recv_t.append(rx_time)
        delay_list.append(rx_time - tx_time + offset)
        cnt += 1
    if return_type == 1:
        return [range(0, cnt*1000, 1000), delay_list, delay_recv_t] # bytes as the x axis
    else:
        return [range(0, cnt*1000, 1000), delay_list]
