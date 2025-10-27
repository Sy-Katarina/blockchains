import json
import os
import requests
from web3.providers.rpc import HTTPProvider
from web3 import Web3

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)

# You will need the ABI to connect to the contract
# The file 'abi.json' has the ABI for the bored ape contract
# In general, you can get contract ABIs from etherscan
# https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('ape_abi.json', 'r') as f:
    abi = json.load(f)

############################
# Connect to an Ethereum node
api_url = "https://eth-mainnet.g.alchemy.com/v2/HsxlNSRWmG18AxY5MziZM"  # YOU WILL NEED TO PROVIDE THE URL OF AN ETHEREUM NODE
provider = HTTPProvider(api_url)
web3 = Web3(provider)
contract = web3.eth.contract(address=contract_address, abi=abi)


def _fetch_ipfs_json(uri: str) -> dict:
    if uri.startswith("ipfs://"):
        path = uri[7:]
        uri = f"https://gateway.pinata.cloud/ipfs/{path}"

    response = requests.get(uri, timeout=20)
    response.raise_for_status()
    return response.json()


def get_ape_info(ape_id):
    assert isinstance(ape_id, int), f"{ape_id} is not an int"
    assert 0 <= ape_id, f"{ape_id} must be at least 0"
    assert 9999 >= ape_id, f"{ape_id} must be less than 10,000"

    owner = contract.functions.ownerOf(ape_id).call()
    token_uri = contract.functions.tokenURI(ape_id).call()
    metadata = _fetch_ipfs_json(token_uri)

    image_uri = metadata.get("image", "")
    eyes_value = ""
    for trait in metadata.get("attributes", []):
        if trait.get("trait_type") == "Eyes":
            eyes_value = trait.get("value", "")
            break

    data = {'owner': owner, 'image': image_uri, 'eyes': eyes_value}

    assert isinstance(data, dict), f'get_ape_info{ape_id} should return a dict'
    assert all([a in data.keys() for a in
                ['owner', 'image', 'eyes']]), f"return value should include the keys 'owner','image' and 'eyes'"
    return data
