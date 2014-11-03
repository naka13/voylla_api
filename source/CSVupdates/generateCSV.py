import os
import shlex
import subprocess
import string
import sys
import json
from datetime import datetime


def reviseOnInfibeam(skus, qtys):
	stamp = datetime.now().strftime('%Y%m%d%H%M%S')
	filename = "stock_"+stamp+".csv"
	temp = open(filename,"w")
	temp.write('"SKU"'+","+'"Quantity"'+"\n")

	mydict = {"2-0":"2.0","2-2":"2.125","2-4":"2.25","2-6":"2.375","2-8":"2.5","2-10":"2.625","2-12":"2.75","2-14":"2.875"}

	for index in range(len(skus)):
		sku = skus[index].replace("_","-")
		sku1 = sku.split("-")
		if len(sku1) > 1:
			if sku1[1] in mydict:
				sku = sku1[0]+"-"+mydict[sku1[1]]
		qty = qtys[index]
		temp.write(sku+","+str(qty)+"\n")

	temp.close()

	print os.getcwd()
	cmd = 'scp ' + filename + ' root@staging.voylla.com:/home/voylla_update/Inventory_Update/'
	print cmd
	args = shlex.split(cmd)
	p=subprocess.Popen(args)
	p.wait()

	os.remove(filename)

