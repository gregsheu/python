import cv2
import numpy as np
import simpleaudio as sa
import urllib3
from queue import Queue
from requests.auth import HTTPDigestAuth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from apiclient import errors
from logging.handlers import RotatingFileHandler
import socket
import pickle, os.path, base64, mimetypes, requests, urllib, time, threading, os, json, ffmpeg, logging

def write_to_json(trailer_id, myip, gpsdata):
    gps_json = []
    row_tojson = {
        'id': trailer_id,
        'status': 'green',
        'ip': myip, 
        'lat': '%s' % gpsdata['latitude'],
        'lon': '%s' % gpsdata['longitude'],
        'speed': '%s' % gpsdata['speed'],
        'systime': gpsdata['timestamp']
    }
    gps_json.append(row_tojson)
    with open('/tmp/gps.json', 'w') as gps:
        json.dump(gps_json, gps, indent=4)

def login(url):
    endpoint = url + '/login'
    payload = {"username":"admin", "password":"admin12345"}
    header = {"content-type":"application/json"}
    session = requests.Session()
    #response = session.post(endpoint, data=json.dumps(payload), headers=header)
    response = session.post(endpoint, data=json.dumps(payload), headers=header, verify=False)
    cookies = response.cookies.get_dict()
    #From 8080
    #sessionid = cookies["pauth"]
    #From 8443
    sessionid = cookies["bauth"]
    return sessionid

def logout(url, sessionid):
    endpoint = url + '/logout'
    header = {"content-type":"application/json", "cookie":"bauth=" + sessionid}
    #response = requests.post(endpoint, headers=header)
    response = requests.post(endpoint, headers=header, verify=False)

def get_gps(url, sessionid):
    endpoint = url + '/info.location'
    header = {"content-type":"application/json", "cookie":"bauth=" + sessionid}
    #response = requests.get(endpoint, headers=header)
    response = requests.get(endpoint, headers=header, verify=False)
    response_json = response.json()['response']
    return response_json['location']

def load_gps_json(gps_data):
    ip = None
    lat = None
    lon = None
    datasets = {}
    with open(gps_data, 'r') as f:
        datasets = json.loads(f.read())
    for i in datasets:
        #print('%(ip)s %(lat)s %(lon)s' % i)
        trailer_id = '%(id)s' % i
        ip = '%(ip)s' % i
        lat = '%(lat)s' % i
        lon = '%(lon)s' % i
    return {'id': trailer_id, 'ip': ip, 'lat': lat, 'lon': lon}

def goscopes():
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/gmail.send']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/var/task/kingsolarman66.pickle'):
        with open('/var/task/kingsolarman66.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('/var/task/kingsolarman66.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/var/task/kingsolarman66.pickle', 'wb') as token:
            pickle.dump(creds, token)
    gmail_service = build('gmail', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    return gmail_service, drive_service

def create_folder(drive_service, folder_name, parent_id):
    if parent_id:
        file_metadata = {
            'name': '%s' % folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
    else:
        file_metadata = {
            'name': '%s' % folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

    file = drive_service.files().create(body=file_metadata, fields='id').execute()
    #print('Folder ID: %s' % file.get('id'))
    return file.get('id')

def file_structures(drive_service):
    #Set up folder topology on google drive
    top_parent_folder = 'Tesla'
    top_parent_id = None
    resp = requests.get('http://jsonip.com')
    myip = resp.json()['ip']
    second_parent_folder = myip
    second_parent_id = None
    date_dir = time.strftime('%Y-%m-%d')
    third_parent_folder = date_dir
    third_parent_id = None
    items = list_tw_folder(drive_service, top_parent_folder, second_parent_folder)
    #print(len(items))
    #print(items)
    if len(items) == 1:
        if items[0]['name'] == top_parent_folder:
            top_parent_id = items[0]['id']
            #print(u'{0} ({1})'.format(item['name'], item['id']))
    items = list_2nd_folder(drive_service, top_parent_id, second_parent_folder)
    if len(items) == 1:
        second_parent_id = items[0]['id']
        #print(u'{0} ({1})'.format(item['name'], item['id']))
    else:
        #top_parent_id =  create_folder(drive_service, 'Onview', None)
        second_parent_id = create_folder(drive_service, myip, top_parent_id)
    items = list_date_folder(drive_service, second_parent_id, date_dir)
    if len(items) == 1:
        for item in items:
            if item['name'] == third_parent_folder:
                third_parent_id = item['id']
    else:
        third_parent_id = create_folder(drive_service, date_dir, second_parent_id)
    time.sleep(1)
    return third_parent_id, third_parent_folder

def callback(request_id, response, exception):
    if exception:
        # Handle error
        print(exception)
    else:
        print("Permission Id: %s" % response.get('id'))

def list_tw_folder(drive_service, drive_name, ip):
    results = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder' and name='%s' and trashed=false" % (drive_name), pageSize=30, spaces='drive', fields="nextPageToken, files(id, name, parents)").execute()
    items = results.get('files', [])
    return items

def list_2nd_folder(drive_service, parents, ip):
    results = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder' and name='%s' and parents in '%s' and trashed=false" % (ip, parents), pageSize=30, spaces='drive', fields="nextPageToken, files(id, name, parents)").execute()
    items = results.get('files', [])
    return items

def list_date_folder(drive_service, parents, date_dir):
    results = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder' and name='%s' and parents in '%s' and trashed=false" % (date_dir, parents), pageSize=30, spaces='drive', fields="nextPageToken, files(id, name, parents)").execute()
    items = results.get('files', [])
    return items

def get_file_link(drive_service, file_id):
    results = drive_service.files().list(pageSize=30, fields="nextPageToken, files(id, name, webViewLink)").execute()
    items = results.get('files', [])
    return items[0]['webViewLink']

def share_file_link(drive_service, file_id):
    batch = drive_service.new_batch_http_request(callback=callback)
    #For sharing anyone with link
    user_permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    batch.add(drive_service.permissions().create(fileId=file_id, body=user_permission, fields='id',))
    batch.execute()

def upload_file_to_folder(drive_service, folder_id, filename):
    #The filename is date_dir/filename
    file_metadata = {
        'name': '%s' % filename[11:],
        'parents': [folder_id]
    }
    #Let's check the file type
    if filename[-3:] == 'jpg':
        mimetype = 'image/jpeg'
    elif filename[-3:] == 'mp4':
        mimetype = 'video/mp4'
    media = MediaFileUpload('%s' % filename, mimetype=mimetype, chunksize=1024*1024, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    #print('File ID: %s' % file.get('id'))
    return file.get('id')

def gdrive(drive_service, third_parent_id, filename):
    file_id = upload_file_to_folder(drive_service, third_parent_id, filename)
    share_file_link(drive_service, file_id)
    webviewlink = get_file_link(drive_service, file_id)
    return webviewlink

def create_gmail(sender, to, cc, subject, message_text):
    """Create a message for an email.
    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to + ',' + cc
    message['from'] = sender
    message['subject'] = subject
    return base64.urlsafe_b64encode(message.as_bytes())

def send_gmail(service, user_id, message_body):
    """Send an email message.
    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.
    Returns:
      Sent Message.
    """
    try:
        message = message_body.decode()
        messages = {'raw': message}
        sent_message = (service.users().messages().send(userId=user_id, body=messages).execute())
        #print('Message %s ' % (sent_message))
        return sent_message
    except errors.HttpError as error:
        print('An error occurred %s' % error)

def gmail(gmail_service, webviewlink, plate):
    sender = os.getenv('SENDER')
    to = os.getenv('To')
    cc = os.getenv('Cc')
    if cc:
        cc = cc
    gps_data = '/tmp/gps.json'
    trailer_infos = {}
    trailer_infos = load_gps_json(gps_data)
    trailer_infos.update({'link': webviewlink})
    trailer_infos.update({'plate': plate})
    ## If modifying these scopes, delete the file token.pickle.
    subject = 'King Solarman Inc. Car Plate Recognition! for %s' % trailer_infos['id']
    #message = 'This is test'
    message = "Our car plate recoginition system (Trailer %(id)s IP %(ip)s) detects car plate %(plate)s at https://www.google.com/maps?q=%(lat)s,%(lon)s . Please log on here to view the snapshots %(link)s" % trailer_infos
    email_message = create_gmail(sender, to, cc, subject, message)
    send_gmail(gmail_service, 'kingsolarman66@gmail.com', email_message)

def events(cam_ip):
    #Set up goapi scopes
    socket.setdefaulttimeout(3600)
    gmail_service, drive_service = goscopes()
    third_parent_id, third_parent_folder = file_structures(drive_service)
    #IPC event
    #snap_url = 'http://%s:8888/cgi-bin/snapManager.cgi?action=attachFileProc&Flags[0]=Event&Events=[All]&heartbeat=5' % cam_ip
    snap_url = 'http://%s/cgi-bin/snapManager.cgi?action=attachFileProc&Flags[0]=Event&Events=[All]&heartbeat=5&channel=1' % cam_ip
    user = 'admin'
    password = 'admin12345'
    channel = 1
    payload = {'channel': channel}
    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    with requests.get(snap_url, params=param, auth=HTTPDigestAuth(user, password), stream=True) as resp:
        bytes = b'' 
        for chunk in resp.iter_content(chunk_size=1024):
            cur_time = time.time()
            #eventstart = time.strftime('%H:%M:%S', time.localtime(cur_time))
            eventstart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
            newtime = eventstart.replace(' ', '')
            newtime = newtime.replace(':', '')
            date_dir = eventstart[0:eventstart.index(' ')]
            filename =  'plate-%s-%s.jpg' % (str(channel)+cam_ip.split('.')[-1], newtime)
            #if third_parent_folder != date_dir:
            #    third_parent_id, third_parent_folder = file_structures(drive_service)
            #if '2022-02-08' in str(chunk):
            #    print(chunk)
            #    with open('plate.txt', 'a+') as f:
            #        f.write(str(chunk))
            bytes += chunk
            finda = bytes.find(b'\xff\xd8')
            findb = bytes.find(b'\xff\xd9')
            findc = b'\x17"$"\x1e$\x1c\x1e\x1f\x1e\xff\xfe\x07\xfe\x01\x10\x00\xee\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'
            lenc = len(findc)
            #if findc != -1:
            #    plate = bytes[findc+lenc:findc+lenc+7]
            #    print('This is plate %s' % plate)
            if finda != -1 and findb != -1:
                jpg = bytes[finda:findb+2]
                bytes = bytes[findb+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                time.sleep(1)
                #if frame is not None:
                #    cv2.imwrite(filename, frame)
                #    webviewlink = gdrive(drive_service, third_parent_id, filename)
                #findc = jpg.find(findc)
                #if findc != -1:
                #    plate = jpg[findc+lenc:findc+lenc+12]
                #    plate = str(plate)[2:str(plate).index('\\x00')]
                #    print('This is plate %s' % plate)
                #    if plate == '':
                #        plate = 'No Plate'
                #    gmail(gmail_service, webviewlink, plate)

def main():
    urllib3.disable_warnings()
    #trailer_id = os.getenv('HOST')
    #Preparation of GPS
    #resp = requests.get('http://jsonip.com')
    #myip = resp.json()['ip']
    #url = "http://192.168.1.1:8080/api"
    #url = "http://:8080/api"
    #url = "https://166.193.32.142:8443/api"
    #sessionid = login(url)
    #gpsdata = get_gps(url, sessionid)
    #write_to_json(trailer_id, myip, gpsdata)
    #logout(url, sessionid)

    cam1_ip = os.getenv('CAM1')
    t1 = threading.Thread(target=events, args=(cam1_ip,))
    t1.start()
    t1.join()

if __name__ == '__main__':
    main()
