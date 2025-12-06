import json
import os
from datetime import datetime

import pandas as pd
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware  # Necessary for POA chains


def connect_to(chain):
    if chain == 'source':  # The source contract chain is avax
        api_url = f"https://api.avax-test.network/ext/bc/C/rpc" #AVAX C-chain testnet

    if chain == 'destination':  # The destination contract chain is bsc
        api_url = f"https://data-seed-prebsc-1-s1.binance.org:8545/" #BSC testnet

    if chain in ['source','destination']:
        w3 = Web3(Web3.HTTPProvider(api_url))
        # inject the poa compatibility middleware to the innermost layer
        w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    return w3


def get_contract_info(chain, contract_info):
    """
        Load the contract_info file into a dictionary
        This function is used by the autograder and will likely be useful to you
    """
    try:
        with open(contract_info, 'r')  as f:
            contracts = json.load(f)
    except Exception as e:
        print( f"Failed to read contract info\nPlease contact your instructor\n{e}" )
        return 0
    return contracts[chain]



def scan_blocks(chain, contract_info="contract_info.json"):
    """
        chain - (string) should be either "source" or "destination"
        Scan the last 5 blocks of the source and destination chains
        Look for 'Deposit' events on the source chain and 'Unwrap' events on the destination chain
        When Deposit events are found on the source chain, call the 'wrap' function the destination chain
        When Unwrap events are found on the destination chain, call the 'withdraw' function on the source chain
    """

    # This is different from Bridge IV where chain was "avax" or "bsc"
    if chain not in ['source','destination']:
        print( f"Invalid chain: {chain}" )
        return 0

    w3 = connect_to(chain)
    other_chain = 'destination' if chain == 'source' else 'source'
    other_w3 = connect_to(other_chain)

    contracts = get_contract_info(chain, contract_info)
    other_contracts = get_contract_info(other_chain, contract_info)
    warden = get_contract_info('warden', contract_info)

    if not warden or warden.get("private_key", "").startswith("FILL_ME_IN"):
        print("Warden credentials missing")
        return 0

    contract = w3.eth.contract(address=Web3.to_checksum_address(contracts['address']), abi=contracts['abi'])
    other_contract = other_w3.eth.contract(address=Web3.to_checksum_address(other_contracts['address']), abi=other_contracts['abi'])

    latest_block = w3.eth.block_number
    start_block = max(latest_block - 4, 0)

    nonce = other_w3.eth.get_transaction_count(Web3.to_checksum_address(warden['address']))
    gas_price = other_w3.eth.gas_price
    warden_address = Web3.to_checksum_address(warden['address'])
    chain_id = other_w3.eth.chain_id

    if chain == 'source':
        events = contract.events.Deposit.get_logs(fromBlock=start_block, toBlock='latest')
        for event in events:
            args = event['args']
            tx = other_contract.functions.wrap(args['token'], args['recipient'], args['amount']).build_transaction({
                'from': warden_address,
                'nonce': nonce,
                'gasPrice': gas_price,
                'chainId': chain_id,
            })
            signed_tx = other_w3.eth.account.sign_transaction(tx, private_key=warden['private_key'])
            other_w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            nonce += 1
    else:
        events = contract.events.Unwrap.get_logs(fromBlock=start_block, toBlock='latest')
        for event in events:
            args = event['args']
            tx = other_contract.functions.withdraw(args['underlying_token'], args['to'], args['amount']).build_transaction({
                'from': warden_address,
                'nonce': nonce,
                'gasPrice': gas_price,
                'chainId': chain_id,
            })
            signed_tx = other_w3.eth.account.sign_transaction(tx, private_key=warden['private_key'])
            other_w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            nonce += 1
