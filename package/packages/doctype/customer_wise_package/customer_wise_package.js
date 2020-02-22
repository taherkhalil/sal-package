// Copyright (c) 2017, taher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer wise package', {
	before_save: function(frm) {
		// var remaining_qty = frm.doc.quantity_issued - frm.doc.used_qty;
		// frm.set_value("remaining_qty", remaining_qty);
		// frm.refresh_field("remaining_qty");
		// // cur_frm.save();
	}
});
