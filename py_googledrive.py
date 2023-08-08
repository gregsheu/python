from __future__ import print_function
import pickle
import os.path
import time
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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
    media = MediaFileUpload('/tmp/%s' % filename, mimetype='image/jpeg')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('File ID: %s' % file.get('id'))
    return file.get('id')

def upload_file(drive_service, filename):
    #This upload file to under My Drive, not parent folder
    file_metadata = {'name': '%s' % filename}
    #media = MediaFileUpload('/tmp/4.jpg', mimetype='image/jpeg')
    media = MediaFileUpload('/tmp/%s' % filename) 
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

def main():
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
                'Downloads/kingsolarman77.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('kingsolarman77drive.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    items = list_files(service)
    top_parent_folder = 'Onview'
    top_parent_id = None
    resp = requests.get('http://jsonip.com')
    myip = resp.json()['ip']
    second_parent_folder = myip
    second_parent_id = None
    cur_time = time.time()
    eventstart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
    date_dir = eventstart[0:eventstart.index(' ')]
    third_parent_folder = date_dir
    third_parent_id = None
    for item in items:
        if item['name'] == top_parent_folder:
            top_parent_id = item['id']
            print(u'{0} ({1})'.format(item['name'], item['id']))
        if item['name'] == second_parent_folder:
            second_parent_id = item['id']
            print(u'{0} ({1})'.format(item['name'], item['id']))
        if item['name'] == third_parent_folder:
            third_parent_id = item['id']
            print(u'{0} ({1})'.format(item['name'], item['id']))

    if top_parent_id:
        if second_parent_id:
            if third_parent_id:
                ...
            else:
                third_parent_id = create_folder(service, date_dir, second_parent_id)
        else:
            second_parent_id = create_folder(service, myip, top_parent_id)
    else:
        top_parent_id =  create_folder(service, 'Onview', None)
    filename = 'fw-max_br1_br2-8.0.2-build3612.bin'
    filename = 'nginx-1.19.6.tar.gz'
    filename = 'proscendspeedtest-2.png'
    filename = 'proscendspeedtest-5.png'
    file_id = upload_file_to_folder(service, third_parent_id, filename)
    email = 'kingsolarman66@gmail.com'
    share_file_with_email(service, file_id, email)
    email = 'greg@king-solarman.com'
    share_file_with_email(service, file_id, email)
    share_file_link(service, file_id)
    share_file_link(service, file_id)
    weblink = get_file_link(service, file_id)
    print(weblink)
    file_id = upload_file(service, filename)
    share_file_with_email(service, file_id, email)
    share_file_link(service, file_id)

if __name__ == '__main__':
    main()
