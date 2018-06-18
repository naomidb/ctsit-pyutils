from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mimetypes
import smtplib
import getpass

def connect_to_smtp(host, port):
    try:
        connection = smtplib.SMTP(host=host,
                                  port=port,)
        connection.starttls()
        login = input("Enter your gatorlink: ")
        password = getpass.getpass("Enter your password: ")
        connection.login(login, password)
    except smtplib.SMTPConnectError as e:
        print(e)
        connection = None

    return connection

def create_email(config, body, file):
    msg = MIMEMultipart()
    msg['From'] = config.get('from_email')
    msg['Subject'] = config.get('subject')

    to_list = config.get('to_emails')
    to_string = ",".join(to_list)
    msg['To'] = to_string

    msg.attach(MIMEText(body, 'plain'))

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(file)
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()

    attachment.add_header("Content-Disposition", "attachment", filename=file)
    msg.attach(attachment)

    return msg

def send_message(connection, msg, config):
    connection.sendmail(config.get('from_email'), config.get('to_emails'), msg.as_string())
    connection.quit()

