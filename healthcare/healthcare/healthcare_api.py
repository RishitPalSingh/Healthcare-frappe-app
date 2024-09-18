from frappe import _
import frappe

@frappe.whitelist(allow_guest=True)
def get_patient(patient_id):
    """Retrieve patient details by patient_id"""
    try:
        patient = frappe.get_doc("Patient", patient_id)
        return patient.as_dict()
    except frappe.DoesNotExistError:
        frappe.throw(_("Patient not found"), frappe.NotFoundError)


@frappe.whitelist(allow_guest=True)
def get_patient_id_by_email(email):
    """
    Retrieve the patient ID using the email address.
    """
    try:
   
        patient = frappe.get_all('Patient', filters={'contact_information': email}, fields=['patient_id'])
        if patient:
            return patient[0].patient_id
        else:
            return {'error': 'Patient not found'}
    except Exception as e:
        frappe.log_error(message=str(e), title=_('Error in get_patient_id_by_email API'))
        return {'error': str(e)}        

@frappe.whitelist(allow_guest=True)
def get_doctors():

    """
    Retrieve a list of all doctors.
    """
    try:
      
        doctors = frappe.get_all('Doctor', fields=['doctor_id', 'first_name', 'last_name', 'specialization'])
        return doctors
    except Exception as e:
        frappe.log_error(message=str(e), title=_('Error in get_doctors API'))
        return {'error': str(e)}

@frappe.whitelist()
def update_patient(patient_id, first_name=None, last_name=None, contact_information=None,date_of_birth=None, address=None):
    """Update patient details"""
    try:
       
        patient = frappe.get_doc("Patient", patient_id)

      
        if first_name:
            patient.first_name = first_name
        if last_name:
            patient.last_name = last_name

        if date_of_birth:
            patient.date_of_birth = date_of_birth

        if contact_information:
            patient.contact_information = contact_information
        if address:
            patient.address = address

        patient.save()
        frappe.db.commit()

        return {"message": "Patient details updated successfully"}

    except frappe.DoesNotExistError:
        # Log a shorter error message for debugging
       
        return {"error": "Patient not found"}
    except Exception as e:
      
    
        return {"error": str(e)}




@frappe.whitelist(allow_guest=True)
def get_current_user():
    
    user = frappe.get_doc('User', frappe.session.user)
    return {'email': user.email}


@frappe.whitelist(allow_guest=True)
def get_discharge_summarybyid(discharge_id):
    
    
    try:
       
        discharge_summary = frappe.get_doc('Discharge Summary', discharge_id)
        print(discharge_summary)
       
        return {
            "discharge_id": discharge_summary.discharge_id,
            "admission_id": discharge_summary.admission_id,
            "discharge_date": discharge_summary.discharge_date,
            "final_diagnosis": discharge_summary.final_diagnosis,
            "treatment_given": discharge_summary.treatment_given,
            "follow_up_instructions": discharge_summary.follow_up_instructions
        }
    
    except frappe.DoesNotExistError:
       
        return {"error": "Discharge summary not found"}
    except Exception as e:
       
        frappe.log_error(f"Error in get_discharge_summary: {str(e)}")
        return {"error": "An error occurred while fetching discharge summary details"}



@frappe.whitelist(allow_guest=True)
def get_admission_by_id(admission_id):
    try:
    
        admission = frappe.get_doc('Admission', admission_id)
    
        return {
            "admission_id": admission.admission_id,
            "patient_id": admission.patient_id,
            "admission_date": admission.admission_date,
            "reason_for_admission": admission.reason_for_admission,
            "status": admission.status
        }
    except frappe.DoesNotExistError:
    
        return {"error": "Admission not found"}
    except Exception as e:
    
        frappe.log_error(f"Error in get_admission: {str(e)}")
        return {"error": "An error occurred while fetching admission details"}


@frappe.whitelist(allow_guest=True)
def get_invoice(invoice_id):
    try:
    
        invoice = frappe.get_doc('Invoice', invoice_id)
        
        return {
            "invoice_id": invoice.invoice_id,
            "patient_id": invoice.patient_id,
            "date": invoice.date,
            "services_rendered": invoice.services_rendered,
            "total_amount": invoice.total_amount,
            "payment_status": invoice.payment_status,
            "payment_method": invoice.payment_method
        }
    except frappe.DoesNotExistError:
        
        return {"error": "Invoice not found"}
    except Exception as e:
        
        frappe.log_error(f"Error in get_invoice: {str(e)}")
        return {"error": "An error occurred while fetching invoice details"}



@frappe.whitelist(allow_guest=True)
def get_appointments(patient_id):
    """Retrieve all appointments for a patient"""
    appointments = frappe.get_all("Appointment", filters={"patient_id": patient_id}, fields=["*"])
    return appointments


@frappe.whitelist()
def create_appointment(patient_id, doctor_id, appointment_date, appointment_time):
    """Create a new appointment"""
    try:
       
        appointment = frappe.get_doc({
            "doctype": "Appointment",
          "appointment_id":patient_id+doctor_id,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_date": appointment_date,
            "appointment_time": appointment_time,
            "status": "Scheduled"
        })
        
        appointment.insert()
        frappe.db.commit()

        return {"message": "Appointment created successfully", "appointment_id": appointment.name}

    except Exception as e:
        return {"error": str(e)}

@frappe.whitelist(allow_guest=True)
def get_appointmentbyID(appointment_id):
    try:
        # Fetch the appointment record using the appointment_id
        appointment = frappe.get_doc('Appointment', appointment_id)
        # Convert the doc to a dictionary and return it
        return {
            "appointment_id": appointment.appointment_id,
            "patient_id": appointment.patient_id,
            "doctor_id": appointment.doctor_id,
            "appointment_date": appointment.appointment_date,
            "appointment_time": appointment.appointment_time,
            "status": appointment.status
        }
    except frappe.DoesNotExistError:
        # Handle the case where the appointment does not exist
        return {"error": "Appointment not found"}
    except Exception as e:
        # Handle any other exceptions
        return {"error": "An error occurred while fetching appointment details"}

@frappe.whitelist(allow_guest=True)
def get_admission(patient_id):
    """Retrieve the current admission details for a patient"""
    admission = frappe.get_all("Admission", filters={"patient_id": patient_id, "status": "Admitted"}, fields=["*"])
    if not admission:
        frappe.throw(_("No active admission found"), frappe.NotFoundError)
    return admission


@frappe.whitelist(allow_guest=True)
def get_discharge_summary(admission_id):
    """Retrieve discharge summary based on admission_id"""
    discharge_summary = frappe.get_doc("Discharge Summary", {"admission_id": admission_id})
    if not discharge_summary:
        frappe.throw(_("No discharge summary found"), frappe.NotFoundError)
    return discharge_summary.as_dict()


@frappe.whitelist(allow_guest=True)
def get_invoices(patient_id):
    """Retrieve all invoices for a patient"""
    invoices = frappe.get_all("Invoice", filters={"patient_id": patient_id}, fields=["*"])
    return invoices

