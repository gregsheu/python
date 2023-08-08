#!/use/bin/python
import re
import getopt
import json
import requests
import sys
import time
import socket
import paramiko

def send_udp(msg):
    #Run telegraf on unix socket
    telegraf_socket = "/tmp/telegraf.sock"
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.connect(telegraf_socket)
    #Run as udp://:8094
    #udp_ip = '0.0.0.0'
    #udp_port = 8094
    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.connect((udp_ip, udp_port))
    sock.send(msg)

def get_session_geoip():
    #Connect to telegraf udp port
    #IPstack API
    access_key = '00fc621e986c788901b3f148aaefd755'
    ssh_client = paramiko.client.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect('107.126.222.254', 8822, 'admin', 'admin12345')
    stdin, stdout, stderr = ssh_client.exec_command('get session')
    time.sleep(1)
    #Exclude the first occurance
    #pattern = re.compile("(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):\d+")
    pattern = re.compile("(?!(192.168.1.\d{1,3})):\d+\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):\d+")
    re_pattern = re.compile("^((?!192.168.1.\d{1,3}).)*$")
    match = None
    invert_match = None
    #with open('sship.txt', 'r') as f:
    match = pattern.findall(stdout.read().decode('utf-8'))
    loc_list = []
    if match != None:
        for i in match:
            invert_match = re.search("^((?!192.168.1.\d{1,3}).)*$", i[1])
            if invert_match:
                #print(invert_match.group())
                ip = invert_match.group()
                response = requests.get('http://api.ipstack.com/%s?access_key=%s' % (ip, access_key))
                ccode = response.json()['country_code']
                address = response.json()['ip']
                lat = response.json()['latitude']
                lon = response.json()['longitude']
                loc_list.append({'country': ccode, 'ip': address, 'lat': lat, 'lon': lon, 'name': 'geoip'})
                #These two lines ingest as format of influx
                #msg = ("socket_listener,country=%s,ip=%s lat=%f %s\n" % (ccode, address, lat, time.time_ns())).encode('utf-8')
                #msg = msg + ("socket_listener,country=%s,ip=%s lon=%f %s\n" % (ccode, address, lon, time.time_ns())).encode('utf-8')
                #This line ingest as format of json to influx
                msg = json.dumps({'lat': lat, 'lon': lon, 'country': ccode, 'ip': address, 'name': 'geoip'}).encode('utf-8')
                #send_udp(msg)
                print(msg)

def main(argv):
    while True:
        get_session_geoip()
        time.sleep(21600)

if __name__ == '__main__':
    main(sys.argv[1:])
