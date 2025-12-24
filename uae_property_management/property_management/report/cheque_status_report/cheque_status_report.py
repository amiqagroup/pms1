import frappe


def execute(filters=None):
    filters = filters or {}
    status = filters.get("status")

    columns = [
        {"fieldname": "name", "label": "PDC", "fieldtype": "Link",
            "options": "Post Dated Cheque", "width": 120},
        {"fieldname": "lease_contract", "label": "Lease",
            "fieldtype": "Link", "options": "Lease Contract", "width": 150},
        {"fieldname": "cheque_number", "label": "Cheque #",
            "fieldtype": "Data", "width": 120},
        {"fieldname": "bank_name", "label": "Bank",
            "fieldtype": "Data", "width": 120},
        {"fieldname": "cheque_date", "label": "Cheque Date",
            "fieldtype": "Date", "width": 100},
        {"fieldname": "amount", "label": "Amount",
            "fieldtype": "Currency", "width": 120},
        {"fieldname": "status", "label": "Status",
            "fieldtype": "Data", "width": 100}
    ]

    filters_dict = {}
    if status:
        filters_dict["status"] = status

    data = frappe.get_all(
        "Post Dated Cheque",
        filters=filters_dict,
        fields=["name", "lease_contract", "cheque_number",
                "bank_name", "cheque_date", "amount", "status"]
    )

    return columns, data
