#!/use/bin/python
import re
import getopt
import json
import requests
import sys
import time
import socket
import paramiko
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse

def send_udp(msg):
    udp_ip = '0.0.0.0'
    udp_port = 8094
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((udp_ip, udp_port))
    sock.send(msg)

def get_temperature():
    mc = ModbusClient(method='rtu', port='/dev/ttyUSB0', stopbits=1, bytesize=8, parity='N', baudrate=9600, timeout=5, unit=1)
    con = mc.connect()
    r = mc.read_holding_registers(256, 35, unit=1)
    temp = json.dumps({"raw": r.registers[3], "hex":  hex(r.registers[3]), "mppt": int(hex(r.registers[3])[2:-2],16)*9/5+32, "battery": int(hex(r.registers[3])[-2:],16)*9/5+32}).encode('utf-8')
    send_udp(temp)
    return temp.decode('utf-8')

def get_session_geoip():
    #Connect to telegraf udp port
    #IPstack API
    access_key = '00fc621e986c788901b3f148aaefd755'
    ssh_client = paramiko.client.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect('192.168.1.1', 8822, 'admin', 'admin12345')
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
                send_udp(msg)
    return(json.dumps(loc_list))

def login(url):
    endpoint = url + '/login'
    payload = {"username":"admin", "password":"admin12345"}
    header = {"content-type":"application/json"}
    session = requests.Session()
    response = session.post(endpoint, data=json.dumps(payload), headers=header)
    cookies = response.cookies.get_dict()
    sessionid = cookies["pauth"]
    return sessionid

def logout(url, sessionid):
    endpoint = url + '/logout'
    header = {"content-type":"application/json", "cookie":"pauth=" + sessionid}
    response = requests.post(endpoint, headers=header)

def get_client(url, sessionid):
    endpoint = url + '/status.client'
    header = {"content-type":"application/json", "cookie":"pauth=" + sessionid}
    client_list = []
    response = requests.get(endpoint, headers=header)
    response_json = response.json()['response']
    for i in response_json.values():
        client_list += i
    return json.dumps(client_list)

def get_gps(url, sessionid):
    endpoint = url + '/info.location'
    header = {"content-type":"application/json", "cookie":"pauth=" + sessionid}
    response = requests.get(endpoint, headers=header)
    response_json = response.json()['response']
    return json.dumps((response_json['location']))

def get_signal(url, sessionid):
    endpoint = url + '/status.wan.connection.signal'
    header = {"content-type":"application/json", "cookie":"pauth=" + sessionid}
    response = requests.get(endpoint, headers=header)
    response_json = response.json()['response']
    for k, v in response_json.items():
        if k == '2':
            return json.dumps((v['band'][0]['signal']))

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"tncgs",["temperature=", "session=", "client=", "gps=", "signal="])
        url = "http://192.168.1.1:8080/api"
        sessionid = login(url)
    except getopt.GetoptError:
        print("py_pepwave_api_v2.py -c")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("py_pepwave_api_v2.py -t -n -c -g -s")
        elif opt in ("-t", "--temperature"):
            sys.stdout.write(get_temperature())
        elif opt in ("-n", "--session"):
            sys.stdout.write(get_session_geoip())
        elif opt in ("-c", "--client"):
            sys.stdout.write(get_client(url, sessionid))
        elif opt in ("-g", "--gps"):
            sys.stdout.write(get_gps(url, sessionid))
        elif opt in ("-s", "--signal"):
            sys.stdout.write(get_signal(url, sessionid))
        elif opt in ("-a", "--all"):
            sys.stdout.write("[" + get_client(url, sessionid) + "," + get_gps(url, sessionid) + "," + get_signal(url, sessionid) + "]")
    logout(url, sessionid)

if __name__ == '__main__':
    main(sys.argv[1:])
