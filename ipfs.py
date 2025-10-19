import json
import os

import requests

def pin_to_ipfs(data):
	# "pin_to_ipfs()" which takes a Python dictionary, 
	# and stores the dictionary (as JSON) on IPFS. 
	# The function should return the Content Identifier (CID) of the data stored.

	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	api_key = '371f89fc5df6d0e26488'
	api_secret = 'd7f98041357cf2a044ee0cebf4d9658201447cb64f3a612d72858d8bd19c1a34'
	url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
	payload = json.dumps(data, separators=(',', ':'))
	headers = {
	    'Content-Type': 'application/json',
	    'pinata_api_key': api_key,
	    'pinata_secret_api_key': api_secret,
	}
	response = requests.post(url, data=payload, headers=headers)
	assert response.status_code == 200, f"pin_to_ipfs failed with status code {response.status_code}"
	cid = response.json()['IpfsHash']
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
