import os
import shlex
import subprocess
import string
import sys
import json
from datetime import datetime


def reviseOnStoreking(skus, qtys):
	stamp = datetime.now().strftime('%Y%m%d%H%M%S')
	filename = "stock_"+stamp+".xml"
	temp = open(filename,"w")
	temp.write('<?xml version="1.0"?>\n')
	temp.write("<inventory_data>\n")

	for index in range(len(skus)):
		sku = skus[index]
		qty = qtys[index]
		temp.write("<product>\n")
		temp.write("<SKU>"+sku+"</SKU>\n")
		temp.write("<Quantity>"+str(qty)+"</Quantity>\n")
		temp.write("</product>\n\n\n")

	temp.write("</inventory_data>")
	temp.close()

	print os.getcwd()
	cmd = 'scp ' + filename + ' root@staging.voylla.com:/home/storeking/stock/'
	print cmd
	args = shlex.split(cmd)
	p=subprocess.Popen(args)
	p.wait()

	os.remove(filename)
