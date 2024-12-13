import smtplib
from email.mime.text import MIMEText
from datetime import datetime


def send_email(body, recipient):
   msg = MIMEText(body)
   # Remove date() if you wish to use this multiple times a day
   msg['Subject'] = "PA Liquor Store Scrape " + str(datetime.now().date())
   msg['From'] = "liquorstorescraper@gmail.com"
   msg['To'] = recipient
   with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
      smtp_server.login("liquorstorescraper@gmail.com", "tpzu hfqf nmug warp")
      smtp_server.sendmail("liquorstorescraper@gmail.com", recipient, msg.as_string())