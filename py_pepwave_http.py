import os
import json
import requests
import sys
import time
import urllib3

def login(url):
    endpoint = url + '/login'
    payload = {"username":"admin", "password":"admin12345"}
    header = {"content-type":"application/json"}
    session = requests.Session()
    response = session.post(endpoint, data=json.dumps(payload), headers=header, verify=False)
    cookies = response.cookies.get_dict()
    sessionid = cookies["pauth"]
    return sessionid

def logout(url, sessionid):
    endpoint = url + '/logout'
    header = {"content-type":"application/json", "cookie":"pauth=" + sessionid}
    response = requests.post(endpoint, headers=header, verify=False)

def get_wan(url, sessionid):
    endpoint = url + '/status.wan.connection'
    header = {"content-type":"application/json", "cookie":"pauth=" + sessionid}
    response = requests.get(endpoint, headers=header, verify=False)
    response_json = response.json()['response']
    return(response_json)

def get_gps(url, sessionid):
    endpoint = url + '/info.location'
    header = {"content-type":"application/json", "cookie":"pauth=" + sessionid}
    response = requests.get(endpoint, headers=header, verify=False)
    response_json = response.json()['response']
    return response_json['location']

def get_client(url, sessionid):
    endpoint = url + '/status.client'
    header = {"content-type":"application/json", "cookie":"pauth=" + sessionid}
    client_list = []
    response = requests.get(endpoint, headers=header)
    response_json = response.json()['response']
    for i in response_json.values():
        client_list += i
    for i in client_list:
        if i['active']:
            print(i['ip'] + ' ' + i['connectionType'] + ' active: true')
    return(client_list)

def get_bandwidth(url, sessionid):
    endpoint = url + '/status.wan.connection.allowance'
    header = {"content-type":"application/json", "cookie":"pauth=" + sessionid}
    response = requests.get(endpoint, headers=header, verify=False)
    response_json = response.json()['response']
    return(response_json)

def post_sms(url, sessionid):
    endpoint = url + '/cmd.sms.sendMessage'
    payload = {"address":"+19516661052", "content":"Alert Tripwires"}
    header = {"content-type":"application/json", "cookie":"pauth=" + sessionid}
    response = requests.post(endpoint, data=json.dumps(payload), headers=header, verify=False)
    response_json = response.json()
    return(response_json)

def get_sms(url, sessionid):
    endpoint = url + '/cmd.sms.get?connId=2'
    header = {"content-type":"application/json", "cookie":"pauth=" + sessionid}
    response = requests.post(endpoint, headers=header, verify=False)
    response_json = response.json()
    return(response_json)

def main():
    urllib3.disable_warnings()
    ip = sys.argv[1]
    url = 'http://%s:8080/api' % ip
    sessionid = login(url)
    responsejson = (get_sms(url, sessionid))
    print(responsejson)
    responsejson = (post_sms(url, sessionid))
    print(responsejson)
    #responsejson = (get_wan(url, sessionid))
    #print(responsejson['2']['ip'] + ' ' + responsejson['2']['statusLed'] + ' ' + responsejson['2']['cellular']['sim']['1']['status'] + ' ' + responsejson['2']['cellular']['sim']['1']['mtn'])
    responsejson = (get_bandwidth(url, sessionid))
    print(responsejson)
    #responsejson = (get_gps(url, sessionid))
    #print(responsejson)
    responsejson = (get_client(url, sessionid))
    print(responsejson)
    logout(url, sessionid)

if __name__ == '__main__':
    main()
