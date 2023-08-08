#!/use/bin/python
import getopt
import json
import requests
import sys
import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse

def get_temperature():
    mc = ModbusClient(method='rtu', port='/dev/ttyUSB0', stopbits=1, bytesize=8, parity='N', baudrate=9600, timeout=5, unit=1)
    con = mc.connect()
    r = mc.read_holding_registers(256, 35, unit=1)
    temp = json.dumps({"raw": r.registers[3], "hex":  hex(r.registers[3]), "mppt": int(hex(r.registers[3])[2:-2],16)*9/5+32, "battery": int(hex(r.registers[3])[-2:],16)*9/5+32})
    return temp

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
    return json.dumps(response_json['location'])

def get_signal(url, sessionid):
    endpoint = url + '/status.wan.connection.signal'
    header = {"content-type":"application/json", "cookie":"pauth=" + sessionid}
    response = requests.get(endpoint, headers=header)
    response_json = response.json()['response']
    for k, v in response_json.items():
        if k == '2':
            return json.dumps(v['band'][0]['signal'])

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"tcgs",["temperature=", "client=", "gps=", "signal="])
        url = "http://192.168.1.1:8080/api"
        sessionid = login(url)
    except getopt.GetoptError:
        print("py_pepwave_api.py -c")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("py_pepwave_api.py -t -c -g -s")
        elif opt in ("-t", "--temperature"):
            sys.stdout.write(get_temperature())
        elif opt in ("-c", "--client"):
            sys.stdout.write(get_client(url, sessionid))
        elif opt in ("-g", "--gps"):
            sys.stdout.write(get_gps(url, sessionid))
        elif opt in ("-s", "--signal"):
            sys.stdout.write(get_signal(url, sessionid))
        elif opt in ("-a", "--all"):
            sys.stdout.write("[" + get_temperature() + "," + get_client(url, sessionid) + "," + get_gps(url, sessionid) + "," + get_signal(url, sessionid) + "]")
    logout(url, sessionid)

if __name__ == '__main__':
    main(sys.argv[1:])
