import frappe
from frappe.utils import getdate, add_months

FREQUENCY_MONTHS = {
    "Annual": 12,
    "Semi-Annual": 6,
    "Quarterly": 3,
    "Monthly": 1,
}


def get_payment_schedule(lease_doc):
    """Return list of dicts: {due_date, amount}."""
    total = lease_doc.annual_rent
    freq = lease_doc.payment_frequency or "Annual"
    months = FREQUENCY_MONTHS[freq]
    installments = int(12 / months)
    installment_amount = total / installments

    schedule = []
    start = getdate(lease_doc.lease_start)
    for i in range(installments):
        due_date = add_months(start, i * months)
        schedule.append({"due_date": due_date, "amount": installment_amount})
    return schedule
