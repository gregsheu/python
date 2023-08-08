import os
import json
import requests
import sys
import time
import urllib3, urllib
from requests.auth import HTTPDigestAuth

def login(url):
    endpoint = url + '/login'
    payload = {"username":"admin", "password":"admin12345"}
    header = {"content-type":"application/json"}
    session = requests.Session()
    response = session.post(endpoint, data=json.dumps(payload), headers=header, verify=False)
    cookies = response.cookies.get_dict()
    sessionid = cookies["bauth"]
    return sessionid

def logout(url, sessionid):
    endpoint = url + '/logout'
    header = {"content-type":"application/json", "cookie":"bauth=" + sessionid}
    response = requests.post(endpoint, headers=header, verify=False)

def get_wan(url, sessionid):
    endpoint = url + '/status.wan.connection'
    header = {"content-type":"application/json", "cookie":"bauth=" + sessionid}
    response = requests.get(endpoint, headers=header, verify=False)
    response_json = response.json()['response']
    return(response_json)

def get_gps(url, sessionid):
    endpoint = url + '/info.location'
    header = {"content-type":"application/json", "cookie":"bauth=" + sessionid}
    response = requests.get(endpoint, headers=header, verify=False)
    response_json = response.json()['response']
    return response_json['location']

def get_client(url, sessionid):
    endpoint = url + '/status.client'
    header = {"content-type":"application/json", "cookie":"bauth=" + sessionid}
    client_list = []
    response = requests.get(endpoint, headers=header, verify=False)
    response_json = response.json()['response']
    for i in response_json.values():
        client_list += i
    for i in client_list:
        if i['active']:
            print(i['ip'] + ' ' + i['connectionType'] + ' active: true')
    return(client_list)

def get_bandwidth(url, sessionid):
    endpoint = url + '/status.wan.connection.allowance'
    header = {"content-type":"application/json", "cookie":"bauth=" + sessionid}
    response = requests.get(endpoint, headers=header, verify=False)
    response_json = response.json()['response']
    return(response_json)

def post_sms(url, sessionid):
    endpoint = url + '/cmd.sms.sendMessage'
    payload = {"address":"+12533349251", "content":"Alert Tripwires"}
    header = {"content-type":"application/json", "cookie":"bauth=" + sessionid}
    response = requests.post(endpoint, data=json.dumps(payload), headers=header, verify=False)
    response_json = response.json()
    return(response_json)

def get_sms(url, sessionid):
    endpoint = url + '/cmd.sms.get?connId=2'
    header = {"content-type":"application/json", "cookie":"bauth=" + sessionid}
    response = requests.post(endpoint, headers=header, verify=False)
    response_json = response.json()
    return(response_json)

def get_ssid(url, sessionid):
    endpoint = url + '/config.ssid.profile'
    header = {"content-type":"application/json", "cookie":"bauth=" + sessionid}
    response = requests.get(endpoint, headers=header, verify=False)
    response_json = response.json()['response']
    return(response_json)

def get_cam_type(ip):
    payload = {'action': 'getConfig', 'name': 'ChannelTitle'}
    user = 'admin'
    password = 'admin12345'
    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    cam_url = 'http://%s/cgi-bin/configManager.cgi?' % ip
    cam_resp = requests.get(cam_url, params=param, auth=HTTPDigestAuth(user, password), stream=False)
    cam_json = json.dumps(cam_resp.text)
    cam_list = cam_json.split('\\r\\n', 4)
    cam_list.remove('"')
    sorted_cam = []
    for i in cam_list:
        sorted_cam.append(i.split('=', 1)[1])
    return sorted_cam
    #for i in cam_list:
    #    print(i)
    #cam_list.append(cam_resp.text.rstrip())
    #for i in cam_list:
    #    print('This is line' + i)
    #print(json.dumps(cam_resp.text))

def get_geocode(lat, lon):
    key = '9C8OSEmL77jB3BJNkatauCGTA9O8u9BR'
    #Original url with metadata and intersection which we don't need it.
    #url = 'http://www.mapquestapi.com/geocoding/v1/reverse?key=%s&location=%s,%s&includeRoadMetadata=true&includeNearestIntersection=true' % (key, lat, lon)
    url = 'http://www.mapquestapi.com/geocoding/v1/reverse?key=%s&location=%s,%s' % (key, lat, lon)
    print(url)
    response = requests.get(url)
    response_json = response.json()
    return(response_json['results'][0]['locations'][0])

def write_dict_to_json(datasets, file_name):
    #Convert datasets dict to list json
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    rows_tojson = []
    for k,v in datasets.items():
        row_tojson = {
            'id': k,
            'ip': v['ip'],
            'lat': v['lat'],
            'lon': v['lon'],
            'address': v['address'],
            'cam1': v['cam1'], 
            'cam2': v['cam2'], 
            'cam3': v['cam3'], 
            'cam4': v['cam4'], 
            'systime':  cur_time
            }
        rows_tojson.append(row_tojson)
    with open(file_name, 'w') as gpsjsonfile:
        json.dump(rows_tojson, gpsjsonfile, indent=4)

def main():
    urllib3.disable_warnings()
    context = {}
    #ip_file = open('tesla_ips_2.txt')
    ip_file = open(sys.argv[1])
    file_name = sys.argv[2]
    ip_lines = ip_file.readlines()
    for line in ip_lines:
        ip = line.rstrip()
        cam_type = get_cam_type(ip)
        url = 'https://%s:8443/api' % ip
        sessionid = login(url)
        print(ip)
        responsejson = (get_gps(url, sessionid))
        #print(responsejson)
        #print('lat: ' + str(responsejson['latitude']) + 'lon: ' + str(responsejson['longitude']))
        lat = str(responsejson['latitude'])
        lon = str(responsejson['longitude'])
        responsejson = get_geocode(responsejson['latitude'], responsejson['longitude'])
        #print(responsejson)
        address = responsejson['street'] + ', ' + responsejson['adminArea5'] + ' ' + responsejson['adminArea3'] + ' ' + responsejson['postalCode']
        responsejson = get_ssid(url, sessionid)
        #print(responsejson)
        ssid = responsejson['1']['name']
        context.update({ssid[-4:]: {'ip': ip, 'lat': lat, 'lon': lon, 'address': address, 'cam1': cam_type[0], 'cam2': cam_type[1], 'cam3': cam_type[2], 'cam4': cam_type[3]}})
        logout(url, sessionid)
    write_dict_to_json(context, file_name)

if __name__ == '__main__':
    main()
