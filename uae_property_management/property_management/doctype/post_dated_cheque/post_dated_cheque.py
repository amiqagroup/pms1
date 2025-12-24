# post_dated_cheque.py (replacing previous simplistic handler)

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today
from uae_property_management.property_management.utils.notifications import send_bounced_cheque_alert

ALLOWED_TRANSITIONS = {
    "Pending": ["Deposited", "Cancelled"],
    "Deposited": ["Cleared", "Bounced", "Cancelled"],
    "Bounced": ["Replaced"],
    "Cleared": [],
    "Replaced": [],
    "Cancelled": []
}


class PostDatedCheque(Document):
    def before_save(self):
        self.validate_amount()
        self.validate_transition()

    def on_update(self):
        self.handle_status_change()

    def validate_amount(self):
        if self.amount and self.amount <= 0:
            frappe.throw("Cheque amount must be greater than zero")

    def validate_transition(self):
        if not self.get_db_value("status"):
            # first save
            return

        old_status = self.get_db_value("status")
        new_status = self.status

        if old_status == new_status:
            return

        allowed = ALLOWED_TRANSITIONS.get(old_status, [])
        if new_status not in allowed:
            frappe.throw(
                f"Invalid status transition from {old_status} to {new_status}")

    def handle_status_change(self):
        old_status = self.get_db_value("status")
        new_status = self.status

        # When saved via form, get_db_value still returns the current value in DB (before update hook)
        # So we might want to track via flags; here, keep it simple:

        if new_status == "Deposited":
            self.on_deposit()

        elif new_status == "Cleared":
            self.on_clear()

        elif new_status == "Bounced":
            self.on_bounce()

        elif new_status == "Replaced":
            self.on_replaced()

        elif new_status == "Cancelled":
            self.on_cancelled()

    def on_deposit(self):
        # You can log an Activity Log or comment
        self.add_comment(
            "Info", f"Cheque {self.cheque_number} deposited on {today()}")

    def on_clear(self):
        self.create_payment_entry_if_missing()
        self.add_comment(
            "Info", f"Cheque {self.cheque_number} cleared on {today()}")

    def on_bounce(self):
        # Notify relevant roles
        send_bounced_cheque_alert(self)
        self.add_comment(
            "Comment", f"Cheque {self.cheque_number} bounced on {today()}")
        # Optionally track bounce count on Tenant or Lease
        self.increment_bounce_counter()

    def on_replaced(self):
        # no automatic accounting, just ensure replaced_by is set
        if not self.replaced_by:
            frappe.throw("Please link the replacing cheque in 'Replaced By'")
        self.add_comment("Info", f"Cheque replaced by {self.replaced_by}")

    def on_cancelled(self):
        self.add_comment("Info", f"Cheque {self.cheque_number} cancelled")

    def create_payment_entry_if_missing(self):
        if self.payment_entry:
            return
        if not self.sales_invoice:
            # No invoice linked – warn but allow (or enforce link)
            frappe.msgprint(
                "Cheque cleared but no Sales Invoice linked. Please link manually.")
            return

        si = frappe.get_doc("Sales Invoice", self.sales_invoice)
        if si.outstanding_amount <= 0:
            frappe.msgprint(
                "Invoice already fully paid. No Payment Entry created.")
            return

        pe = frappe.new_doc("Payment Entry")
        pe.payment_type = "Receive"
        pe.company = si.company
        pe.posting_date = today()
        pe.party_type = "Customer"
        pe.party = si.customer
        pe.paid_from = si.debit_to  # Customer account
        pe.paid_to = get_default_bank_account(si.company)
        pe.paid_amount = self.amount
        pe.received_amount = self.amount

        pe.append("references", {
            "reference_doctype": "Sales Invoice",
            "reference_name": si.name,
            "total_amount": si.grand_total,
            "outstanding_amount": si.outstanding_amount,
            "allocated_amount": min(self.amount, si.outstanding_amount)
        })

        pe.insert(ignore_permissions=True)
        pe.submit()

        self.payment_entry = pe.name
        frappe.db.set_value(self.doctype, self.name, "payment_entry", pe.name)

    def increment_bounce_counter(self):
        if not self.lease_contract:
            return
        lease = frappe.get_doc("Lease Contract", self.lease_contract)
        # You can add a field bounce_count on Lease Contract / Tenant if you want
        if hasattr(lease, "bounce_count"):
            lease.bounce_count = (lease.bounce_count or 0) + 1
            lease.db_update()


def get_default_bank_account(company):
    # try get from Company default
    acc = frappe.db.get_value("Company", company, "default_bank_account")
    if not acc:
        frappe.throw(f"Please set Default Bank Account for Company {company}")
    return acc
