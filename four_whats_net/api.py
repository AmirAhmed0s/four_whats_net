import frappe
from frappe import _
from four_whats_net.patches.add_whatsapp_number_custom_field import add_whatsapp_field_to_doctype


@frappe.whitelist()
def add_whatsapp_field(doctype):
    """
    Whitelisted API to add the 'whatsapp_number' custom field to *doctype*.

    Can be called from the browser console or from a custom script:
        frappe.call('four_whats_net.api.add_whatsapp_field', {doctype: 'My DocType'})
    """
    if not frappe.has_permission("Custom Field", "write"):
        frappe.throw(_("You do not have permission to add custom fields."), frappe.PermissionError)

    doctype = frappe.strip_html(doctype).strip()
    if not doctype:
        frappe.throw(_("DocType name cannot be empty."))

    if not frappe.db.exists("DocType", doctype):
        frappe.throw(_("DocType '{0}' does not exist.").format(doctype))

    add_whatsapp_field_to_doctype(doctype)
    frappe.db.commit()
    return {"message": _("WhatsApp Number field added to '{0}' successfully.").format(doctype)}
