import subprocess

API_KEY = "2054707c59e84e6183c358569660fcae"
SITE_ID = "voylla_com-u1407152338954"

def reviseOnUnbxd(skus, qtys):
	f = open("update.xml","w")
	f.write('<?xml version="1.0" encoding="UTF-8"?><feed> <catalog> <update>'+"\n")
	for index in range(len(skus)):
		if qtys[index] > 0:
			availability = "true"
		else:
			availability = "false"
		f.write("	<items>\n")
		f.write("		<uniqueId>%s</uniqueId>\n" %(skus[index]))
		f.write("		<availability>%s</availability>\n" %(availability))
		f.write("	</items>\n")
	f.write('</update> </catalog> </feed>')
	f.close()
	cmd = 'curl -F "file=@update.xml"' + " http://feed.unbxdapi.com/upload/v2/%s/%s" % (API_KEY, SITE_ID)
	response = subprocess.check_output(cmd, shell=True)
	print response

	os.remove(update.xml)