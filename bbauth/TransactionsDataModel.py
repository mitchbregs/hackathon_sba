from datetime import datetime


transactions = []

def get_transactions():
    return transactions

def add_transaction(transaction, amount, number):
    timestamp = str(datetime.now())
    insert_row = [timestamp, transaction, amount, number]
    transactions.append(insert_row)

