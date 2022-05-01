import json
import base64
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
from algosdk.future.transaction import *

# Specify your node address and token. This must be updated.
# algod_address = ""  # ADD ADDRESS
# algod_token = ""  # ADD TOKEN

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)

#   Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):    
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0;
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1       
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break

#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1        
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break

# public key of asset creator
CREATOR = "PUH4IZLOGSTUZB3KXW7QDYQUGMNEF7A4RJGCSHRH4EHJUM7BJBMCL67LQA"
# secret key of asset creator
CREATOR_SK = "SHJxpdMgfoEFJqRjf7bYrz77IHc5Hgz0WWhn0kIqqD59D8RlbjSnTIdqvb8B4hQzGkL8HIpMKR4n4Q6aM+FIWA=="

MANAGER  = CREATOR
RESERVE  = CREATOR
FREEZE   = CREATOR
CLAWBACK = CREATOR

TOTAL    = 1000000

############################# CREATE ASSET
def create_asset():

    # Get network params for transactions before every transaction.
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True


    create_asset_txn = AssetConfigTxn(
        sender=CREATOR,
        sp=params, #suggested params from algod
        total=TOTAL,
        default_frozen=False,
        unit_name="UCT",
        asset_name="urban change token",
        manager=MANAGER,
        reserve=RESERVE,
        freeze=FREEZE,
        clawback=CLAWBACK,
        url="",
        decimals=0,
        metadata_hash=None)

    signed_create_asset_txn = create_asset_txn.sign(CREATOR_SK)

    # Send the transaction to the network and retrieve the txid.
    confirmed_txn = ""
    txid = ""
    try:
        txid = algod_client.send_transaction(signed_create_asset_txn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    
    except Exception as err:
        print(err)
    # Retrieve the asset ID of the newly created asset by first
    # ensuring that the creation transaction was confirmed,
    # then grabbing the asset id from the transaction.

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    # print("Decoded note: {}".format(base64.b64decode(
    #     confirmed_txn["txn"]["txn"]["note"]).decode()))

    try:
    # Pull account info for the creator
    # account_info = algod_client.account_info(accounts[1]['pk'])
    # get asset_id from tx
    # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print_created_asset(algod_client, CREATOR, asset_id)
        print_asset_holding(algod_client, CREATOR, asset_id)
    except Exception as e:
        print(e)

create_asset()

