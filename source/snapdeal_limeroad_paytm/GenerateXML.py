import os
import shlex
import subprocess
import string
import sys
import json
from datetime import datetime

def generateXML(skus, qtys):
	stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	filename = "update"+stamp+".xml"
	temp = open(filename,"w")
	temp.write('<?xml version="1.0"?>\n')
	temp.write("<ListingItems>\n")

	for index in range(len(skus)):
		sku = skus[index]
		qty = qtys[index]
		temp.write("<Item>\n")
		temp.write("<SKU>"+sku+"</SKU>\n")
		temp.write("<Quantity>"+str(qty)+"</Quantity>\n")
		temp.write("</Item>\n\n\n")

	temp.write("</ListingItems>")
	temp.close()


	print os.getcwd()
	cmd = 'scp ' + filename + ' root@staging.voylla.com:/srv/ftp/'
	#cmd = 'scp ' + filename + ' root@staging.voylla.com:/srv/ftp/'
	print cmd
	args = shlex.split(cmd)
	p=subprocess.Popen(args)
	p.wait()


	cmd = 'scp ' + filename + ' root@staging.voylla.com:/home/limeroad/inventory/'
	#cmd = 'scp ' + filename + ' root@staging.voylla.com:/home/limeroad/'
	print cmd
	args = shlex.split(cmd)
	p=subprocess.Popen(args)
	p.wait()


	cmd = 'scp ' + filename + ' root@staging.voylla.com:/home/voylla_paytm/Inventory_Update/'
	#cmd = 'scp ' + filename + ' root@staging.voylla.com:/home/voylla_paytm/'
	print cmd
	args = shlex.split(cmd)
	p=subprocess.Popen(args)
	p.wait()


	os.remove(filename)