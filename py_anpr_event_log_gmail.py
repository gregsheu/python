from __future__ import print_function
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
import pickle, os.path, base64, mimetypes, requests, urllib, time, os

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

def create_gmail_with_attachments(sender, to, cc, subject, message_text, files):
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

def gmail(gmail_service, sender, to, cc, logfiles):
    ## If modifying these scopes, delete the file token.pickle.
    subject = 'King Solarman Inc. Car Plate Recognition Log'
    #message = 'This is test'
    message = "Log file for the last 24 hours detected car plates. Please check the attached file. Thank you."
    #email_message = create_gmail(sender, to, cc, subject, message)
    email_message = create_gmail_with_attachments(sender, to, cc, subject, message, logfiles)
    send_gmail(gmail_service, 'kingsolarman66@gmail.com', email_message)
    time.sleep(1)

def gmail_scopes():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
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
    return gmail_service

def main():
    sender = os.getenv('SENDER')
    to = os.getenv('To')
    cc = os.getenv('Cc')
    service = gmail_scopes()
    files = ['/tmp/carplate.html']
    gmail(service, sender, to, cc, files)
    with open('/tmp/carplate.html', 'w') as f:
        f.write('')

if __name__ == '__main__':
    main()
