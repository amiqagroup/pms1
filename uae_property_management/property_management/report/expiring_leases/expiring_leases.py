import frappe
from frappe.utils import add_days, today, getdate


def execute(filters=None):
    filters = filters or {}
    days = filters.get("days") or 60
    target_date = add_days(today(), days)

    columns = [
        {"fieldname": "name", "label": "Lease", "fieldtype": "Link",
            "options": "Lease Contract", "width": 120},
        {"fieldname": "property", "label": "Property",
            "fieldtype": "Link", "options": "Property", "width": 150},
        {"fieldname": "unit", "label": "Unit",
            "fieldtype": "Link", "options": "Unit", "width": 120},
        {"fieldname": "tenant", "label": "Tenant",
            "fieldtype": "Link", "options": "Tenant", "width": 150},
        {"fieldname": "lease_end", "label": "End Date",
            "fieldtype": "Date", "width": 100},
        {"fieldname": "days_to_expiry", "label": "Days to Expiry",
            "fieldtype": "Int", "width": 100}
    ]

    leases = frappe.get_all(
        "Lease Contract",
        filters={"contract_status": "Active",
                 "lease_end": ("<=", target_date)},
        fields=["name", "property", "unit", "tenant", "lease_end"]
    )

    data = []
    for l in leases:
        d = {}
        d.update(l)
        d["days_to_expiry"] = (getdate(l.lease_end) - getdate(today())).days
        data.append(d)

    return columns, data
