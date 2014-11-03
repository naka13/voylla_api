import os
from os import listdir
from os.path import isfile, join
import subprocess
import datetime
from datetime import datetime,timedelta
import shlex
import spur
import ast
import json
import sys

script_path = sys.argv[1]

FTP_SERVER = "ec2-54-251-85-20.ap-southeast-1.compute.amazonaws.com"
FTP_USER = "root"
FEED_LOCATION = "/home/snapdeal/Order_Feeds"
PROCESSED_FEED_LOCATION = "/home/snapdeal/Processed_Order_Feeds"
PREFIX = "SnapdealOrders"

def getFeeds():																####returns the list of feeds in FEED_LOCATION
	shell = spur.SshShell(hostname=FTP_SERVER, username=FTP_USER, private_key_file="/root/.ssh/id_rsa1.pub", missing_host_key=spur.ssh.MissingHostKey.accept)
	####refer to http://askubuntu.com/questions/306798/trying-to-do-ssh-authentication-with-key-files-server-refused-our-key for authentication errors.
	with shell:
		result = shell.run(["ls", FEED_LOCATION])
		feeds = result.output.decode().split("\n")
		#print(temp.split("\n"))
	return feeds


def moveFeed(feedName):
	shell = spur.SshShell(hostname=FTP_SERVER, username=FTP_USER, private_key_file="/root/.ssh/id_rsa1.pub", missing_host_key=spur.ssh.MissingHostKey.accept)
	with shell:
		shell.run(["cp", FEED_LOCATION+"/"+feedName, PROCESSED_FEED_LOCATION+"/"+feedName])
		

'''
mypath = "/home/nish/repos/lappy/snapdeal"
print mypath

files = []
for f in listdir(mypath):
	if isfile(join(mypath,f)):
		files.append(f)
####COULD BE DONE IN A SINGLE LINE:
#feeds = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
#dirs = [d for d in listdir(mypath) if not isfile(join(mypath,d))]
'''


details = {}

feeds = getFeeds()

for feed in feeds:
	if feed.startswith("Snapdeal") == False:
		continue
	time = feed.split("SnapdealOrders",1)[1].split(".")[0]
	if time.startswith("Last3days"):
		time = time.split("Last3days")[1]
	t1 = datetime.now()
	t2 = datetime.strptime(time,"%Y-%m-%d_%H:%M:%S")
	if (t1-t2) < timedelta(minutes=100):
		cmd = "scp %s@%s:%s/%s ." %(FTP_USER, FTP_SERVER, FEED_LOCATION,feed)       ####Get the feed from staging
		args = shlex.split(cmd)
		p = subprocess.Popen(args)
		p.wait()

		cmd1 = "python2 %s/parse.py %s" %(script_path, feed)										###Get the order details dictionary generated by parse.py
		args1 = shlex.split(cmd1)
		p = subprocess.Popen(args1, stdout=subprocess.PIPE)
		(stdout, stderr) = p.communicate()
		tempdetails = json.loads(stdout.decode())

		for key,value in tempdetails.items():										#For multiple feeds Check if its already in the hash. If yes, check status has changed
			if key in details:
				if value != details[key]:
					details[key] = value
			else:
				details[key] = value

		moveFeed(feed)
		#print(details)
		#cmd = "scp %s@%s:%s/%s %s@%s:%s/%s" %(FTP_USER, FTP_SERVER, FEED_LOCATION, feed, FTP_USER, FTP_SERVER, PROCESSED_FEED_LOCATION,feed)       ####Move the feed to PROCESSED_FEED_LOCATION
		#args = shlex.split(cmd)
		#p = subprocess.Popen(args)
		#p.wait()

print (json.dumps(details))
