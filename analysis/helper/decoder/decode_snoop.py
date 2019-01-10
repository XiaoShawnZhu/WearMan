# !/usr/bin/python
# coding=utf-8
import struct
import socket
import json

EPOCH_DELTA_MILLIS = 62168256000000 # from 01/01/0000 to 01/01/1970

def decode_SnoopFileHeader(B_datastring):
    """
                  8 bytes             4 bytes          4 bytes
        ------------------------------------------------------------
Header  | Identification Pattern | Version Number | Datalink Type |
        ------------------------------------------------------------
    """
    header = {}
    header['id_pattern'] = B_datastring[0:8]
    header['version_number'] = B_datastring[8:12]
    header['datalink_type'] = B_datastring[12:16]
    return header


def decode_SnoopDataPacket(B_datastring):
    """
              4 bytes           4 bytes           4 bytes           4 bytes           8 bytes        
        -----------------------------------------------------------------------------------------------------------------------------
Packet  | Original Length | Included Length | Packet Flags | Cumulative Drops |  Timestamp Microseconds |
        -----------------------------------------------------------------------------------------------------------------------------
    """
    packet_num = 0
    packet_data = []
    header = ''
    data = ''
    i = 16

    while (i + 24 < len(B_datastring)):

        # header['GMTtime'] = B_datastring[i:i+4]
        # header['MicroTime'] = B_datastring[i+4:i+8]
        # header['CapLen'] = B_datastring[i+8:i+12]
        # header['Len'] = B_datastring[i+12:i+16]

        # the len of this packet
        header = B_datastring[i:i + 24]
        # packet_len = struct.unpack('I', B_datastring[i+4:i+8])[0]
        origLen, incLen, flags, drops, time64 = struct.unpack(
            ">IIIIq", header)
        #print("Len: ", origLen, incLen, flags, drops, time64)
        if (i + 24 + incLen > len(B_datastring)):
            break
        # the data of this packet
        data = B_datastring[i + 24:i + 24 + incLen]

        # save this packet data
        packet_data.append((header, data))

        i = i + incLen + 24
        packet_num += 1

    return packet_data

def read_Snoop(fileName):
    filepcap = open(fileName, 'rb')
    string_data = filepcap.read()
    packet_data = decode_SnoopDataPacket(string_data)
    return packet_data

def packet_time(packet_data):
    origLen, incLen, flags, drops, microseconds = struct.unpack(
        ">IIIIQ", packet_data[0][0:24])
    #seconds = struct.unpack('I', packet_data[0][16:20])[0]
    #microseconds = struct.unpack('I',packet_data[0][20:24])[0]
    #seconds = struct.unpack('I',packet_data[0][16:20])[0]
    #print(origLen, incLen, flags, drops, seconds, microseconds)
    #print(microseconds/1000000.0)
    #return (seconds * 1000 + microseconds/1000)
    return microseconds/1000.0 - EPOCH_DELTA_MILLIS
    #return time64

def packet_length(packet_data):
    origLen, incLen, flags, drops, seconds, microseconds = struct.unpack(
        ">IIIIII", packet_data[0])
    return incLen

def packet_flag(packet_data):
    """
Record flags conform to:
    - bit 0         0 = sent, 1 = received
    - bit 1         0 = data, 1 = command/event
    - bit 2-31      reserved
Direction is relative to host / DTE. i.e. for Bluetooth controllers,
Send is Host->Controller, Receive is Controller->Host

BTSNOOP_FLAGS = {
        0 : ("host", "controller", "data"),
        1 : ("controller", "host", "data"),
        2 : ("host", "controller", "command"),
        3 : ("controller", "host", "event")
    }
    """
    origLen, incLen, flags, drops, seconds, microseconds = struct.unpack(
        ">IIIIII", packet_data[0])
    return flags

def is_hci_cmd(packet):
    first = packet[1][0]
    #print(hex(first))
    if first == 0x01:
        return True
    return False

def is_hci_evt(packet):
    first = packet[1][0]
    #print(hex(first))
    if first == 0x04:
        return True
    return False

def is_acl_data(packet):
    first = packet[1][0]
    #print(hex(first))
    if first == 0x02:
        return True
    return False

def is_hci_cmd_sniff(packet):
    first = packet[1][0]
    opcode1 = packet[1][1]
    opcode2 = packet[1][2]
    # print(hex(opcode1))
    if first == 0x01 and opcode1 == 0x03 and opcode2 == 0x08:
        return True
    return False

def is_hci_cmd_exit(packet):
    first = packet[1][0]
    opcode1 = packet[1][1]
    opcode2 = packet[1][2]
    if first == 0x01 and opcode1 == 0x04 and opcode2 == 0x08:
        return True
    return False

def is_hci_cmd_create(packet):
    first = packet[1][0]
    opcode1 = packet[1][1]
    opcode2 = packet[1][2]
    if first == 0x01 and opcode1 == 0x05 and opcode2 == 0x04:
        return True
    return False

def is_hci_evt_change(packet):
    first = packet[1][0]
    second = packet[1][1]
    #print(hex(first))
    if first == 0x04 and second == 0x14:
        return True
    return False

def is_hci_evt_change2active(packet):
    """
        Byte 1: HCI Packet Type: HCI Event (0x04)
        Byte 2: Event Code: Mode Change (0x14)
        ......
        Byte 6: Current Mode: Active Mode (0x00)
    """
    first = packet[1][0]
    second = packet[1][1]
    six = packet[1][6]
    if first == 0x04 and second == 0x14 and six == 0x00:
        return True
    return False

def is_hci_evt_change2sniff(packet):
    """
        Byte 1: HCI Packet Type: HCI Event (0x04)
        Byte 2: Event Code: Mode Change (0x14)
        ......
        Byte 6: Current Mode: Active Mode (0x02)
    """
    first = packet[1][0]
    second = packet[1][1]
    six = packet[1][6]
    if first == 0x04 and second == 0x14 and six == 0x02:
        return True
    return False

def is_hci_evt_number(packet):
    first = packet[1][0]
    second = packet[1][1]
    if first == 0x04 and second == 0x13:
        return True
    return False

def is_hci_evt_status(packet):
    first = packet[1][0]
    second = packet[1][1]
    if first == 0x04 and second == 0x0f:
        return True
    return False

def is_hci_evt_subrating(packet):
    first = packet[1][0]
    second = packet[1][1]
    if first == 0x04 and second == 0x2e:
        return True
    return False

def is_hci_evt_disconn(packet):
    if len(packet[1]) < 2:
        return False
    first = packet[1][0]
    second = packet[1][1]
    if first == 0x04 and second == 0x05:
        return True
    return False

def l2cap_cid(packet, seven, eight):
    if packet[1][7] == seven and packet[1][8] == eight:
        return True
    return False
