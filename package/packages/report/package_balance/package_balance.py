# Copyright (c) 2013, taher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, cint, getdate
from frappe import msgprint, _

def execute(filters=None):
	if not filters:
		filters = {}
	# columns, data = [], []

	conditions, filters = get_conditions(filters)
	columns = get_column()
	data = get_data(conditions,filters)

	return columns, data

def get_column():
	columns = [ 
		_("posting_date") + ":Date:120",
		_("Customer") + ":Link/Customer:150",
		_("Invoice") + ":Link/Sales Invoice:120",
		_("Package") + ":Link/Packages",
		_("Service") + ":Link/Item:120",
		_("Attended_by") + "Link/Service Providers:120",
		_("Quantity Used") + ":Data:100",
		_("Total Used") + ":Data:100",
		_("Balance Quantity") + ":Data:100"
		]
	return columns

def get_data(conditions,filters):
	invoices = frappe.db.sql("""select posting_date,name, customer,package_name, grand_total from `tabSales Invoice` where 
		package_name != 'none' %s order by posting_date asc;"""%conditions, filters, as_dict=1)
	data =[]
	row =[]
	for invoice in invoices:
		row = [invoice.posting_date ,invoice.customer,invoice.name,invoice.package_name]
		services = frappe.db.sql("""select item_code, attended_by,qty from `tabSales Invoice Item` where parent = '%s' 
			and item_code IN (select services from `tabService` where parent = '%s');"""%(invoice.name, invoice.package_name), as_dict=1)
		row += [services[0].item_code,services[0].attended_by,services[0].qty]


		total_used = frappe.db.sql(""" select used_qty from `tabCustomer wise package` where services = '%s'
		 and package = '%s' and customer = '%s' limit 1 """%(services[0].item_code,invoice.package_name,invoice.customer) )
		row +=[total_used]


		current_balace = frappe.db.sql(""" select remaining_qty from `tabCustomer wise package` where services = '%s'
		 and package = '%s' and customer = '%s' limit 1 """%(services[0].item_code,invoice.package_name,invoice.customer) )
		row +=[current_balace]
		# frappe.errprint (row)
		# frappe.errprint(services)
		data.append(row)

	bought_packages = frappe.db.sql("""select a.posting_date,a.name, a.customer , b.item_code  from `tabSales Invoice` a , `tabSales Invoice Item` b  where 
	 b.parent = a.name and b.item_code IN (select name from `tabPackages`) %s order by posting_date asc;"""%conditions, filters, as_dict=1)
	frappe.errprint("bought Packages are ")
	frappe.errprint(bought_packages)
	row = []
	data.append([])
	if bought_packages:
		data.append([ "", " <b> Bought Packages are ----- </b>"])
	for b in bought_packages:
		row =[b.posting_date,b.customer,b.name,b.item_code]
		data.append(row)
	return data


def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"): conditions += " and posting_date >= %(from_date)s"
	if filters.get("to_date"): conditions += " and posting_date <= %(to_date)s"
	if filters.get("customer"): conditions += "and customer = %(customer)s"
	if filters.get("package"): conditions  += "and package_name = %(package)s"

	return conditions, filters