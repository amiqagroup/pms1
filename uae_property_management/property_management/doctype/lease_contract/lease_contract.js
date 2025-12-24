frappe.ui.form.on("Lease Contract", {
    unit: function (frm) {
        if (frm.doc.unit) {
            frappe.db.get_value("Unit", frm.doc.unit, ["default_rent_amount", "vat_applicable"], (r) => {
                if (r) {
                    if (!frm.doc.annual_rent) {
                        frm.set_value("annual_rent", r.default_rent_amount || 0);
                    }
                    if (r.vat_applicable != null) {
                        frm.set_value("vat_applicable", r.vat_applicable ? 1 : 0);
                    }
                }
            });
        }
    }
});