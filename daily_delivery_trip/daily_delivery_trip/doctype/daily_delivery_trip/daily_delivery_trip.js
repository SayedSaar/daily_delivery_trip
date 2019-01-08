// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on('Daily Delivery Trip', {
	setup: function(frm) {
		frm.fields_dict.delivery_notes.grid.get_field('delivery_note').get_query =
			function (doc, cdt, cdn) {
				var d = locals[cdt][cdn];

				var filters = [
					["Delivery Note", 'docstatus', '=', '1'],
					["Delivery Note", 'delivery_status', '!=', 'Delivered'],
					["Delivery Note", 'is_return', '!=', '1'],
					["Delivery Note", 'company', '=', frm.doc.company],
				];

				return {
					filters: filters
				}
			};
	},

	refresh: function(frm) {

	},

	get_items_from_delivery_notes: function(frm) {
		if(!frm.doc.delivery_notes.length) {
			frappe.msgprint(__("Please enter Delivery Notes first"));
		} else {
			return frm.call({
				doc: frm.doc,
				method: "get_items_from_delivery_notes",
				callback: function(r, rt) {
					//me.set_applicable_charges_for_item();
				}
			});
		}
	},

	delivery_notes: function(frm) {
		frappe.msgprint("Test");
	}
});

frappe.ui.form.on('Delivery Trip Delivery Note', {
	delivery_note: function(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (row.delivery_note) {
			return frm.call({
				doc: frm.doc,
				method: "update_delivery_note_fields",
				args: {
					row: row
				},
				callback: function(r, rt) {
					//me.set_applicable_charges_for_item();
				}
			});
		}
	}
});
