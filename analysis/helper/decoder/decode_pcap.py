# !/usr/bin/python
#coding=utf-8
import struct
import socket
import json

def decode_PcapFileHeader(B_datastring):
 
    """   
        4 bytes       2 bytes     2 bytes     4 bytes    4 bytes   4 bytes   4 bytes
        ------------------------------------------------------------------------------
Header  | magic_num | ver_major | ver_minor | thiszone | sigfigs | snaplen | linktype|
        ------------------------------------------------------------------------------
    """
    header = {}
    header['magic_number'] = B_datastring[0:4]
    header['version_major'] = B_datastring[4:6]
    header['version_minor'] = B_datastring[6:8]
    header['thiszone'] = B_datastring[8:12]
    header['sigfigs'] = B_datastring[12:16]
    header['snaplen'] = B_datastring[16:20]
    header['linktype'] = B_datastring[20:24]
    return header
 
def decode_PcapDataPacket(B_datastring):
    """   
          4 bytes    4 bytes    4 bytes 4 bytes   
        ----------------------------------------------
Packet  | GMTtime | MicroTime | CapLen | Len |  Data |
        ----------------------------------------------
        |------------Packet Header-----------|
    """
    packet_num = 0
    packet_data = []
    header = ''
    data = ''
    i = 24
 
    while(i+16<len(B_datastring)):
        
       #header['GMTtime'] = B_datastring[i:i+4]
       #header['MicroTime'] = B_datastring[i+4:i+8]
       #header['CapLen'] = B_datastring[i+8:i+12]
       #header['Len'] = B_datastring[i+12:i+16]
       
       # the len of this packet
       header = B_datastring[i:i+16]
       packet_len = struct.unpack('I', B_datastring[i+8:i+12])[0]
       if (i+16+packet_len > len(B_datastring)):
           break
       # the data of this packet
       data = B_datastring[i+16:i+16+packet_len]
      
       # save this packet data
       packet_data.append((header,data))
 
       i = i + packet_len + 16
       packet_num += 1
          
    return packet_data
   
def read_Pcap(fileName):
    filepcap = open(fileName,'rb')
    string_data = filepcap.read()
    packet_data = decode_PcapDataPacket(string_data)
    return packet_data

def is_ip_tcp_no_syn_fin(data):
    if len(data) < 26:
        return False
    if data[16] >> 4 != 4:
        return False
    op_loc = 16
    if data[op_loc+9] != 6:
        return False
    tp_flags = 16 + (data[16] & 0x0f) * 4 + 13
    if data[tp_flags] & 3 == 0:
        return True
    return False

def is_ip_tcp_syn(data):
    if len(data) < 26:
        return False
    if data[16] >> 4 != 4:
        return False
    op_loc = 16
    if data[op_loc+9] != 6:
        return False
    tp_flags = 16 + (data[16] & 0x0f) * 4 + 13
    if data[tp_flags] & 0x02 > 0:
        return True
    return False

def ip_str(byte_array):
    return (str(byte_array[0]) + '.' + str(byte_array[1]) + '.'
            + str(byte_array[2]) + '.' + str(byte_array[3]))

def port_str(byte_array):
    return str(byte_array[0] * 256 + byte_array[1])

def src_ip_str(data):
    return ip_str(data[28:32])

def dst_ip_str(data):
    return ip_str(data[32:36])

def src_port_str(data):
    return port_str(data[36:38])

def dst_port_str(data):
    return port_str(data[38:40])

def window_size(packet_data, i):
	return packet_data[i][1][50] * 256 + packet_data[i][1][51]

def packet_time(packet_data, i):
    seconds = struct.unpack('I',packet_data[i][0][0:4])[0]
    microseconds = struct.unpack('I',packet_data[i][0][4:8])[0]
    return (seconds * 1000 + microseconds/1000)

def packet_len(packet_data, i):
    length = struct.unpack('I', packet_data[i][0][8:12])[0]
    return length

def packet_len_hd(packet_data, i):
    return packet_data[i][1][18]*256+packet_data[i][1][19]-52

def sequence_num(packet_data, i):
	return packet_data[i][1][40] * 16777216\
           + packet_data[i][1][41] * 65536\
           + packet_data[i][1][42] * 256\
           + packet_data[i][1][43]

def is_duplicate(packet_data, i, exp_seq):
    if exp_seq == -1:
        return False
    seq = sequence_num(packet_data, i)
    if(exp_seq > seq):
        # print('exp_seq:' + str(exp_seq) + ' seq:' + str(seq))
        return True
    return False