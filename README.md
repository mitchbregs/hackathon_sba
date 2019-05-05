# BizBackup

## About

Text-message based disaster relief. Do more with less!

## Setup

### Create a `virtualenv`
`$ virtualenv my_env_name --python=python3`


### Activate `my_env_name`
`$ source bin/activate`


### Clone `hackathon_sba` repo
`git clone https://github.com/mitchbregs/hackathon_sba.git`


### Install all requirements
`pip install -r requirements.txt`


### Create a `.env` file in root directory
 `vim .env`
 
##### Place the following here:
 ```
# Authorize.net API credentials
export AUTH_TRANSACTION_KEY="XXX"
export AUTH_API_LOGIN="XXX"

# Twilio credentials
export TWILIO_SID="XXX"
export TWILIO_TOKEN="XXX"
export TWILIO_NUMBER="XXX"

# Google Maps credentials
export GOOGLE_API_KEY="XXX"
 
 ```
 
##### Source it:
 `source .env`

### Set up `ngrok`
[Follow these steps](https://ngrok.com/)

##### Eventually:
`./ngrok http 5000`

and you will see something like this: http://3301c6e7.ngrok.io

### Set Twilio webhook endpoint

![https://www.twilio.com/console/phone-numbers/](https://i.imgur.com/xZHgkku.png "Twilio webhook + ngrok")

Make sure to add the phone number you will be texting with to Verified Numbers on Twilio Console.

#### Run the app

`flask run`

#### Go to website

`localhost:5000/`

##### Sitemap

http://localhost:5000/home

http://localhost:5000/live-feed

http://localhost:5000/transactions-feed

http://localhost:5000/claims-feed

## Usage

### Transactions

`localhost:5000/transactions-feed`

#### Charge

Text `charge +1800555555` to your Twilio phone number to charge +1800555555 for a payment.

#### Pay

Text `pay $0.01` to your Twilio phone number to accept and complete payment request.

#### Lookup

Text `lookup 00000000` (TransactionID) to Twilio phone number to lookup status of transaction.

### Claims

`localhost:5000/claims-feed`

#### Start claim process

Text an image to your Twilio phone number to start filing a relief loan claim.

### BBApps

Text `power 24141` to your Twilio phone number to get the closest publicly available power sources near you.

### BBHelp

Text `bbhelp` to your Twilio phone number to learn more about what BizBackup can do.

## Usage

### Authors

#### Mitchell Bregman (https://github.com/mitchbregs)
#### Jack Carlson (https://github.com/JACflip55)
#### Walter Carlson (https://github.com/wfcarlson)
#### Braxton Croley (https://github.com/braxtoncroley)

## References

[Small Business Week Hackathon 2019 - SBA (Sponsored by Visa and Authorize.net)](https://smallbizweek.hackathon.com/)


