#!/usr/bin/python3

#
# getISOTimeStamp
# secondsSinceEpoch - an arbitrary number of seconds since the Unix epoch
# returns an ISO8601 formatted timestamp in UTC 
# example: 2017-01-01T02:25:00+00:00
#
def getISOTimeStamp(secondsSinceEpoch):
    timeStamp = datetime.fromtimestamp(secondsSinceEpoch, tz=timezone.utc)
    timeStampNoMicroseconds = timeStamp.replace(microsecond=0)
    ISOTimeStamp = timeStampNoMicroseconds.isoformat()
    return ISOTimeStamp

#
# getIndex
# haystack - an array
# returns a random value from an array
#
def getIndex(haystack):
    needle = random.randint(0, len(haystack) - 1)
    return needle

#
# createProxyLine
# ts - a timestamp
# u - a username
# ip - an IP address
# s - a site domain (ex: www.google.com)
# returns a JSON-formatted log entry of the "proxy" type
#
def createProxyLine(ts, u, ip, s):
    a_line = '{'
    a_line = a_line + '"timestamp":"' + ts + '",'
    a_line = a_line + '"ip_address":"' + ip + '",'
    a_line = a_line + '"username":"' + u + '",'
    a_line = a_line + '"site":"' + s + '"'
    a_line = a_line + '}\n'
    return a_line

#
# createProxyLogs
# ts_time - timestamp (in seconds) of the first log entry
#           this increases by one second each iteration of the loop
# end_time - timestamp (in seconds) of the last log entry
# consistent_logs - if this is true, every entry for
#                   a given username will always use the same IP
# this function creates one log entry per second between 
#   start_time and end_time and batch writes them, 10000 at a time,
#   to a file called proxy.log
#
def createProxyLogs(ts_time, end_time, users, sites, user_ips, consistent_logs = False):
    proxy_out = open('proxy.log', 'w')
    line_count = 0
    line_batch = ""
    while (ts_time <= end_time):
        iso_ts = getISOTimeStamp(ts_time)
        user_offset = getIndex(users)
        user = users[user_offset]
        if(consistent_logs):
            ip = user_ips[user_offset]
        else:
            ip = user_ips[getIndex(user_ips)]
        site = sites[getIndex(sites)]
        line_batch = line_batch + createProxyLine(iso_ts, user, ip, site)
        if(line_count%10000 == 0 or ts_time == end_time):
            proxy_out.write(line_batch)
            line_batch = ""
        ts_time = ts_time + 1
        line_count = line_count + 1
    print("Total proxy logs written: " + str(line_count))
    print()

#
# createDNSLine
# ts - a timestamp
# i_dns - the internal DNS server
# e_dns - the responding DNS server
# resp_ip - the response to the DNS query
# domain - the domain requested
# returns a JSON-formatted log entry of the "dns" type
#
def createDNSLine(ts, i_dns, e_dns, query, answer):
    a_line = '{'
    a_line = a_line + '"timestamp":"' + ts + '",'
    a_line = a_line + '"client_ip":"' + i_dns + '",'
    a_line = a_line + '"dns_server":"' + e_dns + '",'
    a_line = a_line + '"query":"' + query + '",'
    a_line = a_line + '"answer":"' + answer + '"'
    a_line = a_line + '}\n'
    return a_line


def createDNSLogs(ts_time, end_time, i_dns, e_dns, sites, bbc_uk, bbc_com, google, cnn):
    dns_out = open('dns.log', 'w')
    line_count = 0
    line_batch = ""
    while(ts_time <= end_time):
        i_dns_ip = i_dns[random.randint(0, len(i_dns) - 1)]
        e_dns_ip = e_dns[random.randint(0, len(i_dns) - 1)]
        query = sites[random.randint(0, len(sites) - 1)]
        if 'bbc.com' in query:
            response = bbc_com[random.randint(0, len(bbc_com) - 1)]
        elif 'bbc.co.uk' in query:
            response = bbc_uk[random.randint(0, len(bbc_uk) - 1)]
        elif 'cnn' in query:
            response = cnn[random.randint(0, len(cnn) - 1)]
        elif 'google' in query:
            response = google[random.randint(0, len(google) - 1)]
        else:
            print('unknown query: ' + domain)
            exit()
        iso_ts = getISOTimeStamp(ts_time)
        line_batch = line_batch + createDNSLine(iso_ts, i_dns_ip, e_dns_ip, query, response)
        if(line_count%10000 == 0 or ts_time >= end_time):
            dns_out.write(line_batch)
            line_batch = ""
        ts_time = ts_time + 1
        line_count = line_count + 1
    print("createDNSLogs lines processed: " + str(line_count))
    print()
 
def createDHCPLogs(start_time, end_time):
    print("In createDHCPLogs")
    print("Start time: " + getISOTimeStamp(start_time))
    print("End time: " + getISOTimeStamp(end_time))

import argparse
from datetime import datetime, timezone
from time import time
import random

#
# all of the possible arguments
#
parser = argparse.ArgumentParser()
parser.add_argument('--days', dest='days', help='How many days back to start generating logs; the default is fourteen days', default='14')
parser.add_argument('--dhcp', dest='dhcplogs', help='If set, generate something that looks like DHCP logs', action='store_true')
parser.add_argument('--dns', dest='dnslogs', help='If set, generate something that looks like DNS logs', action='store_true')
parser.add_argument('--proxy', dest='proxylogs', help='If set, generate something that looks like proxy logs', action='store_true')
parser.add_argument('--all', dest='alllogs', help='If set, generate all log types', action='store_true')
parser.add_argument('--consistent', dest='consistentlogs', help='If set, users and IPs may or may not be consistent...', action='store_true')
args=parser.parse_args()

num_days = int(args.days)
dhcp_logs = args.dhcplogs
dns_logs = args.dnslogs
proxy_logs = args.proxylogs
all_logs = args.alllogs
consistent_logs = args.consistentlogs

#
# the users for proxy logs
#
users = ["alvin", "simon", "theodore", "piper", "prue", "phoebe", "paige"]

#
# the sites for proxy and DNS logs
#
sites = ["www.bbc.co.uk", "www.bbc.com", "www.google.com", "www.cnn.com"]

#
# the IPs for proxy and DHCP logs
#
user_ips = ["10.10.10.1", "10.10.10.3", "10.10.10.8", "10.10.10.21", "10.10.20.2", "10.10.20.5", "10.10.20.13"]

#
# server IPs for passive DNS/DHCP logs
#
i_dns = ["172.16.1.1", "172.24.1.1"]
e_dns = ["8.8.8.8", "208.67.222.222", "208.67.220.220"]
dhcp = ["10.10.10.251", "10.10.20.251"]

#
# site IPs for passive DNS logs
#
bbc_uk = ["212.58.244.70", "212.58.246.94"]
bbc_com = ["151.101.56.81", "151.101.32.81"]
google = ["216.58.193.132"]
cnn = ["151.101.1.67", "151.101.193.67", "151.101.65.67", "151.101.129.67"]

#
# time setup
#
curr_time = time()
iso_curr_time = getISOTimeStamp(curr_time)
time_offset = num_days * 24 * 60 * 60
start_time = curr_time - time_offset
iso_start_time = getISOTimeStamp(start_time)

print()
print('Generating logs for ' + str(num_days) + ' days')
print('Log start time: ' + iso_start_time)
print('Log end time: ' + iso_curr_time)

if(dhcp_logs or all_logs):
    createDHCPLogs(start_time, curr_time)
if(dns_logs or all_logs):
    createDNSLogs(start_time, curr_time, i_dns, e_dns, sites, bbc_uk, bbc_com, google, cnn)
if(proxy_logs or all_logs):
    createProxyLogs(start_time, curr_time, users, sites, user_ips, consistent_logs)
       
exit()
