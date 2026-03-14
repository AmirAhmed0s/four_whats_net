import frappe
from frappe import _


# Standard DocTypes that benefit from a dedicated WhatsApp number field.
# The field is inserted after "mobile_no" when that field exists, otherwise
# after "phone" when that exists, otherwise at the very end of the form.
TARGET_DOCTYPES = [
    "Customer",
    "Supplier",
    "Contact",
    "Lead",
    "Employee",
    "Sales Order",
    "Purchase Order",
    "Sales Invoice",
    "Purchase Invoice",
    "Payment Entry",
    "Journal Entry",
    "Quotation",
    "Delivery Note",
    "Purchase Receipt",
]


def execute():
    """Add the 'whatsapp_number' custom Phone field to a set of standard DocTypes."""
    for doctype in TARGET_DOCTYPES:
        add_whatsapp_field_to_doctype(doctype)
    frappe.db.commit()


def add_whatsapp_field_to_doctype(doctype):
    """
    Add a 'whatsapp_number' custom field (fieldtype=Phone) to *doctype* unless
    the field already exists (either as a standard field or as a custom field).
    """
    if not frappe.db.exists("DocType", doctype):
        return

    # Skip if the field already exists as a standard field or custom field
    if (
        frappe.db.exists("DocField", {"parent": doctype, "fieldname": "whatsapp_number"})
        or frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": "whatsapp_number"})
    ):
        return

    # Decide where to insert the new field
    insert_after = ""
    for preferred in ("mobile_no", "phone"):
        if (
            frappe.db.exists("DocField", {"parent": doctype, "fieldname": preferred})
            or frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": preferred})
        ):
            insert_after = preferred
            break

    custom_field = frappe.get_doc({
        "doctype": "Custom Field",
        "dt": doctype,
        "fieldname": "whatsapp_number",
        "fieldtype": "Phone",
        "label": "WhatsApp Number",
        "insert_after": insert_after,
        "description": _("WhatsApp number used for automated WhatsApp notifications"),
    })
    custom_field.insert(ignore_permissions=True)
