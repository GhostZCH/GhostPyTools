import smtplib
from email.utils import formatdate
from email.mime.text import MIMEText
from email.header import Header


def send_email(content='hello world'):
    to_list = ['a@163.com', 'b@163.com']

    msg = MIMEText(content, 'html')
    msg['From'] = 'xxx@163.com'
    msg['To'] = ",".join(to_list)
    msg['Subject'] = Header('Title of email')
    msg['Date'] = formatdate()

    smtp = smtplib.SMTP_SSL()
    smtp.connect('host', 999)  # need modify when use
    smtp.login('username', 'pwd')
    smtp.sendmail('xxx@163.com', to_list, msg.as_string())

    smtp.quit()

send_email()

