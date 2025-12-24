import frappe
from frappe.model.document import Document


class Property(Document):
    def validate(self):
        self.set_total_units()

    def set_total_units(self):
        if not self.name:
            return
        count = frappe.db.count("Unit", {"property": self.name})
        self.total_units = count
