import xml.etree.ElementTree as ET
import sys
import json

feedname = sys.argv[1]

def parse(feed):
	tree = ET.parse(feed)
	root = tree.getroot()

	details = {}

	for child in root:
		orderNum = child.find("OrderNum").text
		items = []
		details[orderNum] = {}
		suborders = child.find("SubOrders")
		orderStatus = "Confirmed"
		for suborder in suborders.findall("SubOrder"):
				temp = {}
				subordernum = suborder.find("SubOrderNumber").text
				temp["sub_order_id"] = subordernum
				sku = suborder.find("SKU").text
				temp["sku"] = sku
				quantity = suborder.find("Quantity").text
				temp["quantity"] = quantity
				price = suborder.find("Price").text
				temp["price"] = int(price)
				refCode = suborder.find("ReferenceCode").text
				temp["ref_code"] = refCode
				items.append(temp)
				status = suborder.find("Status").text
				if status == "Pending":
						orderStatus = "Pending"
				createdDate = suborder.find("CreatedDate").text
				verifiedDate = suborder.find("VerifiedDate").text
		email = child.find("EmailId").text
		phone = child.find("MobileNum").text
		add1 = child.find("Address1").text
		add2 = child.find("Address2").text
		city = child.find("City").text
		pin = child.find("Pincode").text
		state = child.find("State").text
		country = child.find("Country").text
		customer_name = child.find("CustomerName").text
		details[orderNum]["OrderNum"] = orderNum
		details[orderNum]["RefCode"] = refCode
		details[orderNum]["status"] = orderStatus
		details[orderNum]["items"] = items
		details[orderNum]["email"] = email
		details[orderNum]["phone"] = phone
		details[orderNum]["address_1"] = add1
		details[orderNum]["address_2"] = add2
		details[orderNum]["city"] = city
		details[orderNum]["postalCode"] = pin
		details[orderNum]["state"] = state
		details[orderNum]["country"] = country
		details[orderNum]["customer_name"] = customer_name
	return json.dumps(details)

print (parse(feedname))													####To be piped to shell