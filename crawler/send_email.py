# -*- encoding:utf-8 -*-


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ConfigParser


cf =ConfigParser.ConfigParser()
cf.read('config.conf')
username = cf.get('email','username')
sender = cf.get('email','sender')
password = cf.get('email','password')
smtp_addr = cf.get('email','smtp_addr')

def send_email(receiver,content):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Bitcoin related news"
    try:
        send_content = MIMEText(content.decode("utf-8", errors = 'replace'),'plain','utf-8')    
    except UnicodeDecodeError:
        send_content = MIMEText(content.decode("gbk"),'plain','utf-8')    
    send_content["Accept-Language"] = "zh-CN"
    send_content["Accept-Charset"] = "ISO-8859-1,utf-8"

    msg.attach(send_content)


    client = smtplib.SMTP()
    client.connect(smtp_addr)
    client.login(username,password)
    client.sendmail(sender,receiver,msg.as_string())
    client.quit()


if __name__ == '__main__':
    # client = smtplib.SMTP()
    # client.connect("smtp.163.com")
    # client.login(username, password)
    # client.quit()
    receiver = r"colin.qian@meritco-group.com"
    send_email(receiver,"This is a trial of an extremely fascinating project.\n No reply needed.")

