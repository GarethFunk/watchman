#!/usr/bin/env python3

import smtplib
from email.message import EmailMessage
from credentials import smtp_username, smtp_password, smtp_from

"""
Gareth Funk 2019
"""

class Alert:
    def __init__(self):
        self.__smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        self.__smtp_server.ehlo()
        self.__smtp_server.starttls()
        self.__smtp_server.login(smtp_username, smtp_password)
        return

    def __del__(self):
        self.__smtp_server.quit()
        return

    def Email(self, email):
        msg = EmailMessage()
        msg.set_content("Test")
        msg["Subject"] = "Test Subject"
        msg["From"] = smtp_from
        msg["To"] = email
        self.__smtp_server.send_message(msg)
        return

if __name__ == "__main__":
    addr = smtp_from
    a = Alert()
    a.Email(addr)
