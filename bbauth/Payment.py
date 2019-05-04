from authorizenet import apicontractsv1
from authorizenet.apicontrollers import*
from decimal import*
import os


class Payment:

    def __init__(self):
        """ constructor: all args are strings """
        # Your Account Sid and Auth Token from bbtwilio.com/console
        self.merchent_id = os.environ['AUTH_API_LOGIN']
        self.merchent_key = os.environ['AUTH_TRANSACTION_KEY']


    def send(self, card_number, expiration, amount):
        """ send the payment and return the transactionID or Error"""
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = self.merchent_id
        merchantAuth.transactionKey = self.merchent_key

        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = card_number
        # 5424000000000015
        creditCard.expirationDate = expiration

        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType ="authCaptureTransaction"
        transactionrequest.amount = Decimal(amount)
        transactionrequest.payment = payment


        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = merchantAuth
        createtransactionrequest.refId ="MerchantID-0001"

        createtransactionrequest.transactionRequest = transactionrequest
        createtransactioncontroller = createTransactionController(createtransactionrequest)
        createtransactioncontroller.execute()

        response = createtransactioncontroller.getresponse()

        if (response.messages.resultCode=="Ok"):
            transactionID = response.transactionResponse.transId
            return transactionID
        else:
            return response.messages.resultCode

def send_test_payment():

    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = os.environ['AUTH_API_LOGIN']
    merchantAuth.transactionKey = os.environ['AUTH_TRANSACTION_KEY']

    creditCard = apicontractsv1.creditCardType()
    creditCard.cardNumber ="4111111111111111"
    # 5424000000000015
    creditCard.expirationDate ="2020-12"

    payment = apicontractsv1.paymentType()
    payment.creditCard = creditCard

    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType ="authCaptureTransaction"
    transactionrequest.amount = Decimal('2.22')
    transactionrequest.payment = payment


    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId ="MerchantID-0001"

    createtransactionrequest.transactionRequest = transactionrequest
    createtransactioncontroller = createTransactionController(createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()
    if (response.messages.resultCode=="Ok"):
        transactionID = response.transactionResponse.transId
        print("Transaction ID : %s"% transactionID)
        return transactionID
    else:
        print("response code: %s"% response.messages.resultCode)
        return("Transaction failed")
