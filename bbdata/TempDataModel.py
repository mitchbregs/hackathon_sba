from datetime import datetime

business_owner_data = {

    "name" : "Mitch Jobs",
    "zip" : 24141,
    "business_name" : "Mitch's Roofing",
    "phone_number" : "+19086162014"
    #"phone_number" : "+15135265845"
}

numbers_dict = {

    '+19086162014':'370000000000002',
    '+15712455390':'6011000000000012',
    '+15135265845':'5424000000000015',
    #'+15712691693':'4007000000027',
    '+15712691693':'4012888818888'

}


sms_activity = [
    ['2019-05-04 14:10:53.854653',"RECEIVED: Pay $20.00 for gas TEST. FROM:","+17038161881"],
    ['2019-05-04 14:10:52.684836',"SENT: Transaction Processed! Confirmation 999999999 TO:","+17038161881"]
]

def print_data_models():
    print(business_owner_data)
    print(numbers_dict)
    print(sms_activity)

def lookup(phone):
    return numbers_dict[phone]

def business_name():
    return business_owner_data["business_name"]

def business_phone():
    return business_owner_data["phone_number"]


def get_sms():
    return sms_activity

def add_message(message, number):
    timestamp = str(datetime.now())
    insert_row = [timestamp, message, number]
    sms_activity.append(insert_row)
