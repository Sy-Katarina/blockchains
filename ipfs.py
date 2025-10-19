import json
import requests
import os

def pin_to_ipfs(data):
    assert isinstance(data, dict), "pin_to_ipfs expects a dictionary"
    PINATA_JWT = os.environ.get("PINATA_JWT", "")

    PINATA_API_KEY = os.environ.get("PINATA_API_KEY", "")
    PINATA_API_SECRET = os.environ.get("PINATA_API_SECRET", "")

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    body = {"pinataContent": data} 
    headers = {}
    if PINATA_JWT:
        headers["Authorization"] = f"Bearer {PINATA_JWT}"
    else:
        headers["pinata_api_key"] = PINATA_API_KEY
        headers["pinata_secret_api_key"] = PINATA_API_SECRET

    response = requests.post(url, json=body, headers=headers)
    assert response.status_code == 200, f"pin_to_ipfs failed with status code {response.status_code}: {response.text}"
    cid = response.json()["IpfsHash"]
    return cid


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


