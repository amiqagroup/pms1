import frappe
from frappe.utils import today, add_days, getdate


def on_lease_submit(doc, method):
    # Placeholder for additional notifications
    pass


def on_lease_cancel(doc, method):
    # Placeholder if you want notifications on cancellation
    pass


def on_pdc_update(doc, method):
    # Already handled in controller; here you can send additional notifications if needed
    pass


def send_bounced_cheque_alert(pdc_doc):
    recipients = get_property_managers_and_accounts()
    subject = f"Bounced Cheque: {pdc_doc.cheque_number}"
    message = f"""
    Cheque {pdc_doc.cheque_number} for Lease {pdc_doc.lease_contract} has bounced.
    Amount: {pdc_doc.amount}
    Date: {pdc_doc.cheque_date}
    """
    send_email_notification(recipients, subject, message)


def get_property_managers_and_accounts():
    users = []
    for role in ["Property Manager", "Accounts Officer"]:
        role_users = frappe.db.get_all(
            "Has Role", filters={"role": role}, fields=["parent"])
        users.extend([u.parent for u in role_users])
    return list(set(users))


def send_email_notification(recipients, subject, message):
    if not recipients:
        return
    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=message
    )


def daily_lease_and_cheque_alerts():
    send_lease_expiry_reminders()
    send_cheque_due_reminders()
    send_overdue_rent_alerts()
    send_vacant_unit_alerts()


def send_lease_expiry_reminders():
    days_list = [90, 60, 30]
    for days in days_list:
        target_date = add_days(today(), days)
        leases = frappe.get_all(
            "Lease Contract",
            filters={"lease_end": target_date, "contract_status": "Active"},
            fields=["name", "tenant", "unit", "property"]
        )
        for lease in leases:
            # Simple notification
            subject = f"Lease {lease.name} expiring in {days} days"
            message = f"Lease {lease.name} for unit {lease.unit} will expire on {target_date}."
            recipients = get_property_managers_and_accounts()
            send_email_notification(recipients, subject, message)


def send_cheque_due_reminders():
    # Remind 3 days before cheque date
    target_date = add_days(today(), 3)
    cheques = frappe.get_all(
        "Post Dated Cheque",
        filters={"cheque_date": target_date, "status": "Pending"},
        fields=["name", "lease_contract", "amount", "cheque_number"]
    )
    for c in cheques:
        subject = f"Cheque {c.cheque_number} due on {target_date}"
        message = f"Cheque {c.cheque_number} for lease {c.lease_contract} is due on {target_date}."
        recipients = get_property_managers_and_accounts()
        send_email_notification(recipients, subject, message)


def send_overdue_rent_alerts():
    # Simple version: check unpaid Sales Invoices past due_date
    invoices = frappe.get_all(
        "Sales Invoice",
        filters={"outstanding_amount": (
            ">", 0), "docstatus": 1, "due_date": ("<", today())},
        fields=["name", "customer", "due_date", "outstanding_amount"]
    )
    if not invoices:
        return

    subject = "Overdue Rent Invoices"
    lines = []
    for inv in invoices:
        lines.append(
            f"{inv.name} - {inv.customer} - Due {inv.due_date} - AED {inv.outstanding_amount}")
    message = "The following rent invoices are overdue:\n" + "\n".join(lines)

    recipients = get_property_managers_and_accounts()
    send_email_notification(recipients, subject, message)


def send_vacant_unit_alerts():
    units = frappe.get_all("Unit", filters={"current_status": "Vacant"}, fields=[
                           "name", "property"])
    if not units:
        return
    subject = "Vacant Units Alert"
    lines = [f"{u.name} ({u.property})" for u in units]
    message = "The following units are vacant:\n" + "\n".join(lines)
    recipients = get_property_managers_and_accounts()
    send_email_notification(recipients, subject, message)
