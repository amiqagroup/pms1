import frappe
from frappe.model.document import Document


class Unit(Document):
    def validate(self):
        self.validate_status()

    def validate_status(self):
        # Example rule: you cannot mark unit as Occupied manually
        if self.current_status == "Occupied":
            # Must be controlled via Lease Contract
            from frappe import _
            if not frappe.flags.allow_unit_occupied_change:
                frappe.throw(
                    _("Unit status cannot be set to Occupied directly. Use Lease Contract."))
