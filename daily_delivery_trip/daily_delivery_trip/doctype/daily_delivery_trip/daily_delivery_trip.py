# -*- coding: utf-8 -*-
# Copyright (c) 2018, Sayed Hameed Ebrahim and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, erpnext
from frappe import _
from frappe.utils import flt
from frappe.model.meta import get_field_precision
from frappe.model.document import Document
from frappe.contacts.doctype.contact.contact import get_contact_details, get_default_contact

class DailyDeliveryTrip(Document):
	def get_items_from_delivery_notes(self):
		#self.set("items", [])
		for dn in self.get("delivery_notes"):
			if dn.delivery_note:
				dn_items = frappe.db.sql("""select dn_item.name, dn_item.item_code,
					dn_item.item_name, dn_item.qty, dn_item.delivered_qty
					from `tabDelivery Note Item` dn_item where parent = %s
					and exists(select name from tabItem where name = dn_item.item_code and is_stock_item = 1)
					""",dn.delivery_note, as_dict=True)

				delivery_note_doc = frappe.get_doc("Delivery Note", dn.delivery_note)

				for d in dn_items:
					exist = False
					for i in self.get("items"):
						if d.name == i.delivery_note_item:
							exist = True
					if exist == False:
						item = self.append("items")
						item.delivery_note = delivery_note_doc.name
						delivery_note_item_doc = frappe.get_doc("Delivery Note Item", d.name)
						item.delivery_note_item = delivery_note_item_doc.name
						item.item_code = d.item_code
						item.item_name = d.item_name
						item.qty = abs(flt(d.qty)) - abs(flt(d.delivered_qty))

	def validate(self):
		self.check_mandatory()
		self.validate_delivery_notes()
		if not self.get("items"):
			self.get_items_from_delivery_notes()
		else:
			self.validate_quantities()

	def validate_quantities(self):
		for dn in self.get("delivery_notes"):
			if dn.delivery_note:
				dn_items = frappe.db.sql("""select dn_item.name, dn_item.item_code,
					dn_item.item_name, dn_item.qty, dn_item.delivered_qty
					from `tabDelivery Note Item` dn_item where parent = %s
					and exists(select name from tabItem where name = dn_item.item_code and is_stock_item = 1)
					""",dn.delivery_note, as_dict=True)

				wrong_items = []
				already_delivered = []
				wrong_qty_msg = "<b>The following items have wrong quantities:</b><br>"
				already_delivered_msg = "<hr><b>The following items are already delivered:</b><br>"
				for d in dn_items:
					for i in self.get("items"):
						if d.name == i.delivery_note_item:
							undelivered_qty = flt(d.qty) - flt(d.delivered_qty)
							if flt(i.qty) > undelivered_qty:
								wrong_items.append(i)
								wrong_qty_msg +=  "- " + i.delivery_note + " (" + i.item_name + ") <b>-></b> Max Quanitity is " +  str(undelivered_qty) + ".<br>"
							elif int(undelivered_qty) == 0:
								already_delivered_msg +=  "- " + i.delivery_note + " (" + i.item_name + ")" + ".<br>"
								already_delivered.append(i)

				errormsg = ""
				if len(wrong_items) > 0:
					errormsg += wrong_qty_msg

				if len(already_delivered) > 0:
					errormsg += already_delivered_msg

				if errormsg != "":
					frappe.throw(errormsg)							

	def check_mandatory(self):
		if not self.get("delivery_notes"):
			frappe.throw(_("Please enter Delivery Note"))

	def validate_delivery_notes(self):
		delivery_notes = []
		
		for d in self.get("delivery_notes"):
			if frappe.db.get_value("Delivery Note", d.delivery_note, "docstatus") != 1:
				frappe.throw(_("Delivery Note must be submitted"))
			else:
				delivery_notes.append(d.delivery_note)

		for item in self.get("items"):
			if not item.delivery_note:
				frappe.throw(_("Item must be added using 'Get Items from Delivery Notes' button"))
			elif item.delivery_note not in delivery_notes:
				frappe.throw(_("Item Row {idx}: {doctype} {docname} does not exist in above '{doctype}' table")
					.format(idx=item.idx, doctype="Delivery Note", docname=item.delivery_note.name))

	def update_delivery_note_fields(self, row):
		selected_delivery_note = frappe._dict(row)
		delivery_note_doc = frappe.get_doc("Delivery Note", selected_delivery_note.delivery_note)
		delivery_notes = self.get("delivery_notes")
		for dn in delivery_notes:
			if delivery_note_doc.name == dn.delivery_note:
				dn.customer = delivery_note_doc.customer
				if delivery_note_doc.shipping_address:
					dn.address = delivery_note_doc.shipping_address_name
					dn.customer_address = delivery_note_doc.shipping_address
				dn.date = delivery_note_doc.posting_date
				dn.status = delivery_note_doc.status
				contact_person = get_default_contact("Customer", delivery_note_doc.customer)
								
				if contact_person:
					contact = get_contact_details(contact_person)
					dn.mobile = contact["contact_mobile"]


	def on_submit(self):
		self.validate()
		for item in self.get("items"):
			delivery_note_item = frappe.get_doc("Delivery Note Item", item.delivery_note_item)
			new_qty = flt(delivery_note_item.delivered_qty) + flt(item.qty)
			frappe.db.set_value("Delivery Note Item", item.delivery_note_item, "delivered_qty", new_qty)
			if flt(new_qty) == flt(delivery_note_item.qty):
				frappe.db.set_value("Delivery Note Item", item.delivery_note_item, "delivery_status", "Delivered")
			
			delivery_note = frappe.get_doc("Delivery Note", item.delivery_note)
			delivery_status = "Delivered"
			for i in delivery_note.items:
				if i.delivery_status != "Delivered":
					delivery_status = "Pending"
					break
			
			if delivery_status == "Delivered":
				frappe.db.set_value("Delivery Note", item.delivery_note, "delivery_status", "Delivered")

	def on_cancel(self):
		for item in self.get("items"):
			delivery_note_item = frappe.get_doc("Delivery Note Item", item.delivery_note_item)
			new_qty = flt(delivery_note_item.delivered_qty) - flt(item.qty)
			frappe.db.set_value("Delivery Note Item", item.delivery_note_item, "delivered_qty", new_qty)
			frappe.db.set_value("Delivery Note Item", item.delivery_note_item, "delivery_status", "Pending")
			
			frappe.db.set_value("Delivery Note", item.delivery_note, "delivery_status", "Pending")
