import tkinter as tk

from tkinter import messagebox, simpledialog, ttk

from appointment_scheduler import AppointmentScheduler


class AppointmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Scheduler")
        self.root.geometry("700x500")

        self.scheduler = AppointmentScheduler()
        self.patient_name_var = tk.StringVar()
        self.doctor_name_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.reason_var = tk.StringVar()

        self.build_ui()
        self.refresh_appointments()

    def build_ui(self):
        form_frame = tk.ttk.Frame(self.root, padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        fields = [
            ("Patient Name", self.patient_name_var),
            ("Doctor Name", self.doctor_name_var),
            ("Date", self.date_var),
            ("Time", self.time_var),
            ("Reason", self.reason_var),
        ]

        for label_text, variable in fields:
            row = ttk.Frame(form_frame)
            row.pack(fill="x", pady=4)

            label = ttk.Label(row, text=label_text, width=18)
            label.pack(side="left")

            entry = ttk.Entry(row, textvariable=variable)
            entry.pack(side="left", fill="x", expand=True)

        button_row = ttk.Frame(form_frame)
        button_row.pack(fill="x", pady=8)

        add_button = ttk.Button(
            button_row, text="Add Appointment", command=self.add_appointments
        )
        add_button.pack(side="left", padx=(0, 8))
        refresh_button = ttk.Button(
            button_row, text="Refresh", command=self.refresh_appointments
        )
        refresh_button.pack(side="left")

        list_frame = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        list_frame.pack(fill="both", expand=True)
        ttk.Label(list_frame, text="Appointment").pack(anchor="w")

        self.appointment_list = tk.Listbox(list_frame, height=16)
        self.appointment_list.pack(fill="both", expand=True, pady=(0, 8))

        cancel_button = ttk.Button(
            list_frame, text="Cancel Selected", command=self.cancel_selected_appointment
        )
        cancel_button.pack(anchor="e")

    def cancel_selected_appointment(self):
        pass

    def refresh_appointments(self):
        self.appointment_list.delete(0, tk.END)

        appointments = self.scheduler.list_appointments()

        for appointment in appointments:
            text = (
                f"{appointment.appointment_id}: {appointment.patient_name} | "
                f"{appointment.doctor_name} | {appointment.date} | {appointment.time}"
            )
        self.appointment_list.insert(tk.END, text)

    def add_appointments(self):
        patient_name = self.patient_name_var.get()
        doctor_name = self.doctor_name_var.get()
        date_text = self.date_var.get()
        time_text = self.time_var.get()
        reason = self.reason_var.get()

        try:
            self.scheduler.add_appointment(
                patient_name, doctor_name, date_text, time_text, reason
            )
            self.clear_form()
            self.refresh_appointments()
            messagebox.showinfo("Succes", "Appointment added")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def clear_form(self):
        self.patient_name_var.set("")
        self.doctor_name_var.set("")
        self.date_var.set("")
        self.time_var.set("")
        self.reason_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppointmentApp(root)
    root.mainloop()
