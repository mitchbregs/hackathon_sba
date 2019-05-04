import os
from twilio.rest import Client
import sys

sys.path.insert(0, "../data")

from data import TempDataModel as data

class SendMessage:

    def __init__(self):

        # Your Account Sid and Auth Token from bbtwilio.com/console
        self.account_sid = os.environ['TWILIO_SID']
        self.auth_token = os.environ['TWILIO_TOKEN']
        self.phone_num = os.environ['TWILIO_NUMBER'] #'+12028310945'

    def send(self, receiver, message_text):

        client = Client(self.account_sid, self.auth_token)

        message = client.messages.create(
                body=message_text,
                from_=self.phone_num,
                to=receiver
        )
        # log message
        # SENT: message TO:
        data.add_message("SENT: "+str(message_text)+" TO: ", str(receiver))

        return message.sid
