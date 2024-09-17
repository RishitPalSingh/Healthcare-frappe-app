frappe.ui.form.on('Doctor', {
    before_save: function(frm) {
        // Ensure all required fields are available before formatting doctor_id
        if (frm.doc.first_name && frm.doc.last_name && frm.doc.specialization) {
            frm.doc.doctor_id = `Dr. ${frm.doc.first_name} ${frm.doc.last_name} ${frm.doc.specialization}`;
        } else if (!frm.doc.doctor_id) {
            // Default value if doctor_id is not set and required fields are missing
            frm.doc.doctor_id = "Dr. Unknown";
        }
    }
});
