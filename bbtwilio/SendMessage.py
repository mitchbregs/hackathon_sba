import os
from twilio.rest import Client


class SendMessage:

    def __init__(self):
        
        # Your Account Sid and Auth Token from bbtwilio.com/console
        self.account_sid = os.environ['TWILIO_SID']
        self.auth_token = os.environ['TWILIO_TOKEN']
        self.phone_num = '+12028310945'

    def send(self, receiver, message):
        
        client = Client(self.account_sid, self.auth_token)
        
        message = client.messages.create(
                body=message,
                from_=self.phone_num,
                to=receiver
        )
        
        return message.sid
