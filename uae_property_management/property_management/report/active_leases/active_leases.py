import frappe


def execute(filters=None):
    columns = [
        {"fieldname": "name", "label": "Lease", "fieldtype": "Link",
            "options": "Lease Contract", "width": 120},
        {"fieldname": "property", "label": "Property",
            "fieldtype": "Link", "options": "Property", "width": 150},
        {"fieldname": "unit", "label": "Unit",
            "fieldtype": "Link", "options": "Unit", "width": 120},
        {"fieldname": "tenant", "label": "Tenant",
            "fieldtype": "Link", "options": "Tenant", "width": 150},
        {"fieldname": "lease_start", "label": "Start Date",
            "fieldtype": "Date", "width": 100},
        {"fieldname": "lease_end", "label": "End Date",
            "fieldtype": "Date", "width": 100},
        {"fieldname": "annual_rent", "label": "Annual Rent",
            "fieldtype": "Currency", "width": 120}
    ]

    data = frappe.get_all(
        "Lease Contract",
        filters={"contract_status": "Active"},
        fields=["name", "property", "unit", "tenant",
                "lease_start", "lease_end", "annual_rent"]
    )

    return columns, data
