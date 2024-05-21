import smtplib
from django.conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender, receiver, title, content):
    # 创建邮件对象和设置邮件内容
    message = MIMEMultipart("alternative")
    message["Subject"] = title
    message["From"] = sender
    message["To"] = receiver
    # 添加文本
    part = MIMEText(content, "plain")
    # 添加正文到邮件对象中
    message.attach(part)
    # 发送邮件
    try:
        # 创建SMTP服务器连接
        with smtplib.SMTP_SSL(settings.CRC_EMAIL_HOST, settings.CRC_EMAIL_PORT) as server:
            # 登录到邮件服务器
            server.login(sender, settings.CRC_EMAIL_AUTH_CODE)
            # 发送邮件
            server.sendmail(sender, receiver, message.as_string())
    except Exception as e:
        print(f"Error: {e}")
        return False
    else:
        return True
