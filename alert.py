#!/usr/bin/env python3

import smtplib
from email.message import EmailMessage
from googlevoice import Voice
from credentials import smtp_username, smtp_password, smtp_from, \
                        gvoice_username, gvoice_password

"""
Gareth Funk 2019
"""

class Alert:
    def __init__(self):
        self.__gvoice = Voice()
        #self.__gvoice.login(gvoice_username, gvoice_password)
        return

    def __del__(self):
        #self.__gvoice.logout()
        return

    def Email(self, emails):
        if type(emails) is str:
            email = emails
        elif type(emails) is list:
            email = ", ".join(emails)
        else:
            raise TypeError("Unsupported argument type: " + str(type(emails)))
        msg = EmailMessage()
        msg.set_content("Test")
        msg["Subject"] = "Test Subject"
        msg["From"] = smtp_from
        msg["To"] = email
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(smtp_username, smtp_password)
        smtp_server.send_message(msg)
        smtp_server.quit()
        return

    def Sms(self, number):
        self.__gvoice.send_sms(number, "SMS test")
        return

if __name__ == "__main__":
    addr = smtp_from
    a = Alert()
    a.Email(addr)
    a.Email(addr)
