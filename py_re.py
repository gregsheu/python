import re
import requests
import json
import paramiko
import time
import socket

#access_key = '00fc621e986c788901b3f148aaefd755'
#ssh_client = paramiko.client.SSHClient()
#ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh_client.connect('192.168.1.1', 8822, 'admin', 'admin12345')
#stdin, stdout, stderr = ssh_client.exec_command('get session')
#time.sleep(1)
##Exclude the first occurance
##pattern = re.compile("(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):\d+")
#pattern = re.compile("(?!(192.168.1.\d{1,3})):\d+\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):\d+")
#re_pattern = re.compile("^((?!192.168.1.\d{1,3}).)*$")
#match = None
#invert_match = None
##with open('sship.txt', 'r') as f:
#match = pattern.findall(stdout.read().decode('utf-8'))
loc_list = []
udp_ip = '0.0.0.0'
udp_port = 8094
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((udp_ip, udp_port))
#if match != None:
#    for i in match:
#        invert_match = re.search("^((?!192.168.1.\d{1,3}).)*$", i[1])
#        if invert_match:
#            print(invert_match.group())
#            ip = invert_match.group()
#            response = requests.get('http://api.ipstack.com/%s?access_key=%s' % (ip, access_key))
#            ccode = response.json()['country_code']
#            ip_address = response.json()['ip']
#            lat = response.json()['latitude']
#            lon = response.json()['longitude']
#            loc_list.append({'country': ccode, 'name': ip_address, 'lat': lat, 'lon': lon})
#            #echo "m1,tag1=tag_value value=1" | nc -u -4 -q localhost 8094
#            print('Sent')
#            time.sleep(1)

#working to send as json
msg = json.dumps({'lat': 33.12233, 'lon': -114.344, 'country': 'US', 'ip': '123.23.12.23', 'name': 'geoip'}).encode('utf-8')
#msg = ("socket_listener,country=%s,ip=%s lat=%d %s\n" % ('US', '123.3.1.33', 34.343, time.time_ns())).encode('utf-8')
#msg = msg + ("socket_listener,country=%s,ip=%s lon=%d %s\n" % ('US', '123.3.1.33', -117.3434, time.time_ns())).encode('utf-8')
sock.send(msg)
print('Sent')
print(json.dumps(loc_list))
