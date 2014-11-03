import os
import shlex
import subprocess
import string
import sys
import json


def reviseOnAmazon(skus, qtys, path):
	os.chdir(path + '/src/MarketplaceWebService/Samples')
	xml = ""
	for index in range(len(skus)):
		sku = skus[index]
		qty = qtys[index]
		xml = xml + "<Message><MessageID>%s</MessageID><OperationType>Update</OperationType><Inventory><SKU>%s</SKU><Quantity>%s</Quantity></Inventory></Message>" %(index+1,sku,qty)

	print xml
	cmd = 'php -f ReviseItem.php %s' % (xml)
	print cmd
	args = shlex.split(cmd)
	p=subprocess.Popen(args, stdout=subprocess.PIPE)
	(stdout1, stderr1) = p.communicate()
	print stdout1