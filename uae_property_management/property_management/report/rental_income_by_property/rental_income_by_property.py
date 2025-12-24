import frappe


def execute(filters=None):
    filters = filters or {}
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    columns = [
        {"fieldname": "property", "label": "Property",
            "fieldtype": "Link", "options": "Property", "width": 150},
        {"fieldname": "total_rent", "label": "Total Rent",
            "fieldtype": "Currency", "width": 150}
    ]

    conditions = "si.docstatus = 1"
    if from_date:
        conditions += " and si.posting_date >= %(from_date)s"
    if to_date:
        conditions += " and si.posting_date <= %(to_date)s"

    # Assuming custom fields: lease_contract, unit, property on Sales Invoice (or via item)
    data = frappe.db.sql("""
        SELECT
            si.property as property,
            SUM(si.grand_total) as total_rent
        FROM `tabSales Invoice` si
        WHERE {conditions}
        GROUP BY si.property
    """.format(conditions=conditions), filters, as_dict=True)

    return columns, data
