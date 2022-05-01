import json
from algosdk import account, mnemonic

acct = account.generate_account()
print("Address: ", acct[1])
print("PrivateKey: ", acct[0])