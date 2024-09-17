


document.addEventListener('DOMContentLoaded', function () {
    // Fetch current logged-in user's email
    frappe.call({
        method: 'healthcare.healthcare.healthcare_api.get_current_user',
        callback: function (data) {
            const email = data.message.email;
            if (!email) {
                alert('Failed to retrieve user email.');
                return;
            }

            // Fetch patient ID by email
            frappe.call({
                method: 'healthcare.healthcare.healthcare_api.get_patient_id_by_email',
                args: { email: email },
                callback: function (data) {
                    const patientId = data.message;
                    if (!patientId) {
                        alert('Patient ID not found.');
                        return;
                    }

                    // Fetch doctors list
                    frappe.call({
                        method: 'healthcare.healthcare.healthcare_api.get_doctors',
                        callback: function (data) {
                            const doctors = data.message;
                            const doctorSelect = document.getElementById('doctor');
                            
                            doctors.forEach(function(doctor) {
                                const option = document.createElement('option');
                                option.value = doctor.doctor_id;
                                option.textContent = `${doctor.first_name} ${doctor.last_name}`;
                                doctorSelect.appendChild(option);
                            });
                        },
                        error: function (error) {
                            console.error('Error fetching doctors list:', error);
                            alert('Failed to fetch doctors list.');
                        }
                    });

                    // Handle form submission
                    document.getElementById('appointment-form').addEventListener('submit', function(e) {
                        e.preventDefault();

                        const doctorId = document.getElementById('doctor').value;
                        const appointmentDate = document.getElementById('appointment_date').value;
                        const appointmentTime = document.getElementById('appointment_time').value;

                        frappe.call({
                            method: 'healthcare.healthcare.healthcare_api.create_appointment',
                            args: {
                                patient_id: patientId,
                                doctor_id: doctorId,
                                appointment_date: appointmentDate,
                                appointment_time: appointmentTime
                            },
                            callback: function (data) {
                                if (data.message) {
                                    alert('Appointment booked successfully!');
                                } else {
                                    alert('Failed to book appointment.');
                                }
                            },
                            error: function (error) {
                                console.error('Error booking appointment:', error);
                                alert('Failed to book appointment.');
                            }
                        });
                    });
                },
                error: function (error) {
                    console.error('Error fetching patient ID:', error);
                    alert('Failed to fetch patient ID.');
                }
            });
        },
        error: function (error) {
            console.error('Error fetching current user email:', error);
            alert('Failed to fetch current user email.');
        }
    });
});
