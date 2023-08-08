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
import simpleaudio as sa

def setlogger():
    #logger = logging.basicConfig(filename='system.log', format='%(asctime)s %(message)s', datefmt=str(cur_time))
    logger = logging.getLogger('logme')
    handler = RotatingFileHandler('/tmp/py_event.log', maxBytes=2048000, backupCount=5)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

def logme(message):
    cur_time = time.strftime('%b %e %H:%M:%S', time.localtime())
    logger = logging.getLogger('logme')
    logger.info('%s %s' % (cur_time, message))

#Remember to put dir under /tmp in future
def get_snap(ip, channel, eventstart, user, password):
    payload = {'channel': channel}
    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    snap_url = 'http://%s/cgi-bin/snapshot.cgi?' % ip
    snap_resp = requests.get(snap_url, params=param, auth=HTTPDigestAuth(user, password), stream=True)
    newtime = eventstart.replace(' ', '')
    newtime = newtime.replace(':', '')
    filename =  'tripsnap-%s-%s.jpg' % (str(channel)+ip.split('.')[-1], newtime)
    date_dir = eventstart[0:eventstart.index(' ')]
    if os.path.exists('snap/%s' % date_dir):
        pass
    else:
        os.mkdir('snap/%s' % date_dir)
        os.chmod('snap/%s' % date_dir, 0o1777)
    with open('snap/%s/tripsnap-%s-%s.jpg' % (date_dir, str(channel)+ip.split('.')[-1], newtime), 'wb') as f:
        f.write(snap_resp.content)
    os.chmod('snap/%s/tripsnap-%s-%s.jpg' % (date_dir, str(channel)+ip.split('.')[-1], newtime), 0o1777)
    #return 'tripsnap-%s-%s.jpg' % (str(channel)+ip.split('.')[-1], newtime)
    return '%s/%s' % (date_dir, filename)
    #return '%s' % filename

def get_video(ip, channel, eventstart, eventend):
    newtime = eventstart.replace(' ', '')
    newtime = newtime.replace(':', '')
    date_dir = eventstart[0:eventstart.index(' ')]
    if os.path.exists('/tmp/%s' % date_dir):
        pass
    else:
        os.mkdir('/tmp/%s' % date_dir)
        os.chmod('/tmp/%s' % date_dir, 0o1777)
    filename =  'tripvideo-%s-%s.mp4' % (str(channel)+ip.split('.')[-1], newtime)
    video_url = 'rtsp://admin:admin12345@%s:554/cam/realmonitor?channel=%s&subtype=0' % (ip, channel)
    r = ffmpeg.input('%s' % video_url)
    (
        ffmpeg
        .output(r, '/tmp/%s/tripvideo-%s-%s.mp4' % (date_dir, str(channel)+ip.split('.')[-1], newtime), ss=0, t=5, r=5, vb='512k', vcodec='libx264', maxrate='512k', bufsize='1024k', g=2, pix_fmt='yuvj420p')
        #.output(r, '/tmp/%s/tripvideo-%s-%s.mp4' % (date_dir, str(channel)+ip.split('.')[-1], newtime), ss=0, t=15, vsync='passthrough', vcodec='libx264')
        .overwrite_output()
        #.run(cmd='/usr/local/bin/ffmpeg')
        .run()
    )
    os.chmod('/tmp/%s/tripvideo-%s-%s.mp4' % (date_dir, str(channel)+ip.split('.')[-1], newtime), 0o1777)
    #return 'tripvideo-%s-%s.mp4' % (str(channel)+ip.split('.')[-1], newtime)
    return '%s/%s' % (date_dir, filename)
    #return '%s' % filename

def convert_dav(ip, channel, eventstart, eventend):
    newtime = eventstart.replace(' ', '')
    newtime = newtime.replace(':', '')
    date_dir = eventstart[0:eventstart.index(' ')]
    if os.path.exists('/tmp/%s' % date_dir):
        pass
    else:
        os.mkdir('/tmp/%s' % date_dir)
        os.chmod('/tmp/%s' % date_dir, 0o1777)
    filename =  'tripvideo-%s-%s.mp4' % (str(channel)+ip.split('.')[-1], newtime)
    payload = {'action': 'startLoad', 'channel': channel, 'startTime': eventstart, 'endTime': eventend, 'subtype': '0'}
    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    video_url = 'http://%s/cgi-bin/loadfile.cgi?' % ip
    user = 'admin'
    password = 'admin12345'
    video_resp = requests.get(video_url, params=param, auth=HTTPDigestAuth(user, password), stream=True)
    with open('/tmp/%s/tripvideo-%s-%s.dav' % (date_dir, str(channel)+ip.split('.')[-1], newtime), 'wb') as f:
        f.write(video_resp.content)
    r = ffmpeg.input('/tmp/%s/tripvideo-%s-%s.dav' % (date_dir, str(channel)+ip.split('.')[-1], newtime))
    (
        ffmpeg
        .output(r, '/tmp/%s/tripvideo-%s-%s.mp4' % (date_dir, str(channel)+ip.split('.')[-1], newtime), vcodec='libx264', format='mp4')
        .overwrite_output()
        .run()
    )
    return '%s/%s' % (date_dir, filename)

def stitch_video(in1, in2, in3, in4, eventstart, eventend):
    newtime = eventstart.replace(' ', '')
    newtime = newtime.replace(':', '')
    date_dir = eventstart[0:eventstart.index(' ')]
    filename = 'tripvideo-%s-%s.mp4' % (str('4all')+'192.168.1.108'.split('.')[-1], newtime)
    v1 = ffmpeg.input(in1)
    v2 = ffmpeg.input(in2)
    v3 = ffmpeg.input(in3)
    v4 = ffmpeg.input(in4)
    (
        ffmpeg
        .concat(
            v1,
            v2,
        )
        .filter('scale', '1920', '1080')
        .filter('setsar', sar=1/1)
        .output('/tmp/%s/tripvideo-%s-%s-ipc.mp4' % (date_dir, str('4all')+'192.168.1.108'.split('.')[-1], newtime), r=25)
        .overwrite_output()
        .run()
    )
    (
        ffmpeg
        .concat(
            v1,
            v2,
        )
        .filter('scale', '1920', '1080')
        .filter('setsar', sar=1/1)
        .output('/tmp/%s/tripvideo-%s-%s-ptz.mp4' % (date_dir, str('4all')+'192.168.1.108'.split('.')[-1], newtime), r=25)
        .overwrite_output()
        .run()
    )
    return '%s/%s' % (date_dir, filename)

def alarm_sound(alarm):
    wave_obj = sa.WaveObject.from_wave_file(alarm)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing

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

#Below functions are google drive and gmail api
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
    media = MediaFileUpload('/tmp/%s' % filename, mimetype=mimetype, chunksize=1024*1024, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    #print('File ID: %s' % file.get('id'))
    return file.get('id')

def upload_file(drive_service, filename):
    #This upload file to under My Drive, not parent folder
    file_metadata = {'name': '%s' % filename[11:]}
    #media = MediaFileUpload('/tmp/4.jpg', mimetype='image/jpeg')
    media = MediaFileUpload('/tmp/%s' % filename, chunksize=1024*1024, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    #print('File ID: %s' % file.get('id'))
    return file.get('id')

def list_files(drive_service):
    results = drive_service.files().list(pageSize=30, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items

def list_folders(drive_service):
    results = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'", pageSize=30, spaces='drive', fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items

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

def callback(request_id, response, exception):
    if exception:
        # Handle error
        print(exception)
    else:
        print("Permission Id: %s" % response.get('id'))

def share_file_with_email(drive_service, file_id, email):
    batch = drive_service.new_batch_http_request(callback=callback)
    #For sharing with specific user with email
    user_permission = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': '%s' % email
    }
    batch.add(drive_service.permissions().create(fileId=file_id, body=user_permission, fields='id',))
    batch.execute()

def share_file_with_domain(drive_service, file_id, domain):
    batch = drive_service.new_batch_http_request(callback=callback)
    #For sharing with domain name
    domain_permission = {
        'type': 'domain',
        'role': 'reader',
        'domain': '%s' % domain
    }
    batch.add(drive_service.permissions().create(
            fileId=file_id,
            body=domain_permission,
            fields='id',
    ))
    batch.execute()

def share_file_link(drive_service, file_id):
    batch = drive_service.new_batch_http_request(callback=callback)
    #For sharing anyone with link
    user_permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    batch.add(drive_service.permissions().create(fileId=file_id, body=user_permission, fields='id',))
    batch.execute()

#Add gmail oauth instead of early smtplib that will gets blocked by gmail smtp interface
#create_gmail_with attachment create_gmail send_gmail are gmail oauth
def create_gmail_with_attachment(sender, to, cc, subject, message_text, file):
    """Create a message for an email.
    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        file: The path to the file to be attached.
    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['to'] = to + ',' + cc
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)
    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(file, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(file, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(file, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
    #return {'raw': base64.urlsafe_b64encode(message.as_string())}
    return base64.urlsafe_b64encode(message.as_bytes())

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

def gmail(gmail_service, webviewlink):
    sender = os.getenv('SENDER')
    to = os.getenv('To')
    cc = os.getenv('Cc')
    if cc :
        cc = cc
    gps_data = '/tmp/gps.json'
    trailer_infos = {}
    trailer_infos = load_gps_json(gps_data)
    trailer_infos.update({'link': webviewlink})
    ## If modifying these scopes, delete the file token.pickle.
    subject = 'King Solarman Inc. Tripwire Alert! for Onview'
    #message = 'This is test'
    message = "Our surveillance system (Trailer %(id)s IP %(ip)s) detects suspicious intrusion activities on site at https://www.google.com/maps?q=%(lat)s,%(lon)s . Please log on here to view the snapshots and videos %(link)s" % trailer_infos
    email_message = create_gmail(sender, to, cc, subject, message)
    send_gmail(gmail_service, 'kingsolarman77@gmail.com', email_message)

def gmail_scopes():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/var/task/kingsolarman77.pickle'):
        with open('/var/task/kingsolarman77.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('/var/task/kingsolarman77.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/var/task/kingsolarman77.pickle', 'wb') as token:
            pickle.dump(creds, token)
    gmail_service = build('gmail', 'v1', credentials=creds)
    return gmail_service

def gdrive(drive_service, third_parent_id, filename):
    file_id = upload_file_to_folder(drive_service, third_parent_id, filename)
    logme('Upload file %s' % filename)
    share_file_link(drive_service, file_id)
    webviewlink = get_file_link(drive_service, file_id)
    logme('File shared %s' % webviewlink)
    return webviewlink

def drive_scopes():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    if os.path.exists('/var/task/kingsolarman77.pickle'):
        with open('/var/task/kingsolarman77.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('/var/task/kingsolarman77.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/var/task/kingsolarman77.pickle', 'wb') as token:
            pickle.dump(creds, token)
    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

def file_structures(drive_service):
    #Set up folder topology on google drive
    top_parent_folder = 'Onview'
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
    return third_parent_id

def goscopes():
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/gmail.send']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/var/task/kingsolarman77.pickle'):
        with open('/var/task/kingsolarman77.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('/var/task/kingsolarman77.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/var/task/kingsolarman77.pickle', 'wb') as token:
            pickle.dump(creds, token)
    gmail_service = build('gmail', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    return gmail_service, drive_service

def events(cam_ip, cam2_ip, *args):
    #cam_ip = '192.168.1.108'
    cam_ip = 'tesla-1'
    #Play sound when Tripwire happens
    user = 'admin'
    password = 'admin123456'
    while True:
        cur_time = time.time()
        eventstart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
        eventend = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time+5))
        filename1 = get_snap(cam_ip, 1, eventstart, user, password)
        filename2 = get_snap(cam_ip, 2, eventstart, user, password)
        filename3 = get_snap(cam_ip, 3, eventstart, user, password)
        filename4 = get_snap(cam_ip, 4, eventstart, user, password)
        time.sleep(0.002)

def main():
    #Set up goapi scopes
    socket.setdefaulttimeout(3600)
    cam_ip = 'tesla-1'
    t1 = threading.Thread(target=events, args=(cam_ip, cam_ip))
    t1.start()

if __name__ == '__main__':
    main()
