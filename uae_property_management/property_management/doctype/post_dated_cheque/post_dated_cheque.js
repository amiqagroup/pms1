frappe.ui.form.on("Post Dated Cheque", {
    status: function (frm) {
        if (frm.doc.status === "Replaced" && !frm.doc.replaced_by) {
            frappe.msgprint("Please create and link the replacing cheque in 'Replaced By'.");
        }
    }
});