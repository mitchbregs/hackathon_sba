from authorizenet import apicontractsv1
from authorizenet.apicontrollers import*
from decimal import*
import os


class Payment:

    def __init__(self):
        """ constructor: all args are strings """
        # Your Account Sid and Auth Token from bbtwilio.com/console
        self.merchant_id = os.environ['AUTH_API_LOGIN']
        self.merchant_key = os.environ['AUTH_TRANSACTION_KEY']


    def send(self, card_number, expiration, amount):
        """ send the payment and return the transactionID or Error"""
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = self.merchant_id
        merchantAuth.transactionKey = self.merchant_key

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

    def retrieve(self, trans_id):

        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = self.merchant_id
        merchantAuth.transactionKey = self.merchant_key

        transactionDetailsRequest = apicontractsv1.getTransactionDetailsRequest()
        transactionDetailsRequest.merchantAuthentication = merchantAuth
        transactionDetailsRequest.transId = trans_id

        transactionDetailsController = getTransactionDetailsController(transactionDetailsRequest)

        transactionDetailsController.execute()

        transactionDetailsResponse = transactionDetailsController.getresponse()

        if transactionDetailsResponse is not None:
            if transactionDetailsResponse.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
                print('Successfully got transaction details!')

                print('Transaction Id : %s' % transactionDetailsResponse.transaction.transId)
                print('Transaction Type : %s' % transactionDetailsResponse.transaction.transactionType)
                print('Transaction Status : %s' % transactionDetailsResponse.transaction.transactionStatus)
                print('Auth Amount : %.2f' % transactionDetailsResponse.transaction.authAmount)
                print('Settle Amount : %.2f' % transactionDetailsResponse.transaction.settleAmount)
                if hasattr(transactionDetailsResponse.transaction, 'tax') == True:
                    print('Tax : %s' % transactionDetailsResponse.transaction.tax.amount)
                if hasattr(transactionDetailsResponse.transaction, 'profile'):
                    print('Customer Profile Id : %s' % transactionDetailsResponse.transaction.profile.customerProfileId)

                if transactionDetailsResponse.messages is not None:
                    print('Message Code : %s' % transactionDetailsResponse.messages.message[0]['code'].text)
                    print('Message Text : %s' % transactionDetailsResponse.messages.message[0]['text'].text)
            else:
                if transactionDetailsResponse.messages is not None:
                    print('Failed to get transaction details.\nCode:%s \nText:%s' % (transactionDetailsResponse.messages.message[0]['code'].text,transactionDetailsResponse.messages.message[0]['text'].text))
        try:
            return {
                'id': transactionDetailsResponse.transaction.transId,
                'amount': transactionDetailsResponse.transaction.authAmount,
                'status': transactionDetailsResponse.transaction.transactionStatus
            }
        except BaseException:
            return {
                'error': 'Could not find details: {}'.format(transactionDetailsResponse.messages.message[0]['code'])
            }
    

