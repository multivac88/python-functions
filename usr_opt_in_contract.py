import base64

from algosdk.future import transaction
from algosdk import account, mnemonic, logic
from algosdk.v2client import algod
from pyteal import *
import json
import base64

from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, ApplicationCallTxn
from algosdk.future.transaction import *




# user declared algod connection parameters. Node must have EnableDeveloperAPI set to true in its config
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)
params = algod_client.suggested_params()
acc = input("Enter Address to optin ")
secret = input("Enter private Key ")
application_id = int(input("Enter APP ID "))

txn = ApplicationCallTxn(
        sender=acc,
        sp=params,
        app_args=["usr_opt_in"],
        on_complete=1, # optin
        index=application_id,
        rekey_to=None)
stxn = txn.sign(secret)

# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))    
except Exception as err:
    print(err)


