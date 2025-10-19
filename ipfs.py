import json
import requests

def pin_to_ipfs(data):
    assert isinstance(data, dict), "pin_to_ipfs expects a dictionary"

    PINATA_API_KEY = "c0d75aa88a2180a5a0bf"
    PINATA_API_SECRET = "8dc58b052cb23cbba3f7225c9e912dcbdd7eee28deda82926c84e74a9ccc989e"

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    body = {"pinataContent": data}
    headers = {
        "Content-Type": "application/json",
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_API_SECRET
    }

    response = requests.post(url, json=body, headers=headers)

    assert response.status_code == 200, (f"pin_to_ipfs failed with status code {response.status_code}: {response.text}")

    return response.json()["IpfsHash"]



def get_from_ipfs(cid,content_type="json"):
    assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
    url = f"https://ipfs.infura.io/ipfs/{cid}"
    response = requests.get(url)
    assert response.status_code == 200, f"get_from_ipfs failed with status code {response.status_code}"
    if content_type=="json":
        data = response.json()
    else:
        data = response.content

    assert isinstance(data,dict), f"get_from_ipfs should return a dict"
    return data
