from datetime import datetime


transactions = []

def get_transactions():
    return transactions

def add_transaction(transaction, amount, number):
    timestamp = str(datetime.now())
    insert_row = [timestamp, transaction, amount, number]
    transactions.append(insert_row)

images = [{'ts': "2019-05-05 01:02:49.422634", 'image_path':"MM7714faf33436069222249dca4a9fc105.png", 'sender':"+15716789254"}]

def get_claims():
    return images

def add_claim(sender, image_path):
    timestamp = str(datetime.now())
    tmp = {
        'ts': timestamp,
        'image_path': image_path,
        'sender': sender
    }
    images.append(tmp)
