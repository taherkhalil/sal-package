# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "package"
app_title = "Packages"
app_publisher = "taher"
app_description = "package creation app"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "taherkhalil52@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/package/css/package.css"
# app_include_js = "/assets/package/js/package.js"

# include js, css files in header of web template
# web_include_css = "/assets/package/css/package.css"
# web_include_js = "/assets/package/js/package.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "package.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "package.install.before_install"
# after_install = "package.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "package.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
	"Sales Invoice" : {
		"validate": "package.packages.doctype.packages.packages.package_buy",
		"on_submit": "package.packages.doctype.packages.packages.on_submit"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"package.tasks.all"
# 	],
# 	"daily": [
# 		"package.tasks.daily"
# 	],
# 	"hourly": [
# 		"package.tasks.hourly"
# 	],
# 	"weekly": [
# 		"package.tasks.weekly"
# 	]
# 	"monthly": [
# 		"package.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "package.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "package.event.get_events"
# }

