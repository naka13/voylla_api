import shlex
import subprocess
from datetime import datetime,timedelta,time
import os
import sys
import xml.etree.ElementTree as ET
import json
import ast
import time as time2
#from bs4 import BeautifulSoup
##BeautifulSoup is actually very beautiful, although I don't like soup!!
ListOrdersCounter = 0
ListOrderItemsCounter = 0

def checkNextToken(respTree):
	respRoot = respTree.getroot()
	respResults = respRoot.find("resp:ListOrdersResult", namespaces=namespaces)
	respNextToken = respResults.find("resp:NextToken", namespaces=namespaces)
	if respNextToken is not None:
		NextToken = respNextToken.text
		return NextToken
	else:
		return None

def checkNextToken1(respTree):
	respRoot = respTree.getroot()
	respResults = respRoot.find("resp:ListOrdersByNextTokenResult", namespaces=namespaces)
	respNextToken = respResults.find("resp:NextToken", namespaces=namespaces)
	if respNextToken is not None:
		NextToken = respNextToken.text
		return NextToken
	else:
		return None	

##handleNextToken recursively gets orders corresponding to NextToken and appends them to the previous response file
def handleNextToken(token, previousRespFileName, ListOrdersCounter):
	####generate response corresponding to the NextToken
	nextRespFileName = "nextResponse.xml"
	nextRespFile = open(respFilePath+nextRespFileName,"w")
	cmdNext = "php -f ListOrdersByNextToken.php %s" %(token)
	ListOrdersCounter += 1
	argsNext = shlex.split(cmdNext)
	pNext = subprocess.Popen(argsNext, stdout=subprocess.PIPE)
	(stdoutNext, stderrnext) = pNext.communicate()
	nextRespFile.write(stdoutNext)
	nextRespFile.close()
	if ListOrdersCounter >= 5:
		time2.sleep(65)
	mergeXML(respFilePath + previousRespFileName, respFilePath + nextRespFileName)

	####Now check if the response in nextRespFile has NextToken
	nextTree = ET.parse(respFilePath + nextRespFileName)
	nextToken = checkNextToken1(nextTree)
	if nextToken is not None:
		handleNextToken(nextToken, previousRespFileName, ListOrdersCounter)
	return ListOrdersCounter

##mergeXMLs(file1, file2) copies all the orders from file2 to file1
#def mergeXMLs(file1, file2, file3):
#	soup = BeautifulSoup(open(file1))						##with BeautifulSoup, you don't have to worry about namespace
#	insertion_point = soup.listordersresult.orders			##get the element where you want to insert orders, i.e"Orders" element
#
#	##get orders to be inserted from file2
#	orders_b = BeautifulSoup(open(file2)).listordersbynexttokenresult.orders
#	orders_to_insert = orders_b.find_all('order')
#
#	for order in orders_to_insert:
#		insertion_point.append(order)
#	#print(str(soup).replace("</body></html>","").replace('<html><body>',""))
#	xml_string = str(soup).replace("</body></html>","").replace('<html><body>',"")
#
#	f = open(file3,"w")
#	f.write(xml_string)
#	f.close()

def mergeXML(file1, file2):
	tree = ET.parse(file1)
	root = tree.getroot()

	results = root.find("resp:ListOrdersResult", namespaces=namespaces)
	order_array = results.find("resp:Orders", namespaces=namespaces).getchildren()

	tree1 = ET.parse(file2)
	root1 = tree1.getroot()

	results1 = root1.find("resp:ListOrdersByNextTokenResult", namespaces=namespaces)
	order_array1 = results1.find("resp:Orders", namespaces=namespaces).getchildren()

	for order in order_array1:
		order_array.append(order)

	tree.write("temp.xml")

	correct_data = open("temp.xml").read().replace('ns0:', '').replace(':ns0','')
	filewrite = open(file1, 'w')
	filewrite.write(correct_data)
	filewrite.close()


time_now = datetime.now()
hour_now = time_now.strftime('%H')

time_3 = time(3,0)
hour_3 = time_3.strftime('%H')

lookback_time = int(sys.argv[2]) + 6
##if time is 3a.m. lookback time is 78 (72 + 5:30 ~ 78) else 18 (12 + 5:30 ~ 18)
if hour_now == hour_3:
	time = (datetime.now()- timedelta(hours=78)).strftime('%Y-%m-%dT%H:%M:%S') 
else:
	time = (datetime.now()- timedelta(hours=lookback_time)).strftime('%Y-%m-%dT%H:%M:%S') 
#print time
#time = "2014-10-21T12:47:04+00:00"
#time1 = "2014-10-21T12:59:04+00:00"

path = sys.argv[1]
confirmed_orders = json.loads(sys.argv[3])
respFilePath = path + '/src/MarketplaceWebServiceOrders/Samples/'
#print path

os.chdir(respFilePath)
respFileName = "response.xml"
respFile = open(respFileName,"w")


##ListOrders API call would give order details for orders created after a given point of time
cmd = "php -f ListOrders.php %s" %(time)
ListOrdersCounter += 1
#cmd = "php -f ListOrders.php %s %s" %(time,time1)
#print cmd
args = shlex.split(cmd)
p = subprocess.Popen(args, stdout=subprocess.PIPE)
(stdout1, stderr) = p.communicate()
respFile.write(stdout1)
respFile.close()
#print stdout1


#print path1
namespaces = {'resp': 'https://mws.amazonservices.com/Orders/2013-09-01'}
tree = ET.parse(respFilePath+respFileName)
nextToken = checkNextToken(tree)
if nextToken is not None:
	ListOrdersCounter = handleNextToken(nextToken, respFileName, ListOrdersCounter)

tree = ET.parse(respFilePath+respFileName)
root = tree.getroot()
results = root.find("resp:ListOrdersResult", namespaces=namespaces)
nextToken = results.find("resp:NextToken", namespaces=namespaces)

order_array = results.find("resp:Orders", namespaces=namespaces)
#print order_array

amznIds = []
items = {}
skus = []
qtys = []
shipping = []
error = []
canceled = []

for child in order_array.findall('resp:Order', namespaces=namespaces):
	status = child.find("resp:OrderStatus", namespaces=namespaces).text
	#print status
	##skip FBA orders
	channel = child.find("resp:FulfillmentChannel", namespaces=namespaces).text
	if channel == "AFN":
		continue
	##only unshipped or pending orders considered for order creation
	amznId = child.find("resp:AmazonOrderId", namespaces=namespaces).text
	if status == "Unshipped" or status == "Pending":
		amznIds.append(amznId)
	if (status == "Canceled") and (hour_now == hour_3):
		canceled.append(amznId)


#print amznIds
for order in amznIds:
	if order in confirmed_orders:
		continue
	items[order] = []
	##ListOrderItems API call gives the item level details (sku, qty etc.) for a given amazon order number
	cmd = "php -f ListOrderItems.php %s" %(order)
	ListOrderItemsCounter += 1
	#print cmd
	args = shlex.split(cmd)
	p = subprocess.Popen(args, stdout=subprocess.PIPE)
	(stdout, stderr) = p.communicate()
	itemFile = open("items.xml","w")
	itemFile.write(stdout)
	itemFile.close()
	if ListOrderItemsCounter >= 29:
		time2.sleep(2)						##sleep for 2 seconds, restore rate for he API call is 1 request/2 secs
	try:
		tree = ET.parse(path + '/src/MarketplaceWebServiceOrders/Samples/items.xml')
	except ET.ParseError:
		error.append(order)
		continue
	root = tree.getroot()
	results = root.find("resp:ListOrderItemsResult", namespaces=namespaces)
	item_array = results.find("resp:OrderItems", namespaces=namespaces)
	for child in item_array.findall('resp:OrderItem', namespaces=namespaces):
		temp = {}
		sku = child.find("resp:SellerSKU", namespaces=namespaces).text
		skus.append(sku)
		qty = child.find("resp:QuantityOrdered", namespaces=namespaces).text
		qtys.append(qty)
		ship = child.find("resp:ShippingPrice", namespaces=namespaces)
		if ship is not None:
			ship_amount = float(ship.find("resp:Amount", namespaces=namespaces).text)
		else:
			ship_amount = "NA"
		temp["sku"] = sku
		temp["qty"] = qty
		temp["shipping"] = ship_amount
		#print temp
		#print sku
		#print qty
		items[order].append(temp)

cmd = "python2 %s/parse.py %s" %(path,path)
args = shlex.split(cmd)
p = subprocess.Popen(args, stdout=subprocess.PIPE)
(stdout, stderr) = p.communicate()
details = ast.literal_eval(stdout)
#print details

#print items
rdict = {}
def ret():
	rskus = json.dumps(skus)
	rqtys = json.dumps(qtys)
	rdict["skus"] = skus
	rdict["qtys"] = qtys
	rdict["items"] = items
	rdict["details"] = details
	rdict["error"] = error
	rdict["canceled"] = canceled
	#print rskus
	#print rqtys
	return json.dumps(rdict)
print ret()
