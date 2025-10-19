import json
import requests
import os

def pin_to_ipfs(data):
    assert isinstance(data, dict), "pin_to_ipfs expects a dictionary"
    PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI2NjhlYWU3OS00N2MyLTQ0YjgtYWI1Yi0xOTBkMDY4NmZlM2QiLCJlbWFpbCI6Imthbm5hMDQ5QHNlYXMudXBlbm4uZWR1IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiRlJBMSJ9LHsiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiTllDMSJ9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjVmN2U1ZDQyZjUxN2MxZjc0ZWQwIiwic2NvcGVkS2V5U2VjcmV0IjoiZmE4ODdiNzA3NTZlMzUwMmQ3MjNhOWM2NmNjY2I4NjJiZWQ0ZjI5M2QzYjJhYWVlMzM4NTI4ODIwNWQ4YzE0YyIsImV4cCI6MTc5MjM5ODU2NX0.GHEWtqGi28s-hIhaL2WlSFeKeWae0WzQOUlSTQ9FshU"

    PINATA_API_KEY = "5f7e5d42f517c1f74ed0"
    PINATA_API_SECRET = "fa887b70756e3502d723a9c66cccb862bed4f293d3b2aaee3385288205d8c14c"

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


