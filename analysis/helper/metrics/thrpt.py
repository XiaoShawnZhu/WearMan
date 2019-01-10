from helper.filter.pcap_filter import *
from helper.filter.snoop_filter import *

def get_thrpt_kbps_from_pcap(pcap_fname, svr_ip, svr_port, granularity):
    # get the dict of time:bytes
    datapkt = pcap_payload_timestamp(pcap_fname, svr_ip, svr_port, False)
    return timelog_to_thr_kbps(datapkt, granularity)

# timelog is a dict of time:bytes, granularity is 1000, 500, 200 (ms), etc
def timelog_to_thr_kbps(timelog, granularity):
    thr={}
    factor = 1000.0 / granularity
    arr_int = {}
    x=[]
    y=[]
    for key in timelog:
        time = int(key / granularity)
        data = timelog[key]
        if time in arr_int.keys():
            arr_int[time] += data
        else:
            arr_int[time] = data
    first = min(arr_int)
    last = max(arr_int)
    while first < last:
        x.append(first * granularity / 1000.0)
        if first in arr_int.keys():
            thr[first] = arr_int[first]
        else:
            thr[first] = 0
        first += 1
    x.sort()
    for key in thr:
       y.append(8 * factor * thr[key] / 1e3) #kbps
    return [x,y]