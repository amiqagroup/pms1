import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today
from uae_property_management.property_management.utils.lease_utils import get_payment_schedule


class LeaseContract(Document):
    def validate(self):
        self.set_lease_duration()
        self.validate_dates()
        self.validate_unit_availability()

    def on_submit(self):
        self.occupy_unit()
        self.create_security_deposit_entry()
        self.create_rent_invoices()

    def on_cancel(self):
        self.vacate_unit()
        self.reverse_security_deposit_entry()

    def set_lease_duration(self):
        if self.lease_start and self.lease_end:
            self.lease_duration = (
                getdate(self.lease_end) - getdate(self.lease_start)).days

    def validate_dates(self):
        if self.lease_start and self.lease_end and self.lease_end <= self.lease_start:
            frappe.throw("Lease End Date must be after Lease Start Date")

    def validate_unit_availability(self):
        unit = frappe.get_doc("Unit", self.unit)
        if unit.current_status == "Occupied":
            frappe.throw("This unit is already occupied")

    def occupy_unit(self):
        frappe.flags.allow_unit_occupied_change = True
        unit = frappe.get_doc("Unit", self.unit)
        unit.current_status = "Occupied"
        unit.save()
        frappe.flags.allow_unit_occupied_change = False

        self.contract_status = "Active"

    def vacate_unit(self):
        unit = frappe.get_doc("Unit", self.unit)
        unit.current_status = "Vacant"
        unit.save()
        self.contract_status = "Terminated" if getdate(
            self.lease_end) > getdate(today()) else "Expired"

    def create_security_deposit_entry(self):
        if not self.security_deposit:
            return

        # Optional: create Journal Entry or leave to manual
        # Configurable via system settings, but here we show an example
        pass

    def create_rent_invoices(self):
        schedule = get_payment_schedule(self)
        for period in schedule:
            inv = frappe.new_doc("Sales Invoice")
            inv.customer = self.tenant
            inv.due_date = period["due_date"]
            inv.due_date = period["due_date"]
            inv.posting_date = period["due_date"]
            inv.set_posting_time = 1
            inv.lease_contract = self.name
            inv.unit = self.unit

            # Rent item
            inv.append("items", {
                "item_name": "Rent - " + self.unit,
                "qty": 1,
                "rate": period["amount"],
                "description": f"Rent for lease {self.name}",
                "income_account": self.get_rent_income_account()
            })

            # VAT is handled via ERPNext tax templates; alternatively set taxes here

            inv.insert(ignore_permissions=True)
            inv.submit()

    def get_rent_income_account(self):
        # Could be read from Company or Property settings
        company = frappe.defaults.get_user_default("Company")
        return frappe.db.get_value("Company", company, "default_income_account")
