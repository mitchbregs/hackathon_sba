from flask import Flask, request, render_template, redirect
from twilio.twiml.messaging_response import MessagingResponse

import os
import re
import requests

import bbauth.Payment as pay
import bbauth.TransactionsDataModel as transaction_data
import bbdata.TempDataModel as data
from bbtwilio.SendMessage import *
from bbdata.generators import GeneratorAPI


app = Flask(__name__)
generatorAPI = GeneratorAPI()


@app.route("/print-data", methods=['GET'])
def print_data():
    """Send a test payment"""
    data.print_data_models()
    return "Done"


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
    save_message = "RECEIVED: {}, FROM: {}".format(message, number)
    data.add_message(save_message, number)


@app.route('/transactions-feed')
def transactions_feed():
    return render_template('transactions.html', messages=transaction_data.get_transactions())

@app.route('/claims-feed')
def claims_feed():
    return render_template('claims.html', images=transaction_data.get_claims())


@app.route('/sms', methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    bbt = SendMessage()

    # Get the message the user sent our Twilio number
    number = request.form.get('From', None)
    body = request.values.get('Body', None)

    # dealing with incoming MMS (image)
    num_images = request.values.get('NumMedia', None)
    if num_images != '0':
        filename = request.values.get('MessageSid', None) + '.png'
        with open('{}/{}'.format('static/mms', filename), 'wb') as f:
            image_url = request.values.get('MediaUrl0', None)
            f.write(requests.get(image_url).content)
        f.close()
        message = 'Thank you for sending your image. We have backed it up for your SBA loan application or insurance claim!'

        # this will begin the image saving workflow; images stored in bbdata/images/
        transaction_data.add_claim(number, filename)
        return bbt.send(number, message)

    store_incoming_sms(body, number)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'Hello':
        return bbt.send(number, 'Hi friend!')

    elif body == 'Bye':
        return bbt.send(number, 'See you later!')

    # Parse payment command
    words = []
    try:
        words = body.split()
    except AttributeError:
        print("Message has no body!")
        message = "Message has no body!"
        return bbt.send(number, message)

    words = [word.lower() for word in words if isinstance(word, str)]
    if 'pay' in words or 'payment' in words or 'paid' in words:

        # lookup number
        credit_card = ''
        try:
            credit_card = data.lookup(number)
        except KeyError:
            message = "We don't have your card on file, Sorry!"
            return bbt.send(number, message)
        amount = ''
        try:
            amount = re.search(
                r'[+-]?(\$\d+|\d+\.\d+|\.\d+|\d+\.)([eE]\d+)?', body)
            amount = (amount.group()).replace('$', '')
        except AttributeError:
            print('Could not find a $ sign.')
            message = 'To process a payment, you must include the word "pay" and a $ before the amount. \n\nFor example, say "hey, pay my employee Joe $45.63".'
            return bbt.send(number, message)
        except IndexError:
            print("Message has no amount!")
            message = "Message has no body!"
            return bbt.send(number, message)

        expiration = "2020-12" # hard coded right now
        payment = pay.Payment()
        transaction_response = payment.send(credit_card, expiration, float(amount))
        transaction_data.add_transaction(transaction_response.transId, float(amount), number)
        bbt.send(number, "Transaction ID is " + str(transaction_response.transId))
        return bbt.send(data.business_phone(), "You've been paid. Transaction ID is " + str(transaction_response.transId))

    if 'charge' in words:
        # only allowed for business business owner

        if number != data.business_phone():
            print (number)
            print (data.business_phone())
            return bbt.send(number,
                'Only registered merchants can request payments.  Please sign up on our website.'
            )

        # lookup number
        phone = ''

        try:
            phone = re.search(
                r'(\+\d{11})', body)
            phone = phone.group()
        except AttributeError:
            print('Could not find a phone number.')
            return bbt.send(number,
                'To make a charge request, you must include a full phone number like +17035555555'
            )
        except IndexError:
            print("Message has no phone number!")
            # resp.message("Message has no body!")
            return str(resp)

        bbt.send(phone, str(data.business_name()) + " has requested a payment from you.  Reply PAY $XX to make a payment with your credit card." )
        return bbt.send(number, "Confirmed. Payment request sent to "+phone )



    if 'bbhelp' in words:
        resp.message('Thanks for contacting BizBackup - a text-based disaster relief platform. \n\nTo make a payment: use the command "pay $0.01" \n\nTo find closest power: "power 20002" \n\nOther functionality: Include it here..')
        return bbt.send(number, str(resp.message))

    if 'lookup' in words:
        try:
            search_id = re.search(
                '(\d{11})', body)
            search_id = search_id.group()
        except AttributeError:
            message = 'Could not find a transaction id in your message.'
            return bbt.send(number, message)
        try:
            search = pay.Payment()
            details = search.retrieve(search_id)
            if 'id' in details.keys():
                message = 'Found transaction details: \nID: {} \nAmount: {} \nStatus: {}'.format(details['id'], details['amount'], details['status'])
            else:
                message = 'Could not find a transaction \n\n{}'.format(details['error'])
            return bbt.send(number, message)
        except BaseException:
            message = 'Something went wrong.'
            return bbt.send(number, messages)


    if 'energy' in words or 'power' in words or 'generators' in words:
        zipcode = re.search('(\d{5})', body).group(0)
        generators = generatorAPI.zipcodeQuery(zipcode)

        message = ''
        i = 1
        for entry in generators:

            if entry['address']:
                message = message + '{}. {}: {} \n\n'.format(i, entry['operator'], entry['address'])
            else:
                message = message + '{}. {}: {} \n\n'.format(i, entry['operator'], generatorAPI.decodeLatLong(entry['latitude'], entry['longitude']))
            i += 1
        print(message)
        return bbt.send(number, message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
