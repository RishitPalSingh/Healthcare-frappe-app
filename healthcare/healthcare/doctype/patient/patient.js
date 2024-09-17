frappe.ui.form.on('Patient', {
    validate: function(frm) {
        // Ensure date_of_birth is not a future date
        if (frm.doc.date_of_birth) {
            const today = new Date();
            const dob = new Date(frm.doc.date_of_birth);
            
            if (dob > today) {
                frappe.msgprint(__('Date of Birth cannot be a future date.'));
                frappe.validated = false;  // Prevent the form from saving
            }
        }
    },
    before_save: function(frm) {
        // Ensure that first_name and date_of_birth fields are available before formatting patient_id
        if (frm.doc.first_name && frm.doc.date_of_birth) {
            // Format date_of_birth to YYYY-MM-DD
            const formattedDate = frappe.datetime.str_to_obj(frm.doc.date_of_birth).toISOString().split('T')[0];
            frm.doc.patient_id = `${frm.doc.first_name} ${formattedDate}`;
        } else if (!frm.doc.patient_id) {
            // Default value if patient_id is not set and required fields are missing
            frm.doc.patient_id = "Unknown Patient";
        }
    },
    refresh: function(frm) {

        // Add a custom button to the Patient form
        frm.add_custom_button(__('Book Appointment'), function() {

            
            frappe.new_doc('Appointment', {
                patient_id: frm.doc.name
            });
        });
        frm.add_custom_button(__('Make Invoice'), function() {
    
            
            frappe.new_doc('Invoice', {
                patient_id: frm.doc.name  
            });
        });
        frm.add_custom_button(__('Admit'), function() {
        
            
            frappe.new_doc('Admission', {
                patient_id: frm.doc.name  ,
                
            });
        });
    }
});
