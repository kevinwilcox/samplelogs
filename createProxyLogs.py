#!/usr/bin/python3

def getISOTimeStamp(secondsSinceEpoch):
    timeStamp = datetime.fromtimestamp(secondsSinceEpoch, tz=timezone.utc)
    timeStampNoMicroseconds = timeStamp.replace(microsecond=0)
    ISOTimeStamp = timeStampNoMicroseconds.isoformat()
    return ISOTimeStamp

def createProxyLogs(start_time, end_time, consistent_logs = False):
    import random
    users = ["alvin", "simon", "theodore", "piper", "prue", "phoebe", "paige"]
    sites = ["https://www.bbc.co.uk", "https://www.bbc.com", "https://www.google.com", "https://www.cnn.com"]
    user_ips = ["10.10.10.1", "10.10.10.3", "10.10.10.8", "10.10.10.21", "10.10.20.2", "10.10.20.5", "10.10.20.13"]
    proxy_out = open('proxy.log', 'w')
    ts_time = start_time
    line_count = 0
    line_batch = ""
    total_lines = 0
    while (ts_time <= end_time):
        line_count = line_count + 1
        iso_ts = getISOTimeStamp(ts_time)
        user_offset = random.randint(0, len(users) - 1)
        if(consistent_logs):
            ip_offset = user_offset
        else:
            ip_offset = random.randint(0, len(user_ips) - 1)
        line_batch = line_batch + '{'
        line_batch = line_batch + '"timestamp":"' + iso_ts + '",'
        line_batch = line_batch + '"ip_address":"' + user_ips[ip_offset] + '",'
        line_batch = line_batch + '"username":"' + users[user_offset] + '",'
        line_batch = line_batch + '"site":"' + sites[random.randint(0,len(sites)-1)] + '"'
        line_batch = line_batch + '}' + "\n"
        ts_time = ts_time + 1
        total_lines = total_lines + 1
        if(line_count >= 1000 or ts_time == end_time):
            proxy_out.write(line_batch)
            line_batch = ""
            line_count = 0
    proxy_out.close()
    print("Total proxy logs written: " + str(total_lines))
    print()

import argparse
from datetime import datetime, timezone
from time import time

parser = argparse.ArgumentParser()
parser.add_argument('--days', dest='days', help='How many days back to start generating logs; the default is fourteen days', default='14')
parser.add_argument('--consistent', dest='consistentlogs', help='If set, users and IPs may or may not be consistent...', action='store_true')
args=parser.parse_args()

num_days = int(args.days)
consistent_logs = args.consistentlogs

curr_time = time()
iso_curr_time = getISOTimeStamp(curr_time)
time_offset = num_days * 24 * 60 * 60
start_time = curr_time - time_offset
iso_start_time = getISOTimeStamp(start_time)
print()
print('Generating logs for ' + str(num_days) + ' days')
print('Start time: ' + iso_start_time)
print('End time: ' + iso_curr_time)

createProxyLogs(start_time, curr_time, consistent_logs)
       
exit()
