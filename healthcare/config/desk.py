

from __future__ import unicode_literals

# Define the custom pages
def get_custom_pages():
    return [
        {
            "title": "Patient Dashboard",
            "path": "patient_dashboard",
            "type": "website"
        },
        {
            "title": "Profile Management",
            "path": "profile_management",
            "type": "website"
        },
        {
            "title": "Book Appointment",
            "path": "appointment_booking",
            "type": "website"
        },
    
        {
            "title": "Admission Status",
            "path": "admission_status",
            "type": "website"
        },
        {
            "title": "Discharge Summary",
            "path": "discharge_summary",
            "type": "website"
        },
        {
            "title": "Invoice Viewer",
            "path": "invoice_viewer",
            "type": "website"
        }
    ]
