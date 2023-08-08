import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "An email with hourly picture from marijuana farm"
body = "Picture attachment from marijuana farm."
sender_email = "kingsolarman66@gmail.com"
receiver_email = "greg@king-solarman.com"
#bcc_receiver_email = "lallende.la@gmail.com"
#cc_receiver_email = "allen@king-solarman.com,hugo@king-solarman.com,mike@king-solarman.com,greg@king-solarman.com"
cc_receiver_email = ["lallende.la@gmail.com", "hugo@king-solarman.com", "mike@king-solarman.com", "greg@king-solarman.com", "kingsolarman88@gmail.com"]
#cc_receiver_email = "allen@king-solarman.com,hugo@king-solarman.com,mike@king-solarman.com,greg@king-solarman.com"
#cc_receiver_email = "greg@king-solarman.com"
bcc_receiver_email = "greg@king-solarman.com"
#bcc_receiver_email = "lallende.la@gmail.com"
password = '4087280048'

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = ','.join(cc_receiver_email)
message["Subject"] = subject
#message["Cc"] = cc_receiver_email  # Recommended for mass emails
#message["Bcc"] = bcc_receiver_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

filename = "marijuana_farm.jpg"  # In same directory as script

# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    #server.sendmail(sender_email, receiver_email, text)
    server.send_message(message)
