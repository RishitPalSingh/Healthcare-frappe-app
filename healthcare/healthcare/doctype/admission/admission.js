// Copyright (c) 2024, Rishit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Admission", {
    refresh: function(frm) {

        frm.add_custom_button(__('Make Discharge Summary'), function() {
        
            
            frappe.new_doc('Discharge Summary', {
                admission_id: frm.doc.name  ,
                
            });
        });
    }
});
