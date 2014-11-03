#!/home/nish/.rvm/rubies/ruby-1.9.2-p320/bin/ruby

require 'json'
skus = []
skus.push("ABPNQ20025")

qty = []
qty.push("7")


sku = skus.to_s
print sku
qtys = qty.to_s
print qtys

path = File.expand_path('../', __FILE__)
print path

system "python2 " + path + "/ReviseOnOrder.py #{sku.to_json} #{qtys.to_json} #{path}"
