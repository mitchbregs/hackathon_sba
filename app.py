from flask import Flask, request, render_template, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os

import bbauth.Payment as pay
import data.TempDataModel as cards
from bbtwilio.SendMessage import *


app = Flask(__name__)

@app.route("/test_pay", methods=['GET'])
def test_pay():
    """Send a test payment"""
    transactionID = pay.send_test_payment(999)
    return "transactionID is "+str(transactionID)



def send_message():
    """Send a text message"""
    bbtwilio = SendMessage()
    # Must be a Twilio verified phone number
    return bbtwilio.send('+0000000000', 'Type a message here.')


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/error', methods=['GET', 'POST'])
def fallback_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    number = request.form.get('From', None)
    body = request.values.get('Body', None)
    print('{}: {}'.format(number, body))
    resp = MessagingResponse()
    return str(resp)


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
    if body == 'Hello':
        print("Sending...")
        bbt = SendMessage()
        return bbt.send(number, 'Type a message here.')


    elif body == 'Bye':
        resp.message("Goodbye")
        return str(resp)


    # Parse payment command
    print (body)
    words = []
    try:
        words = body.split()
    except AttributeError:
        print("Message has no body!")
        #resp.message("Message has no body!")
        return str(resp)


    if words[0].lower() == 'pay':
        #lookup number
        credit_card = ''
        try:
            credit_card = cards.lookup(number)
        except KeyError:
            resp.message("We don't have your card on file, Sorry!")
            return str(resp)
        amount = ''
        try:
            amount = words[1]
        except IndexError:
            print("Message has no amount!")
            #resp.message("Message has no body!")
            return str(resp)

        expiration = "2020-12" # hard coded right now
        payment = pay.Payment()
        trans_id = payment.send(credit_card, expiration, amount)
        bbt = SendMessage()
        return bbt.send(number, "Transaction ID is "+str(trans_id) )

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
