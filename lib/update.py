import contextlib, StringIO
import inspect, os, sys

from source.ebay.ReviseOnOrder import reviseOnEbay
from source.amazon.ReviseOnOrder import reviseOnAmazon
from source.snapdeal_limeroad_paytm.GenerateXML import generateXML
from source.flipkart.ReviseOnOrder import reviseOnFlipkart
from source.CSVupdates.generateCSV import reviseOnInfibeam
from source.storeking.GenerateXML import reviseOnStoreking
from source.junglee.update_using_MWS import reviseOnJunglee
from source.shopclues.ReviseOnOrder import reviseOnShopclues
from source.unbxd.ReviseOnOrder import reviseOnUnbxd


@contextlib.contextmanager
def stdout_redirect(where):
    sys.stdout = where
    try:
        yield where
    finally:
        sys.stdout = sys.__stdout__


def updateEbay(skusEbay, parentSkus, qtys):
	mod = inspect.getmodule(reviseOnEbay)
	path =  os.path.abspath(mod.__file__).split("/")
	path.pop()
	path = "/".join(path)
	with stdout_redirect(StringIO.StringIO()) as ebay_stdout:
		reviseOnEbay(skusEbay, qtys, parentSkus, path)
	ebay_stdout.seek(0)
	return ebay_stdout.read()


def updateAmazon(skus, qtys):
	mod = inspect.getmodule(reviseOnAmazon)
	path = os.path.abspath(mod.__file__).split("/")
	path.pop()
	path = "/".join(path)
	with stdout_redirect(StringIO.StringIO()) as amzn_stdout:
		reviseOnAmazon(skus, qtys, path)
	amzn_stdout.seek(0)
	return amzn_stdout.read()


def updateSnapdeal(skus, qtys):
	with stdout_redirect(StringIO.StringIO()) as snapdeal_stdout:
		generateXML(skus, qtys)
	snapdeal_stdout.seek(0)
	return snapdeal_stdout.read()


def updateFlipkart(skus, skusAmazon, qtys):
	with stdout_redirect(StringIO.StringIO()) as fk_stdout:
		reviseOnFlipkart(skus, qtys)
		reviseOnFlipkart(skusAmazon, qtys)
	fk_stdout.seek(0)
	return fk_stdout.read()


def updateInfibeam(skus, qtys):
	with stdout_redirect(StringIO.StringIO()) as infi_stdout:
		reviseOnInfibeam(skus, qtys)
	infi_stdout.seek(0)
	return infi_stdout.read()


def updateStoreking(skus, qtys):
	with stdout_redirect(StringIO.StringIO()) as sk_stdout:
		reviseOnStoreking(skus, qtys)
	sk_stdout.seek(0)
	return sk_stdout.read()


def updateJunglee(skus, qtys):
	mod = inspect.getmodule(reviseOnAmazon)
	path = os.path.abspath(mod.__file__).split("/")
	path.pop()
	path = "/".join(path)
	with stdout_redirect(StringIO.StringIO()) as jun_stdout:
		reviseOnJunglee(skus, qtys, path)
	jun_stdout.seek(0)
	return jun_stdout.read()


def updateShopclues(skus, qtys):
	with stdout_redirect(StringIO.StringIO()) as sc_stdout:
		reviseOnShopclues(skus, qtys)
	sc_stdout.seek(0)
	return sc_stdout.read()

def updateUnbxd(skus, qtys):
	with stdout_redirect(StringIO.StringIO()) as unbxd_stdout:
		reviseOnUnbxd(skus, qtys)
	unbxd_stdout.seek(0)
	return unbxd_stdout.read()