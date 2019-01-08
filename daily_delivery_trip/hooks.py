# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "daily_delivery_trip"
app_title = "Daily Delivery Trip"
app_publisher = "Sayed Hameed Ebrahim"
app_description = "Manage Daily Delivery Trips"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "sayed.saar@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/daily_delivery_trip/css/daily_delivery_trip.css"
# app_include_js = "/assets/daily_delivery_trip/js/daily_delivery_trip.js"

# include js, css files in header of web template
# web_include_css = "/assets/daily_delivery_trip/css/daily_delivery_trip.css"
# web_include_js = "/assets/daily_delivery_trip/js/daily_delivery_trip.js"

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
# get_website_user_home_page = "daily_delivery_trip.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "daily_delivery_trip.install.before_install"
# after_install = "daily_delivery_trip.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "daily_delivery_trip.notifications.get_notification_config"

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

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"daily_delivery_trip.tasks.all"
# 	],
# 	"daily": [
# 		"daily_delivery_trip.tasks.daily"
# 	],
# 	"hourly": [
# 		"daily_delivery_trip.tasks.hourly"
# 	],
# 	"weekly": [
# 		"daily_delivery_trip.tasks.weekly"
# 	]
# 	"monthly": [
# 		"daily_delivery_trip.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "daily_delivery_trip.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "daily_delivery_trip.event.get_events"
# }


fixtures = [
	{"dt": "DocType", "filters": [
		["name", "in", [
				"Daily Delivery Trip",
				"Daily Delivery Trip Item",
				"Delivery Trip Delivery Note"
			]
		]
	]},
	{"dt": "Custom Field", "filters": [
		["name", "in", [
				"Delivery Note-delivery_status",
				"Delivery Note Item-delivered_qty",
				"Delivery Note Item-delivery_status"
			]
		]
	]}
]
