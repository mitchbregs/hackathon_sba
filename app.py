from flask import Flask, request, render_template, redirect
from twilio.twiml.messaging_response import MessagingResponse

from bbtwilio.SendMessage import *


app = Flask(__name__)


def send_message():
    """Send a text message"""
    bbtwilio = SendMessage()
    # Must be a Twilio verified phone number
    return bbtwilio.send('+0000000000', 'Type a message here.')


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/sms', methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    number = request.form.get('From', None)
    body = request.values.get('Body', None)
    print('{}: {}'.format(number, body))

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'hello':
        resp.message('Hi!')
    elif body == 'bye':
        resp.message('Goodbye')

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
