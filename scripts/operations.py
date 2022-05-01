from algosdk import account, mnemonic
from algosdk.v2client import algod # connect client
# build transaction
from algosdk.future import transaction
from algosdk import constants

# for submitting tx
import json
import base64

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

def first_transaction_example(private_key, my_address):
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)
    
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

    # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE 
    receiver = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
    note = "Hello World".encode()
    amount = 1000000

    unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, amount, None, note)
    signed_txn = unsigned_txn.sign(private_key)

     #submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))
    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    print("Amount transfered: {} microAlgos".format(amount) )    
    print("Fee: {} microAlgos".format(params.fee) ) 


    account_info = algod_client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")
#My address: PUH4IZLOGSTUZB3KXW7QDYQUGMNEF7A4RJGCSHRH4EHJUM7BJBMCL67LQA
#My private key: SHJxpdMgfoEFJqRjf7bYrz77IHc5Hgz0WWhn0kIqqD59D8RlbjSnTIdqvb8B4hQzGkL8HIpMKR4n4Q6aM+FIWA==
#My passphrase: empower shift sport artwork wisdom gate coral picnic unaware supreme unable turtle wait sight slight bullet light guitar reflect chapter mad appear vocal ability season

first_transaction_example("SHJxpdMgfoEFJqRjf7bYrz77IHc5Hgz0WWhn0kIqqD59D8RlbjSnTIdqvb8B4hQzGkL8HIpMKR4n4Q6aM+FIWA==", "PUH4IZLOGSTUZB3KXW7QDYQUGMNEF7A4RJGCSHRH4EHJUM7BJBMCL67LQA")