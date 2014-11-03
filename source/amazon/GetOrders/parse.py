import xml.etree.ElementTree as ET
import json
import sys
import difflib

states_possible = ["Chhattisgarh","Goa","Sikkim","Meghalaya","Tamil Nadu","Jammu and Kashmir","Madhya Pradesh","Rajasthan","Uttar Pradesh","Uttrakhand","Andhra Pradesh","Dadra and Nagar Haveli","Army Post Office","Nagaland","Jharkhand","Lakshadweep","Maharashtra","Mizoram","Punjab","West Bengal","Tripura","Himachal Pradesh","Arunachal Pradesh","Karnataka","Gujarat","Manipur","Odisha","Haryana","Assam","Chandigarh","Daman and Diu","Andaman and Nicobar","Bihar","Kerala","Pondicherry","Delhi"]

path = sys.argv[1]
orderList = open("list","w")
def parse():
	tree = ET.parse(path+"/src/MarketplaceWebServiceOrders/Samples/response.xml")
	root = tree.getroot()
	namespaces = {'resp': 'https://mws.amazonservices.com/Orders/2013-09-01'}
	results = root.find("resp:ListOrdersResult", namespaces=namespaces)
	order_array = results.find("resp:Orders", namespaces=namespaces)
	#print order_array
	detailsList = []
	i=0
	for order in order_array.findall('resp:Order', namespaces=namespaces):
		status = order.find('resp:OrderStatus', namespaces=namespaces).text
		#print status
		#if status != "Unshipped":
		#	continue
		details = {}
		details['status'] = status
		amazon_id = order.find('resp:AmazonOrderId', namespaces=namespaces).text
		details['amazon_id'] = amazon_id
		#print amazon_id
		channel = order.find('resp:FulfillmentChannel', namespaces=namespaces).text
		details['channel'] = channel
		#print channel
		address = order.find('resp:ShippingAddress', namespaces=namespaces)
		#print address
		if address is not None:
			name = address.find('resp:Name', namespaces=namespaces).text
			details['name']= name
			address_1 = address.find('resp:AddressLine1', namespaces=namespaces).text
			address_2 = address.find('resp:AddressLine2', namespaces=namespaces)
			if address_2 is not None:
				address_2 = address_2.text
			details['address_1']=address_1
			details['address_2']=address_2
			city = address.find('resp:City', namespaces=namespaces).text
			details['city']= city
			state = address.find('resp:StateOrRegion', namespaces=namespaces)
			if state is not None:
				state = state.text
			else:
				state = "Maharashtra"
			if state not in states_possible:
				state_val = difflib.get_close_matches(state.lower(),states_possible)
				if state_val:
					state = state_val[0]
			details['state']=state
			countryCode = address.find('resp:CountryCode', namespaces=namespaces).text
			details['countryCode']=countryCode
			phone = address.find('resp:Phone', namespaces=namespaces).text
			details['phone']=phone
			postalCode = address.find('resp:PostalCode', namespaces=namespaces).text
			details['postalCode']=postalCode
		else:
			details['name'] = "NA"
			details['address_1'] = "NA"
			details['address_2'] = "NA"
			details['city'] = "NA"
			details['state'] = "NA"
			details['countryCode'] = "NA"
			details['phone'] = "NA"
			details['postalCode'] = "NA"
		payment_method_element = order.find('resp:PaymentMethod', namespaces=namespaces)
		if payment_method_element is not None:
			payment_method = payment_method_element.text
		else:
			payment_method = "COD"
		#print payment_method
		details['payment_method'] = payment_method
		service = order.find('resp:ShipmentServiceLevelCategory', namespaces=namespaces).text
		#print service
		details['service'] = service
		#shipped_by_amazon = order.find('resp:ShippedByAmazonTFM', namespaces=namespaces).text
		#print shippied_by_amazon
		#details['shipped_by_amazon'] = shipped_by_amazon
		order_type = order.find('resp:OrderType', namespaces=namespaces).text
		details['order_type'] = order_type
		#print order_type
		buyer_name_element = order.find('resp:BuyerName', namespaces=namespaces)
		if buyer_name_element is not None:
			details['buyer_name'] = buyer_name_element.text
		else:
			details["buyer_name"] = "NA"
		order_total = order.find('resp:OrderTotal', namespaces=namespaces)
		if order_total is not None:
			total = order_total.find('resp:Amount', namespaces=namespaces).text
		else:
			total = "NA"
		details["amount"] = total
		#print details
		detailsList.append(details)
	#print detailsList
	#output = json.dumps(detailsList)
	#print "Output is: " + str(output)
	return detailsList

print parse()
