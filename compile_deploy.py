import base64

from algosdk.future import transaction
from algosdk import account, mnemonic, logic
from algosdk.v2client import algod
from pyteal import *

from contracts.vault import approval_program, clear_state_program

# public key of asset creator
CREATOR = "PUH4IZLOGSTUZB3KXW7QDYQUGMNEF7A4RJGCSHRH4EHJUM7BJBMCL67LQA"
# secret key of asset creator
CREATOR_SK = "SHJxpdMgfoEFJqRjf7bYrz77IHc5Hgz0WWhn0kIqqD59D8RlbjSnTIdqvb8B4hQzGkL8HIpMKR4n4Q6aM+FIWA=="


# user declared algod connection parameters. Node must have EnableDeveloperAPI set to true in its config
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# helper function to compile program source
def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])


# helper function that formats global state for printing
def format_state(state):
    formatted = {}
    for item in state:
        key = item['key']
        value = item['value']
        formatted_key = base64.b64decode(key).decode('utf-8')
        if value['type'] == 1:
            # byte string
            if formatted_key == 'voted':
                formatted_value = base64.b64decode(value['bytes']).decode('utf-8')
            else:
                formatted_value = value['bytes']
            formatted[formatted_key] = formatted_value
        else:
            # integer
            formatted[formatted_key] = value['uint']
    return formatted

# helper function to read app global state
def read_global_state(client, app_id):
    app = client.application_info(app_id)
    global_state = app['params']['global-state'] if "global-state" in app['params'] else []
    return format_state(global_state)



# create new application
def create_app(client, approval_program, clear_state_program, global_schema, local_schema):
    # define sender as creator
    sender = CREATOR

    # declare on_complete as NoOp
    on_complete = transaction.OnComplete.NoOpOC.real

    # get node suggested parameters
    params = client.suggested_params()

    application_args = [
        "miami",
        1000,
        500
    ]

    assets = [86114010]
    # create unsigned transaction
    txn = transaction.ApplicationCreateTxn(sender, params, on_complete, \
                                            approval_program, clear_state_program, \
                                            global_schema, local_schema, \
                                                app_args=application_args, foreign_assets=assets)

    # sign transaction
    signed_txn = txn.sign(CREATOR_SK)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # wait for confirmation
    try:
        transaction_response = transaction.wait_for_confirmation(client, tx_id, 5)
        print("TXID: ", tx_id)
        print("Result confirmed in round: {}".format(transaction_response['confirmed-round']))

    except Exception as err:
        print(err)
        return

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response['application-index']
    print("Created new app-id:", app_id)

    return app_id




def main() :
    # initialize an algodClient
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # define private keys
    creator_private_key = CREATOR_SK

    # declare application state storage (immutable)
    local_ints = 2
    local_bytes = 0
    global_ints = 6
    global_bytes = 2
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    # compile program to TEAL assembly
    with open("./approval.teal", "w") as f:
        approval_program_teal = approval_program()
        f.write(approval_program_teal)


    # compile program to TEAL assembly
    with open("./clear.teal", "w") as f:
        clear_state_program_teal = clear_state_program()
        f.write(clear_state_program_teal)

    # compile program to binary
    approval_program_compiled = compile_program(algod_client, approval_program_teal)

    # compile program to binary
    clear_state_program_compiled = compile_program(algod_client, clear_state_program_teal)

    print("--------------------------------------------")
    print("Deploying Counter application......")

    # create new application
    app_id = create_app(algod_client, approval_program_compiled, clear_state_program_compiled, global_schema, local_schema)

    # read global state of application
    print("Global state:", read_global_state(algod_client, app_id))

    #print("--------------------------------------------")
    #print("Calling Counter application......")
    #app_args = ["Add"]
    #call_app(algod_client, CREATOR_SK, app_id, app_args)

    # read global state of application
    print("Global state:", read_global_state(algod_client, app_id))

main()
