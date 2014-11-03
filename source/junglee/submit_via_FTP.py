import paramiko
import sys
import json
from datetime import datetime

host = "dar-eu.amazon-digital-ftp.com"
port = 22
transport = paramiko.Transport((host, port))

password = "z1NC4mNsAM"
username = "M_VOYLLA_117512524"

csvdata = json.loads(sys.argv[1])

stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

File = "update_%s.txt" %(stamp)
f = open(File,"w")

csvdata_flat = []
for sublist in csvdata:
	if isinstance(sublist,list):
		for item in sublist:
			csvdata_flat.append(item)
	else:
		csvdata_flat.append(sublist)
#[sublist if isinstance(sublist,list) for sublist in csvdata else item for item in sublist]

f.write(str("\n".join(csvdata_flat)))
f.close()
transport.connect(username = username, password = password)

sftp = paramiko.SFTPClient.from_transport(transport)

sftp.put(File,File)

sftp.close()
transport.close()
print( 'Upload successful')