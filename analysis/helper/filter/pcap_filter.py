from helper.decoder.decode_pcap import *

HEADER = 68

def pcap_payload_timestamp(pcap_fname, svr_ip, svr_port, is_server):
    payload={}
    pktno = 0
    exp_seq = -1
    pkt_len = 0
    seq_map = {}
    exp_seq_list = []
    all_data = read_Pcap(pcap_fname)
    while pktno < len(all_data) - 1:
        header = all_data[pktno][0]
        data = all_data[pktno][1]
        if (is_ip_tcp_no_syn_fin(data)):
            if (src_ip_str(data) == svr_ip and src_port_str(data) == svr_port):
                pkt_len = struct.unpack('I', header[8:12])[0]  # pkt length
                if pkt_len > HEADER: 
                    if is_server:
                        pkt_time = packet_time(all_data, pktno)
                        seq = sequence_num(all_data, pktno)
                        exp_seq = seq + pkt_len - HEADER
                        if seq in seq_map:
                            pass
                        else:
                            payload[pkt_time] = pkt_len - HEADER 
                            seq_map[seq] = pkt_len - HEADER
                    else:
                        pkt_time = packet_time(all_data, pktno)
                        seq = sequence_num(all_data, pktno)
                        if exp_seq == -1:
                            exp_seq = seq
                        if seq == exp_seq:
                            exp_seq = seq + pkt_len - HEADER
                            for key in seq_map:
                                if exp_seq == key:
                                    exp_seq = key + seq_map[key]
                                    payload[pkt_time] = seq_map[key]
                            payload[pkt_time] = pkt_len - HEADER
                            seq_map[seq] = pkt_len - HEADER
                        elif seq > exp_seq:
                            if seq in seq_map:
                                pass
                            else:
                                seq_map[seq] = pkt_len - HEADER
                        else:
                            pass
        pktno += 1
    return payload

def kernel_payload_timestamp(dmesg_fname, svr_ip, svr_port, first):
    payload={}
    start_seq = 0
    last_seq = 0
    dmesg_f = open(dmesg_fname, 'r')
    line = dmesg_f.readline()
    while line:
        ll = line.split('WearMan')[1]
        ts_ms = 1000.0 * float(ll.split()[3]) + float(ll.split()[4]) / 1000000.0
        ip = ll.split()[1]
        port = ll.split()[2]
        if start_seq == 0:
            start_seq = int(ll.split()[0])
            last_seq = start_seq - first
        seq = int(ll.split()[0])
        data = seq - last_seq
        if data > 0 and svr_ip == ip and svr_port == port:
            payload[ts_ms] = data
            last_seq = seq
        line = dmesg_f.readline()
    return payload

def android_payload_timestamp(phone_send_fn, signature):
    payload={}
    logcat_f = open(phone_send_fn, 'r')
    line = logcat_f.readline()
    while line:
        if len(line.split()) == 16:
            id1 = line.split()[9]
            id2 = line.split()[10]
            id3 = line.split()[11]
            id4 = line.split()[12]
            id5 = line.split()[13]
            ts_ms = int(line.split()[7])
            data = int(line.split()[8])
            if data > 0 and id1 == "[" + str(signature[0]) + "," and id2 == str(signature[1]) + "," \
            and id3 == str(signature[2]) + "," and id4 == str(signature[3]) + "," and id5 == str(signature[4]) + ",":
                if ts_ms in payload:
                    payload[ts_ms] += data - 7
                else:
                    payload[ts_ms] = data - 7
        line = logcat_f.readline()
    return payload
