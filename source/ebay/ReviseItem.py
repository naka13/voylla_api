print "Content-type: text/html"
print

#import the HTTP, DOM and ConfigParser modules needed
import httplib, ConfigParser, codecs
from xml.dom.minidom import parse, parseString
import sys
import os
import json

sku = sys.argv[1]
print sku

#print myList
#print len(sys.argv)
#print "skus_in is : " + skus_in
#print skus
qty = sys.argv[2]
print qty

#sku = skuList[0]
#quantity = qty[0]
#print sku
#print quantity

# open config file
config = ConfigParser.ConfigParser()
my_file = (os.path.join(os.getcwd(),'config.ini'))
config.read(my_file)

# specify eBay API dev,app,cert IDs
devID = "4d4a9e8e-bf21-472f-9ed3-3c539e824af5"
appID = "Voyllab4a-8867-4bc7-8f6a-dffa45ca38e"
certID = "c36f030c-6c06-48bc-a37f-4d3251be5e78"

#get the server details from the config file
serverUrl = "api.ebay.com"
serverDir = "/ws/api.dll"

# specify eBay token
# note that eBay requires encrypted storage of user data
userToken = "AgAAAA**AQAAAA**aAAAAA**cy+xUg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AFk4GkCJSKoQ2dj6x9nY+seQ**yQwCAA**AAMAAA**x70SWMJ5/4ALxfHZ7Gcg6jFduszVdBWher35BbrWSGlDQWA8Inrg00/7YOxKeYYQeYmGPw34+Dzm+JCaycyPkQr/C/GuuX2vw9BOaXpI46m2Hmg8n+gZuL7uBlsMVMmfKVvTy7ASUjIg7uaj4IGBDB68yGPe4MBkdpwaQFyziuGdzBjmEkzBejM1K24aqakFSfwGvuMHoWLxSdSRoB5AGE4oSdaZxSZLQZ60e8KAAg9crV7wVg9TazFzMPgAZIaFwT/R6suaJYdBptqdWpVp+BSTx3JXSr85yDz7vQsxsNi5pTQx5nKeV/Wy54uylhtFwnFxXJaQ7YBr7+9HUMuYq67mgXWr4u23G8IjeFMrYk4HDrp7pyV94FOrl9kesBWwxr59Rof8yxgdJ0/U3UEaIOuTbZavBjKAufqTXydiiVYo6JtQ6GlQKCwTSPvolOcygTiLvxMR/SNT2bgE82ym658BKzUx4L84avhq00zrxAy6lSV3FVJofq0vr297+8WbD6YzEvx2CKJn3lzV0Xc7/3Rvf0HBXI1yqdLLoFYvciR1RD5vywFRzfJIAzl/e4qM7B/cr08Iv45ICUucL499K/uqCU60cx5etciHWMwRB5e5tC2FZIb1N+dRHnwDbgH3uwku6doX+aEeo2nLmchZaw2mulxypOfHalcAm5op4d12rj0sBxGfT6/NsrrqljTyW5Uc3n3QM+S0qBjrevczxlF7GR1tBl4mdhkNU+J9ijN1KRWDy+/3Kvep/iGLdntE"


#eBay Call Variables
#siteID specifies the eBay international site to associate the call with
#0 = US, 2 = Canada, 3 = UK, ....
siteID = "203"
#verb specifies the name of the call
verb = "ReviseFixedPriceItem"
#The API level that the application conforms to
compatabilityLevel = "433"


#Setup the HTML Page with name of call as title
print "<HTML>"
print "<HEAD><TITLE>", verb, "</TITLE></HEAD>"
print "<BODY>"

#FUNCTION: reviseItem
# Lists an item on eBay
def reviseItem():
    # specify the connection to the eBay environment
    connection = httplib.HTTPSConnection(serverUrl)
    # specify a POST with the results of generateHeaders and generateRequest
    # detailLevel = 1, ViewAllNodes = 1  - this gets the entire tree
    connection.request("POST", serverDir, buildRequestXml("ReturnAll", "1"), buildHttpHeaders())
    response = connection.getresponse()
    if response.status != 200:
        print "Error sending request: " + response.reason
        exit
    else: #response successful
        # store the response data and close the connection
        data = response.read()
        connection.close()
        
        # parse the response data into a DOM
        response = parseString(data)
    
        # check for any Errors
        errorNodes = response.getElementsByTagName('Errors')
        if (errorNodes != []): #there are errors
            print "<P><B>eBay returned the following errors</B>"
            #Go through each error:
            for error in errorNodes:
                #output the error code and short message
                print "<P>" + ((error.getElementsByTagName('ErrorCode')[0]).childNodes[0]).nodeValue
                print " : " + ((error.getElementsByTagName('ShortMessage')[0]).childNodes[0]).nodeValue.replace("<", "&lt;")
                    #output Long Message if it exists (depends on ErrorLevel setting)
                if (error.getElementsByTagName('LongMessage')!= []):
                    print "<BR>" + ((error.getElementsByTagName('LongMessage')[0]).childNodes[0]).nodeValue.replace("<", "&lt;")

        else: #eBay returned no errors - output results
            # check for the <ItemID> tag and print
            if (response.getElementsByTagName('ItemID')!=[]):
                print "<P><B>Item ID is: "
                print ((response.getElementsByTagName('ItemID')[0]).childNodes[0]).nodeValue, "</B>"
        
        response.unlink()
        

# FUNCTION: buildHttpHeaders
# Build together the required headers for the HTTP request to the eBay API
def buildHttpHeaders():
    httpHeaders = {"X-EBAY-API-COMPATIBILITY-LEVEL": compatabilityLevel,
               "X-EBAY-API-DEV-NAME": devID,
               "X-EBAY-API-APP-NAME": appID,
               "X-EBAY-API-CERT-NAME": certID,
               "X-EBAY-API-CALL-NAME": verb,
               "X-EBAY-API-SITEID": siteID,
               "Content-Type": "text/xml"}
    return httpHeaders

# FUNCTION: buildRequestXml
# Build the body of the call (in XML) incorporating the required parameters to pass
def buildRequestXml(detailLevel, viewAllNodes):
    requestXml = "<?xml version='1.0' encoding='utf-8'?>"+\
              "<ReviseFixedPriceItemRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">"+\
              "<RequesterCredentials><eBayAuthToken>" + userToken + "</eBayAuthToken></RequesterCredentials>"
    
    if (detailLevel != ""):
        requestXml = requestXml + "<DetailLevel>" + detailLevel + "</DetailLevel>"
                     
    requestXml = requestXml + "<Item>"+\
				"<SKU>" + sku + "</SKU>"+\
				"<OutOfStockControl>true</OutOfStockControl>"+\
				"<Quantity>"+ str(qty) +"</Quantity>"+\
  				"</Item>"+\
              "</ReviseFixedPriceItemRequest>"
    #print requestXml
    return requestXml
    
reviseItem()
    

#finish HTML page
print "</BODY>"
print "</HTML>"
