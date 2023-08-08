import subprocess
import json
import sys
import time
import requests
from kubernetes import client, config

def get_helm(app_name):
    print('helm get values -n prod --all %s -o json > %s-platblue-helm.json' % (app_name, app_name))
    sub_return = subprocess.run(['helm', 'get',  'values', '-n', 'prod', '--all', app_name, '-o', 'json'], capture_output=True)
    json_object=json.loads(sub_return.stdout)
    with open('%s-platblue-helm.json' % app_name, 'w') as f:
        f.write(json.dumps(json_object, indent=4))
    with open('%s.json' % app_name, 'w') as f:
        f.write(json.dumps(json_object, indent=4))

def get_deploy(app_name):
    print(app_name)
    print('Get %s release and env from platinum blue\'s running pod!!' % app_name)
    app_name_list = []
    env = []
    spring = {}
    k8s_c = client.AppsV1Api()
    resp = k8s_c.read_namespaced_deployment(namespace='prod', name=app_name)
    api_client = client.ApiClient()
    resp = api_client.sanitize_for_serialization(resp) #BINGO!
    for i in resp['spec']['template']['spec']['containers']:
        if app_name in i['name']:
            app_name_list.append(i['name'])
            app_name_list.append(i['image'])
            app_name_list.append(i['env'])
    for i in app_name_list[2]:
        if i['name'] == 'SPRING_PROFILES_ACTIVE':
            print('We need to preserve the SPRING_PROFILES_ACTIVE from running pod!!')
            index = app_name_list[2].index(i)
            spring = app_name_list[2].pop(index)
            print('Platinum blue running pod %s' % spring)
        if i['name'] == 'podName':
            index = app_name_list[2].index(i)
            print('Remove the podName')
            app_name_list[2].pop(index)
    for i in app_name_list[2]:
        if i['name'] == 'release_tag_name':
            index = app_name_list[2].index(i)
            a = app_name_list[1]
            app_name_list[2][index]['value'] = a[a.index(':')+1:len(a)]
        for k, v in i.items():
            if 'eksprodblue' in str(v):
                print(v)
                index = app_name_list[2].index(i)
                app_name_list[2][index]['value'] = str(v).replace('eksprodblue','eksprodgreen')
            if 'platinum' in str(v):
                print(v)
                index = app_name_list[2].index(i)
                app_name_list[2][index]['value'] = str(v).replace('platinum','platgreen')
    if spring:
        print('We added SPRING_PROFILES_ACTIVE back!!')
        app_name_list[2].append(spring)
    else:
        print('SPRING_PROFILES_ACTIVE is only needed in Java!!')
    return app_name_list

def replace_blue(filename):
    #app_name = filename.strip('.json')
    app_name = filename[0:filename.index('.')]
    app_name_list = get_deploy(app_name)
    print('Search and replace platinum to platgreen, eksprodblue to eksprodgreen!!')
    readall = None
    replace = None
    orig_dict = {} 
    dict = {}
    with open(filename, 'r') as f:
        readall = f.read()
        replace = readall.replace('platinum', 'platgreen')
        replace = replace.replace('eksprodblue', 'eksprodgreen')
    #with open(filename, 'w') as f:
    #    f.write(readall)
    #with open(filename, 'r') as f:
    #    dict = json.loads(f.read())
    orig_dict = json.loads(readall)
    dict = json.loads(replace)
    for i in dict['env']:
        if i['name'] == 'SPRING_PROFILES_ACTIVE':
            print('Get SPRING_PROFILES_ACTIVE from platinum blue helm!!')
            index = dict['env'].index(i)
            orig_value = orig_dict['env'][index]
            print('Platinum blue helm SPRING_PROFILES_ACTIVE %s' % orig_value)
            dict['env'][index] = orig_value
    print('Let\'s update release-master platinum blue\'s!!')
    dict['image']['repository'] = app_name_list[1]
    print('Let\'s repleace env with platinum blue\'s!!')
    dict.update({'env': app_name_list[2]})
    print(dict['env'])
    print('Let\'s dedup release_tag_name!!')
    dedup = []
    [dedup.append(x) for x in dict['env'] if x not in dedup]
    #print(dict['env'])
    print('Let\'s update back to json!!')
    dict.update({'env': dedup})
    with open(filename, 'w') as f:
        f.write(json.dumps(dict, indent=4))
    print('We are done editing json file!!')

def post_deploy(url, filename, tplt):
    print('Let\'s do it, the deployment!!')
    body = {}
    endpoint = url
    header = {"Content-Type": "application/json", "templatename": "%s" % tplt}
    with open(filename, 'r') as f:
        body = json.loads(f.read())
    print(body)
    response = requests.post(endpoint, data=json.dumps(body), headers=header)
    print(response.text)
    time.sleep(1)
    print('Awesome, we made it')

def main():
    tplt = None
    if len(sys.argv) == 1 or len(sys.argv) == 2:
        print('This is how to run this script: \npython update_platgreen.py -p python_app_name, \npython update_platgreen.py -j java_app_name, \npython update_platgreen.py -n nodejs_app_name, \npython update_platgreen.py -r reactjs_app_name; \nTo update multilple apps, separate with comma without space,ie,\npython update_platgreen.py -j java1,java2,java3,java4')
        exit(0) 
    if sys.argv[1] == '-p':
        tplt = 'pythonsvcWithIngress'
    elif sys.argv[1] == '-j':
        tplt = 'soasvcWithIngress'
    elif sys.argv[1] == '-n':
        tplt = 'nodejssvcWithIngress'
    elif sys.argv[1] == '-r':
        tplt = 'reactjssvcWithIngress'
    elif sys.argv[1] == '-g':
        tplt = 'goLangsvcWithIngress'
    else:
        exit(0)
    if tplt:
        print(tplt)
    config.load_kube_config()
    app_name_list = sys.argv[2].split(',')
    for app_name in app_name_list:
        filename = '%s.json' % app_name
        print('Let\'s start %s!!' % filename)
        get_helm(app_name)
        time.sleep(10)
        replace_blue(filename)
        time.sleep(5)
        url = 'https://ehds.elevancehealth.com/tenxeng/platgreen/container/utl/genscrexec/helmdeploy'
        post_deploy(url, filename, tplt)

if __name__ == '__main__':
    main()
