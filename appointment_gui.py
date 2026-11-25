import tkinter as tk
from tkinter import messagebox, ttk

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
        form_frame = ttk.Frame(self.root, padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        fields = [
            ("Patient name", self.patient_name_var),
            ("Doctor name", self.doctor_name_var),
            ("Date (YYYY-MM-DD)", self.date_var),
            ("Time (HH:MM)", self.time_var),
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

        add_button = ttk.Button(button_row, text="Add Appointment", command=self.add_appointment)
        add_button.pack(side="left", padx=(0, 8))

        refresh_button = ttk.Button(button_row, text="Refresh", command=self.refresh_appointments)
        refresh_button.pack(side="left")

        list_frame = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        list_frame.pack(fill="both", expand=True)

        ttk.Label(list_frame, text="Appointments").pack(anchor="w")

        self.appointment_list = tk.Listbox(list_frame, height=16)
        self.appointment_list.pack(fill="both", expand=True, pady=(6, 8))

        cancel_button = ttk.Button(list_frame, text="Cancel Selected", command=self.cancel_selected_appointment)
        cancel_button.pack(anchor="e")

    def refresh_appointments(self):
        self.appointment_list.delete(0, tk.END)

        appointments = self.scheduler.list_appointments()
        for appointment in appointments:
            text = (
                f"{appointment.appointment_id}: {appointment.patient_name} | "
                f"{appointment.doctor_name} | {appointment.date} | {appointment.time}"
            )
            self.appointment_list.insert(tk.END, text)

    def add_appointment(self):
        patient_name = self.patient_name_var.get()
        doctor_name = self.doctor_name_var.get()
        date_text = self.date_var.get()
        time_text = self.time_var.get()
        reason = self.reason_var.get()

        try:
            self.scheduler.add_appointment(patient_name, doctor_name, date_text, time_text, reason)
            self.clear_form()
            self.refresh_appointments()
            messagebox.showinfo("Success", "Appointment added successfully.")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def cancel_selected_appointment(self):
        selected_index = self.appointment_list.curselection()

        if not selected_index:
            messagebox.showwarning("No selection", "Select an appointment first.")
            return

        selected_value = self.appointment_list.get(selected_index[0])
        appointment_id = int(selected_value.split(":", 1)[0])

        try:
            self.scheduler.cancel_appointment(appointment_id)
            self.refresh_appointments()
            messagebox.showinfo("Cancelled", f"Appointment #{appointment_id} was cancelled.")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def clear_form(self):
        self.patient_name_var.set("")
        self.doctor_name_var.set("")
        self.date_var.set("")
        self.time_var.set("")
        self.reason_var.set("")


def main():
    root = tk.Tk()
    app = AppointmentApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
