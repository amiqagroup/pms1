import frappe


def execute(filters=None):
    filters = filters or {}
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    columns = [
        {"fieldname": "posting_date", "label": "Posting Date",
            "fieldtype": "Date", "width": 100},
        {"fieldname": "invoice", "label": "Invoice", "fieldtype": "Link",
            "options": "Sales Invoice", "width": 120},
        {"fieldname": "customer", "label": "Tenant",
            "fieldtype": "Link", "options": "Customer", "width": 150},
        {"fieldname": "net_total", "label": "Net Amount",
            "fieldtype": "Currency", "width": 120},
        {"fieldname": "total_taxes_and_charges", "label": "VAT Amount",
            "fieldtype": "Currency", "width": 120},
        {"fieldname": "grand_total", "label": "Total with VAT",
            "fieldtype": "Currency", "width": 120}
    ]

    conditions = "docstatus = 1"
    if from_date:
        conditions += " and posting_date >= %(from_date)s"
    if to_date:
        conditions += " and posting_date <= %(to_date)s"

    data = frappe.db.sql("""
        SELECT
            name as invoice,
            posting_date,
            customer,
            net_total,
            total_taxes_and_charges,
            grand_total
        FROM `tabSales Invoice`
        WHERE {conditions} and ifnull(lease_contract, '') != ''
    """.format(conditions=conditions), filters, as_dict=True)

    return columns, data
