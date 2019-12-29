#!/usr/bin/env python3

import smtplib
from email.message import EmailMessage
from twilio.rest import Client
from credentials import smtp_username, smtp_password, smtp_from, \
                        twilio_account_sid, twilio_auth_token, twilio_send_number

"""
Gareth Funk 2019
"""

class Alert:
    def __init__(self):
        return

    def __del__(self):
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

    def Sms(self, numbers):
        if type(numbers) is not list:
            raise TypeError("Unsupported argument type: " + str(type(numbers)))
        twilio_client = Client(twilio_account_sid, twilio_auth_token)
        body="https://github.com/GarethFunk for all the dankest code",
        for number in numbers:
            twilio_client.messages.create(
                body = body,
                from_= twilio_send_number,
                to=number
                )
        return

    def Call(self, numbers):
        if type(numbers) is not list:
            raise TypeError("Unsupported argument type: " + str(type(numbers)))
        twilio_client = Client(twilio_account_sid, twilio_auth_token)      
        for number in numbers:
            twilio_client.calls.create(
                url='http://demo.twilio.com/docs/voice.xml',
                from_= twilio_send_number,
                to=number,
                )
        return

if __name__ == "__main__":
    from alert_recipients import emails, sms_numbers
    a = Alert()
    a.Email(emails)
    a.Sms(sms_numbers)
    a.Call(sms_numbers)
