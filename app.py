from flask import Flask, request, make_response
import os, sys
from flask.ext.sqlalchemy import SQLAlchemy
import json
import requests
import re
import pdb
from datetime import datetime,timedelta,time
import subprocess

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *
from lib.update import *

#@app.route("/get_orders", methods=["GET"])
def get_orders(time, zero=0):
	lookback_time = time
	response = {}
	if lookback_time is None:
		response["response_code"] = 0
		response["error_message"] = "Please specify a lookback time in request parameters"
		return json.dumps(response)
	else:
		lookback_time = int(lookback_time.decode("utf-8"))
	db_session = scoped_session(sessionmaker(bind=engine))
	skusEbay = []
	skusAmazon = []
	skus = []
	qty = []
	parentSkus = []
	done = []

	for order in db_session.query(Order).filter((datetime.now() - Order.updated_at) <= timedelta(minutes=lookback_time)):
		for lineitem in db_session.query(LineItem).filter(LineItem.order_id == order.id):
			for variant in db_session.query(Variant).filter(Variant.id == lineitem.variant_id):
				if variant in done:
					continue
				done.append(variant)
				if zero == 1:
					if variant.count_on_hand > 1:
						continue
				qty.append(variant.count_on_hand if variant.count_on_hand >=0 else 0)
				parentSkus.append(variant.sku)
				option_value = db_session.query(OptionValueVariant).filter(OptionValueVariant.variant_id == variant.id).first()
				if option_value is not None:
					size = db_session.query(OptionValue).filter(OptionValue.id == option_value.option_value_id).one().name
					if size == "adjustable" or size == "Adjustable" or size == "m" or size == "free size":
						skus.append(variant.sku)
						skusEbay.append(variant.sku)
					else:
						skus.append(variant.sku + "_" + size)
						skusEbay.append(variant.sku + size)
				else:
					skus.append(variant.sku)
					skusEbay.append(variant.sku)
	for sku in skus:
		amznsku = sku.split(".")[0]
		skusAmazon.append(amznsku)
	response["response_code"] = 1
	response["skus"] = skus
	response["skusEbay"] = skusEbay
	response["skusAmazon"] = skusAmazon
	response["parentSkus"] = parentSkus
	response["qtys"] = qty
	return response


@app.route('/')
def hello():
	return "Hello World!"


@app.route('/click_event', methods=["POST"])
def clicks():
	sku = request.args.get("sku")
	pattern = re.compile('([A-Z]{5})(\d{5})')
	if pattern.match(sku):
		entry = db.session.query(Product).filter(Product.sku==sku).first()
		if entry is None:
			new_product = Product(sku=sku, clicks=1, buys=0, cart_adds=0)
			db.session.add(new_product)
			db.session.commit()
			return json.dumps(new_product)
		else:
			entry.clicks += 1
			db.session.add(entry)
			db.session.commit()
			return json.dumps(entry.clicks)
		db.session.flush()
	else:
		return "Not Found! Invalid sku"


@app.route('/buy_event', methods=["POST"])
def buys():
	sku = request.args.get("sku")
	pattern = re.compile('([A-Z]{5})(\d{5})')
	if pattern.match(sku):
		entry = db.session.query(Product).filter(Product.sku==sku).first()
		if entry is None:
			new_product = Product(sku=sku, clicks=0, buys=1, cart_adds=0)
			db.session.add(new_product)
			db.session.commit()
			return json.dumps(new_product)
		else:
			entry.buys += 1
			db.session.add(entry)
			db.session.commit()
			return json.dumps(entry.buys)
		db.session.flush()
	else:
		return "Not Found!  Invalid sku"


@app.route('/cart_addition', methods=["POST"])
def cart_adds():
	sku = request.args.get("sku")
	pattern = re.compile('([A-Z]{5})(\d{5})')
	if pattern.match(sku):
		entry = db.session.query(Product).filter(Product.sku==sku).first()
		if entry is None:
			new_product = Product(sku=sku, clicks=0, buys=0, cart_adds=1)
			db.session.add(new_product)
			db.session.commit()
			return json.dumps(new_product)
		else:
			entry.cart_adds += 1
			db.session.add(entry)
			db.session.commit()
			return json.dumps(entry.cart_adds)
		db.session.flush()
	else:
		return "Not Found! Invalid sku"


@app.route('/glances', methods=["POST"])
def glances():
	skus = request.args.get("skus").decode("utf-8").split(",")

	pattern = re.compile('([A-Z]{5})(\d{5})')
	skus = [sku for sku in skus if pattern.match(sku)]

	for sku in skus:
		entry = db.session.query(Product).filter(Product.sku==sku).first()
		if entry is None:
			new_product = Product(sku=sku, clicks=0, buys=0, cart_adds=0, glances=1)
			db.session.add(new_product)
			db.session.commit()
		else:
			entry.glances += 1
			db.session.add(entry)
			db.session.commit()
	db.session.flush()
	return json.dumps(skus)


@app.route('/download')
def download():
	products = db.session.query(Product).all()
	header = "SKU,Clicks,Buys,Cart Additions,Glances\n"
	rows = []
	for product in products:
		row = ",".join([product.sku,str(product.clicks),str(product.buys),str(product.cart_adds),str(product.glances)])
		rows.append(row)
	rows="\n".join(rows)
	response = make_response(header+rows)
	response.headers["Content-Disposition"] = "attachment; filename=report.csv"
	return response


@app.route('/update')
def update():
	time = request.args.get("time")
	zero = request.args.get("zero")
	details = get_orders(str(time),int(zero))
	skus = ([str(x) for x in details["skus"]])
	skusAmazon = ([str(x) for x in details["skusAmazon"]])
	skusEbay = ([str(x) for x in details["skusEbay"]])
	parentSkus = ([str(x) for x in details["parentSkus"]])
	qtys = details["qtys"]
	ebay_resp = updateEbay(skusEbay,parentSkus,qtys)
	amzn_resp = updateAmazon(skus, qtys)
	snapdeal_resp = updateSnapdeal(skus, qtys)
	fk_resp = updateFlipkart(skus, skusAmazon, qtys)
	ib_resp = updateInfibeam(skus, qtys)
	sk_resp = updateStoreking(skus, qtys)
	jun_resp = updateJunglee(skus, qtys)
	sc_resp = updateShopclues(skus, qtys)
	unbxd_resp = updateUnbxd(parentSkus, qtys)
	return "\n\n<br>\n\n<br>".join([ebay_resp, amzn_resp, snapdeal_resp, fk_resp, ib_resp, sk_resp, jun_resp, sc_resp, unbxd_resp])


def dbinit():
	db.create_all()
	db.session.commit()


if __name__ == '__main__':
	dbinit()
	app.run()