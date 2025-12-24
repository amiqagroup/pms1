import frappe


def execute(filters=None):
    columns = [
        {"fieldname": "name", "label": "Invoice", "fieldtype": "Link",
            "options": "Sales Invoice", "width": 120},
        {"fieldname": "customer", "label": "Tenant",
            "fieldtype": "Link", "options": "Customer", "width": 150},
        {"fieldname": "posting_date", "label": "Posting Date",
            "fieldtype": "Date", "width": 100},
        {"fieldname": "due_date", "label": "Due Date",
            "fieldtype": "Date", "width": 100},
        {"fieldname": "grand_total", "label": "Grand Total",
            "fieldtype": "Currency", "width": 120},
        {"fieldname": "outstanding_amount", "label": "Outstanding",
            "fieldtype": "Currency", "width": 120}
    ]

    data = frappe.get_all(
        "Sales Invoice",
        filters={"docstatus": 1, "outstanding_amount": (">", 0)},
        fields=["name", "customer", "posting_date",
                "due_date", "grand_total", "outstanding_amount"]
    )

    return columns, data
