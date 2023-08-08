from __future__ import print_function
import pickle
import os.path
import time
import requests
import mimetypes
import base64
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from apiclient import errors, discovery

##
# google drive
##
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
    print('Folder ID: %s' % file.get('id'))
    return file.get('id')

def upload_file_to_folder(drive_service, folder_id, filename):
    #folder_id = '0BwwA4oUTeiV1TGRPeTVjaWRDY1E'
    file_metadata = {
        'name': '%s' % filename,
        'parents': [folder_id]
    }
    media = MediaFileUpload('%s' % filename, mimetype='image/jpeg')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('File ID: %s' % file.get('id'))
    return file.get('id')

def upload_file(drive_service, filename):
    #This upload file to under My Drive, not parent folder
    file_metadata = {'name': '%s' % filename}
    #media = MediaFileUpload('/tmp/4.jpg', mimetype='image/jpeg')
    media = MediaFileUpload('%s' % filename) 
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('File ID: %s' % file.get('id'))
    return file.get('id') 

def list_files(drive_service):
    results = drive_service.files().list(pageSize=30, fields="nextPageToken, files(id, name)").execute()
    #print(results)
    items = results.get('files', [])
    return items 

def get_file_link(drive_service, file_id):
    results = drive_service.files().list(pageSize=30, fields="nextPageToken, files(id, name, webViewLink)").execute()
    #print(results)
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
##
# gmail
##
def create_message_with_attachment(sender, to, cc, subject, message_text, file):
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

def create_message_with_attachments(sender, to, cc, subject, message_text, files):
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

    #attempting multiple files
    for file_path in files or []:
        with open(file_path, "rb") as fp:
            msg = MIMEBase('application', "octet-stream")
            msg.set_payload((fp).read())
            # Encoding payload is necessary if encoded (compressed) file has to be attached.
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(file_path))
            #message.attach(part)
            msg.add_header('Content-Disposition', 'attachment', filename=file_path)
            message.attach(msg)
    return base64.urlsafe_b64encode(message.as_bytes())

def create_message(sender, to, cc, subject, message_text):
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

def send_message(service, user_id, message_body):
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
        print('Message %s ' % (sent_message))
        return sent_message
    except errors.HttpError as error:
        print('An error occurred %s' % error)

def drive_scopes():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    # If modifying these scopes, delete the file token.pickle.
    #SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('kingsolarman77drive.pickle'):
        with open('kingsolarman77drive.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'kingsolarman77.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('kingsolarman77drive.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

def gmail_scopes():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('kingsolarman77gmail.pickle'):
        with open('kingsolarman77gmail.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'kingsolarman77.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('kingsolarman77gmail.pickle', 'wb') as token:
            pickle.dump(creds, token)
    gmail_service = build('gmail', 'v1', credentials=creds)
    return gmail_service

def goapi():
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/gmail.send']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('kingsolarman77.pickle'):
        with open('kingsolarman77.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('kingsolarman77.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('kingsolarman77.pickle', 'wb') as token:
            pickle.dump(creds, token)
    gmail_service = build('gmail', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service, gmail_service

def main():
    #drive_service = drive_scopes()
    #gmail_service = gmail_scopes()
    drive_service, gmail_service = goapi()
    #top_parent_folder = 'Test'
    #folder_id = create_folder(drive_service, top_parent_folder, '')
    #filename = 'proscendspeedtest-5.png'
    #file_id = upload_file_to_folder(drive_service, folder_id, filename)
    #email = 'greg@king-solarman.com'
    #share_file_with_email(drive_service, file_id, email)
    #share_file_link(drive_service, file_id)
    #weblink = get_file_link(drive_service, file_id)
    #print(weblink)
    #file_id = upload_file(drive_service, filename)
    #share_file_link(drive_service, file_id)
    #weblink = get_file_link(drive_service, file_id)
    #print(weblink)
    sender = 'kingsolarman77@gmail.com'
    to = 'greg@king-solarman.com'
    cc = 'kingsolarman66@gmail.com,gregsheu@yahoo.com'
    subject = 'King Solarman Inc. Google drive sharing!'
    #message = weblink
    message = 'Multiple Files'
    #email_message = create_message(sender, to, cc, subject, message)
    #send_message(gmail_service, 'kingsolarman77@gmail.com', email_message)
    file_names = ['/tmp/4.jpg', '/tmp/alarm.wav', '/tmp/py_event.log', '/tmp/py_event_v1_goapi.log']
    email_message = create_message_with_attachments(sender, to, cc, subject, message, file_names)
    send_message(gmail_service, 'me', email_message)

if __name__ == '__main__':
    main()
