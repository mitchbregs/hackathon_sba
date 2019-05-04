from flask import Flask, request, render_template, redirect
from twilio.twiml.messaging_response import MessagingResponse

import os
import re

import bbauth.Payment as pay
import bbdata.TempDataModel as data
from bbtwilio.SendMessage import *
from bbdata.generators import GeneratorAPI


app = Flask(__name__)
generatorAPI = GeneratorAPI()


@app.route("/test_pay", methods=['GET'])
def test_pay():
    """Send a test payment"""
    transactionID = pay.send_test_payment(999)
    return "transactionID is " + str(transactionID)

def send_message():
    """Send a text message"""
    bbtwilio = SendMessage()
    # Must be a Twilio verified phone number
    return bbtwilio.send('+0000000000', 'Type a message here.')

@app.route('/live-feed')
def live_feed():
    return render_template('live-feed.html', messages=data.get_sms())


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

def store_incoming_sms(message, number):
    """Store a text message"""
    save_message = "RECEIVED: "+message+" FROM: "
    data.add_message(save_message, number)



@app.route('/sms', methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    number = request.form.get('From', None)
    body = request.values.get('Body', None)
    store_incoming_sms(body, number)
    # print('{}: {}'.format(number, body))

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
    print(body)
    words = []
    try:
        words = body.split()
    except AttributeError:
        print("Message has no body!")
        #resp.message("Message has no body!")
        return str(resp)

    words = [word.lower() for word in words if isinstance(word, str)]
    if 'pay' in words or 'payment' in words or 'paid' in words:
        # lookup number
        credit_card = ''
        try:
            credit_card = data.lookup(number)
        except KeyError:
            resp.message("We don't have your card on file, Sorry!")
            return str(resp)
        amount = ''
        try:
            amount = re.search(
                r'[+-]?(\$\d+|\d+\.\d+|\.\d+|\d+\.)([eE]\d+)?', body)
            amount = (amount.group()).replace('$', '')
        except AttributeError:
            print('Could not find a $ sign.')
            resp.message(
                'To process a payment, you must include the word "pay" and a $ before the amount. \n\nFor example, say "hey, pay my employee Joe $45.63".'
            )
            return str(resp)
        except IndexError:
            print("Message has no amount!")
            # resp.message("Message has no body!")
            return str(resp)
        
        expiration = "2020-12" # hard coded right now
        payment = pay.Payment()
        trans_id = payment.send(credit_card, expiration, float(amount))
        bbt = SendMessage()
        return bbt.send(number, "Transaction ID is " + str(trans_id))

    if 'bbhelp' in words:
        resp.message('Thanks for contacting BizBackup - a text-based disaster relief platform. \n\nTo make a payment: use the command "pay $0.01" \n\nTo find closest power: "power 20002" \n\nOther functionality: Include it here..')
        return str(resp)

    if 'lookup' in words:
        try:
            search_id = re.search(
                '(\d{11})', body)
            search_id = search_id.group()
        except AttributeError:
            resp.message('Could not find a transaction id in your message.')
            return str(resp)
        try:
            search = pay.Payment()
            details = search.retrieve(search_id)
            if 'id' in details.keys():
                resp.message('Found transaction details: \nID: {} \nAmount: {} \nStatus: {}'.format(details['id'], details['amount'], details['status']))
            else:
                resp.message('Could not find a transaction \n\n{}'.format(details['error']))
            return str(resp)
        except BaseException:
            resp.message('Something went wrong.')
            return str(resp)



    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
