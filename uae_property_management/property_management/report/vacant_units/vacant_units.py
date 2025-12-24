import frappe


def execute(filters=None):
    columns = [
        {"fieldname": "name", "label": "Unit",
            "fieldtype": "Link", "options": "Unit", "width": 120},
        {"fieldname": "property", "label": "Property",
            "fieldtype": "Link", "options": "Property", "width": 150},
        {"fieldname": "unit_type", "label": "Unit Type",
            "fieldtype": "Data", "width": 100},
        {"fieldname": "size_sqft",
            "label": "Size (Sqft)", "fieldtype": "Float", "width": 100},
        {"fieldname": "default_rent_amount", "label": "Default Rent",
            "fieldtype": "Currency", "width": 120}
    ]

    data = frappe.get_all(
        "Unit",
        filters={"current_status": "Vacant"},
        fields=["name", "property", "unit_type",
                "size_sqft", "default_rent_amount"]
    )

    return columns, data
