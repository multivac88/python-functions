import base64

from algosdk.future import transaction
from algosdk import account, mnemonic, logic
from algosdk.v2client import algod
from pyteal import *
import json
import base64

from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, ApplicationCallTxn
from algosdk.future.transaction import *

# public key of asset creator
CREATOR = "NRZE7JL5PTK7JYWWVQRXSJTBGMS6XKXWTOSQ3PCZCVFF7HMF4SBJVUAF7Y"
# secret key of asset creator
CREATOR_SK = "iF+xjLCY8hVPESLYT+P7x+HEgkNUlwt6FDqny5YIBoxsck+lfXzV9OLWrCN5JmEzJeuq9pulDbxZFUpfnYXkgg=="


# user declared algod connection parameters. Node must have EnableDeveloperAPI set to true in its config
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)

params = algod_client.suggested_params()
params.fee = 1000
application_id = 87239468


txn = ApplicationCallTxn(
    sender=CREATOR, 
    sp=params, 
    index=application_id, 
    on_complete=1, # optin
    foreign_assets=[86114010],
    app_args=["contract_opt_in_vault_asset"],
    rekey_to=None,

    )
stxn = txn.sign(CREATOR_SK)
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