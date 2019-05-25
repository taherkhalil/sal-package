# -*- coding: utf-8 -*-
# Copyright (c) 2017, taher and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe, erpnext
from frappe.utils import today,getdate
from datetime import datetime, timedelta, date   
from frappe.utils import cint, flt
import json
from erpnext.controllers.accounts_controller import validate_conversion_rate, \
	validate_taxes_and_charges, validate_inclusive_tax
from frappe import _, scrub
from frappe.model.document import Document
from erpnext.controllers.taxes_and_totals import calculate_taxes_and_totals


class Packages(Document):
	def validate(self):
		package = self.package_name
		cost = self.package_cost
		income_account =self.income_account
		selling_cost_center= self.selling_cost_center
		item_doctype = frappe.db.sql("select name from tabItem", as_list=1)
		i_d = [x[0] for x in item_doctype]

		if not package in i_d:
			it = frappe.new_doc("Item")
			it.item_code = package
			it.item_group = "Packages"
			it.standard_rate = cost
			it.is_stock_item = 0
			it.income_account = income_account
			it.selling_cost_center = selling_cost_center
			it.insert(ignore_permissions=True)
			it.save()

@frappe.whitelist()
def package_buy(doc, method):
	customer = doc.customer
	tday= today()
	flag =False
	pacakage_list =frappe.db.sql("select package_name from tabPackages",as_list=1)
	pl= [x[0] for x in pacakage_list]

	for p in doc.get("items"):
  		cwp = frappe.db.sql("select * from `tabCustomer wise package",as_list=1)
  		check= [x[0] for x in cwp]
	
  		for c in check:
  			cp = frappe.get_doc("Customer wise package",c)
  			aaj = date.today().strftime('%Y-%m-%d')
  			end_date = date.strftime(cp.valid_to,'%Y-%m-%d')
  			
  			if customer == cp.customer and p.item_code == cp.services and cp.quantity_issued != cp.used_qty and aaj < end_date: 
  				doc.package_name = cp.package
  				# cp.used_qty =cp.used_qty +p.qty
  				# cp.save()
  				flag =True
				break

def on_submit(doc, method):
	customer = doc.customer
	tday= today()
	flag =False
	pacakage_list =frappe.db.sql("select package_name from tabPackages",as_list=1)
	pl= [x[0] for x in pacakage_list]

	for p in doc.get("items"):

		if p.item_code in pl:
			mem = frappe.get_doc("Packages", p.item_code)
			if mem.is_enabled:
				flag=True

				for it in mem.get("services"):
					cp = frappe.new_doc("Customer wise package")
					cp.customer = customer
					cp.package = p.item_code
					cp.services = it.services
					cp.quantity_issued = it.number_of_services
					cp.valid_from = datetime.strptime(tday, "%Y-%m-%d")
					if it.validity != 0:
						cp.valid_to = cp.valid_from + timedelta(days = it.validity)
					else:
						cp.valid_to = cp.valid_from + timedelta(days = 999)

					cp.used_qty = 0 
  		 			cp.insert(ignore_permissions=True)
  		 			cp.save()
  		 	else:
  		 		frappe.msgprint("Package inactive")
  		cwp = frappe.db.sql("select * from `tabCustomer wise package",as_list=1)
  		check= [x[0] for x in cwp]
	
  		for c in check:
  			cp = frappe.get_doc("Customer wise package",c)
  			aaj = date.today().strftime('%Y-%m-%d')
  			end_date = date.strftime(cp.valid_to,'%Y-%m-%d')
  			
  			if customer == cp.customer and p.item_code == cp.services and cp.quantity_issued >= cp.used_qty and aaj < end_date: 
  				doc.package_name = cp.package
  				cp.used_qty =cp.used_qty +p.qty
  				cp.remaining_qty = cp.quantity_issued - cp.used_qty
  				cp.save()
  				flag =True
				break


	settings = frappe.get_doc("Package Settings","Package Settings")
	# acc = "Advances From Customer - IBS"
	# sales ="Sales - IBS"
	acc = settings.customer_advance_account
	sales =settings.sales_account
	total_qty = 0
	if doc.package_name != "none":
		p = frappe.get_doc("Packages",doc.package_name)
		cost = p.package_cost
		total_services=0
		for s in p.get("services"):
			total_services +=s.number_of_services
		# frappe.errprint(total_services)
		per_service_cost = float(cost)/float(total_services)

		for it in doc.get("items"):
			if it.amount ==0:
				total_qty = total_qty +it.qty

		je = frappe.new_doc("Journal Entry") #create jv to add sales
		je.posting_date = getdate()
		je.company = doc.company
		je.bill_no = doc.name
		je.reference_date = getdate()
		row1 = je.append("accounts", {})
		row1.account= acc
		row1.party_type = "Customer"
		row1.party = doc.customer
		row1.debit_in_account_currency = per_service_cost*total_qty
		row1.credit_in_account_currency = 0.0

		row2 = je.append("accounts", {})
		row2.account = sales
		row2.party_type = "Customer"
		row2.party = doc.customer
		row2.debit_in_account_currency = 0.0
		row2.credit_in_account_currency = per_service_cost*total_qty
		je.insert(ignore_permissions=True)
		je.submit()

@frappe.whitelist()
def from_pos_call(doc,customer,item,qty):
	# frappe.errprint([customer,item])
	cwp = frappe.db.sql("select * from `tabCustomer wise package",as_list=1)
	check= [x[0] for x in cwp]
	# frappe.errprint(check)

	for c in check:
		cp = frappe.get_doc("Customer wise package",c)
		aaj = date.today().strftime('%Y-%m-%d')
		end_date = date.strftime(cp.valid_to,'%Y-%m-%d')
	
		if customer == cp.customer and item == cp.services and cp.quantity_issued >= int(int(cp.used_qty)+int(qty)) and aaj < end_date: 
  			# frappe.msgprint("call me")
  			# cp.used_qty =cp.used_qty +1 
  			# cp.save()
  			return cp.package
