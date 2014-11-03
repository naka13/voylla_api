import os
import shlex
import subprocess
import string
import sys
import json
import HTMLParser

h = HTMLParser.HTMLParser()

def reviseOnEbay(skus, qtys, parents, path):
	for index in range(len(skus)):
		sku = skus[index]
		qty = qtys[index]
		parent = parents[index]
		cmd = 'python2 ' + path + '/ReviseItem.py %s %s' % (sku,qty)
		print cmd
		args = shlex.split(cmd)
		#p = subprocess.Popen(args)
		#p.wait()
		p = subprocess.Popen(args, stdout=subprocess.PIPE)
		(stdout1, stderr1) = p.communicate()
		print h.unescape(stdout1)
		if sku != parent:
			cmd1 = 'python2 ' + path + '/ReviseItem1.py %s %s %s' % (sku,qty,parent)
			args1 = shlex.split(cmd1)
			p = subprocess.Popen(args1, stdout=subprocess.PIPE)
			(stdout1, stderr1) = p.communicate()
			print json.dumps(stdout1.encode("utf-8"))



