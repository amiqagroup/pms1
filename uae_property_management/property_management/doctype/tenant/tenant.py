import frappe
from frappe.model.document import Document


class Tenant(Document):
    def validate(self):
        self.validate_blacklist()

    def validate_blacklist(self):
        if self.status == "Blacklisted":
            # Simple hook to warn on blacklisted tenants
            frappe.msgprint(
                f"Tenant {self.name} is blacklisted. Avoid new leases unless approved.")
