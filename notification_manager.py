import smtplib
import os

GMAIL = os.environ["GMAIL"]
GMAIL_PW = os.environ["PYTHON_FLIGHT_FINDER_APP_PW"]
Y_MAIL = os.environ["Y_MAIL"]
SMTP = "smtp.gmail.com"
PORT = 587

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def send_mail(self, message, user_mails):
        for mail in user_mails:
            # print("Sending mail...")
            with smtplib.SMTP(SMTP, PORT) as conn:
                conn.starttls()
                conn.login(user=GMAIL, password=GMAIL_PW)
                conn.sendmail(
                    from_addr=GMAIL,
                    to_addrs=mail,
                    msg=message.encode("utf-8")
                )
            # print("Mail sent!")