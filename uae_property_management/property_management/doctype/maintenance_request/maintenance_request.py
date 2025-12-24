import frappe
from frappe.model.document import Document


class MaintenanceRequest(Document):
    def validate(self):
        self.ensure_links()

    def ensure_links(self):
        if not self.property and self.unit:
            self.property = frappe.db.get_value("Unit", self.unit, "property")
