from datetime import datetime


transactions = []

def get_transactions():
    return transactions

def add_transaction(transaction, amount, number):
    timestamp = str(datetime.now())
    insert_row = [timestamp, transaction, amount, number]
    transactions.append(insert_row)

images = []

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
