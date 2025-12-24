from .version import __version__ as app_version  # noqa: F401

app_name = "uae_property_management"
app_title = "UAE Property Management"
app_publisher = "amiqagroup.com"
app_description = "Leasing-focused property management for UAE"
app_email = "info@amiqagroup.com"
app_license = "MIT"

# Includes in <head>
app_include_js = []
app_include_css = []

# Fixtures (roles, permissions, etc.) – you can add later if you export
fixtures = ["Custom Field", "Property Setter"]

# Desk modules
desk_icons = {
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "uae_property_management.property_management.utils.notifications."
        "daily_lease_and_cheque_alerts"
    ],
    "hourly": [
        # If you want more frequent overdue checks, put them here
    ]
}

# Doc Events
doc_events = {
    "Lease Contract": {
        "on_submit": (
            "uae_property_management.property_management.utils.notifications."
            "on_lease_submit"
        ),
        "on_cancel": (
            "uae_property_management.property_management.utils.notifications."
            "on_lease_cancel"
        )
    },
    "Post Dated Cheque": {
        "on_update": (
            "uae_property_management.property_management.utils.notifications."
            "on_pdc_update"
        )
    }
}

# Website, permissions, etc. left minimal for now
