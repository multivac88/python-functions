import base64

from algosdk.future import transaction
from algosdk import account, mnemonic, logic
from algosdk.v2client import algod
from pyteal import *

from contracts.vault import approval_program, clear_state_program

# compile program to TEAL assembly
with open("./approval.teal", "w") as f:
    approval_program_teal = approval_program()
    f.write(approval_program_teal)


# compile program to TEAL assembly
with open("./clear.teal", "w") as f:
    clear_state_program_teal = clear_state_program()
    f.write(clear_state_program_teal)