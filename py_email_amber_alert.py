import email
import smtplib
import ssl
import json
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def load_gps_json(gps_data):
    ip = None
    lat = None
    lon = None
    datasets = {}
    with open(gps_data, 'r') as f:
        datasets = json.loads(f.read())
    for i in datasets:
        print('%(ip)s %(lat)s %(lon)s' % i)
        trailer_id = '%(id)s' % i
        ip = '%(ip)s' % i
        lat = '%(lat)s' % i
        lon = '%(lon)s' % i
    return (trailer_id, ip, lat, lon)

def send_email(sender, receiver, cc_receiver, trailer_infos):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    #receiver_email = "greg@king-solarman.com"
    #cc_receiver_email = ["hugo@king-solarman.com", "mike@king-solarman.com", "greg@king-solarman.com"]
    #cc_receiver_email = ["kingsolarman66@gmail.com"]
    cc_receiver.append(receiver)
    password = '4087280048'
    subject = "Tripwire Alerts from King Solarman Inc."
    body = "Our surveillance system (Trailer %s IP %s) sensors possible intrusion activities on site at https://www.google.com/maps?q=%s,%s. Please log on here to view the snapshots and videos %s" % trailer_infos
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = ','.join(cc_receiver)
    message["Subject"] = subject
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender, password)
        #server.sendmail(sender, receiver_email, text)
        server.send_message(message)

def main():
    amberlink = os.getenv('AMBERLINK')
    #sender = 'kingsolarman88@gmail.com'
    #receiver = 'greg@king-solarman.com'
    #cc_receiver = ['kingsolarman66@gmail.com']
    sender = os.getenv('SENDER')
    receiver = os.getenv('TO')
    cc_receiver = os.getenv('CC')
    if cc_receiver:
        cc_receiver = cc_receiver.split(',')
    gps_data = '/tmp/gps.json'
    trailer_infos = ()
    #(trailer_id, ip, lat, lon) = load_gps_json(gps_data)
    trailer_infos = load_gps_json(gps_data)
    trailer_infos = trailer_infos + (amberlink,)
    send_email(sender, receiver, cc_receiver, trailer_infos)

if __name__ == '__main__':
    main()
