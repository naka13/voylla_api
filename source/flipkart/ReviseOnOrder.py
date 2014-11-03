import os
import shlex
import subprocess
import string
import sys
import json
import httplib
import urllib2

sellerID = "w9cnaikeqptlnvr7"
accessToken = "a93b763e-088b-4581-9b7c-49a3e6648eb9"


def reviseOnFlipkart(skus, qtys):
	for index in range(len(skus)):
		sku = skus[index]
		qty = qtys[index]
		reviseItem(sku, qty)


def reviseItem(sku, qty):
	serverUrl = "https://api.flipkart.net/sellers/skus/" + sku + "/listings"
	p = urllib2.HTTPPasswordMgrWithDefaultRealm()
	p.add_password(None, serverUrl, sellerID, accessToken)
	handler = urllib2.HTTPBasicAuthHandler(p)
	opener = urllib2.build_opener(handler)
	urllib2.install_opener(opener)
	req = urllib2.Request(serverUrl, buildRequest(sku, qty), {'content-type': 'application/json','Authorization': 'Basic dzljbmFpa2VxcHRsbnZyNzphOTNiNzYzZS0wODhiLTQ1ODEtOWI3Yy00OWEzZTY2NDhlYjk='})  # POST request doesn't not work
	response = urllib2.urlopen(req)
	print response.read()


def buildRequest(sku, qty):
	request = '{"skuId" : "%s" ,"attributeValues" :{"stock_count" : "%s"}}' %(sku,qty)
	json_request = json.dumps(request)
	print request
	return request