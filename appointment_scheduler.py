import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


DATA_FILE = Path("appointments.json")


@dataclass
class Appointment:
    """Represents one scheduled appointment."""
    appointment_id: int
    patient_name: str
    doctor_name: str
    date: str
    time: str
    reason: str = ""

    @classmethod
    def from_dict(cls, data):
        """Create an Appointment object from a dictionary."""
        return cls(
            appointment_id=data["appointment_id"],
            patient_name=data["patient_name"],
            doctor_name=data["doctor_name"],
            date=data["date"],
            time=data["time"],
            reason=data.get("reason", ""),
        )

    def to_dict(self):
        """Convert the appointment to a dictionary for JSON storage."""
        return asdict(self)


class AppointmentRepository:
    """Handles loading and saving appointments from a JSON file."""

    def __init__(self, data_file=DATA_FILE):
        self.data_file = Path(data_file)

    def load(self):
        """Load appointments from the JSON file."""
        if not self.data_file.exists():
            return []

        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            raise ValueError("Appointment file is corrupted and could not be loaded.")
        except OSError:
            raise ValueError("Appointment file could not be read.")

        if not isinstance(data, list):
            return []

        return data

    def save(self, appointments):
        """Save appointments to the JSON file."""
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(appointments, file, indent=2)


class AppointmentScheduler:
    def __init__(self, repository=None, data_file=DATA_FILE):
        self.repository = repository or AppointmentRepository(data_file)
        self.appointments = self.load_appointments()
        self.next_id = self.get_next_id()

    def load_appointments(self):
        """Load saved appointments from the repository."""
        raw_appointments = self.repository.load()
        return [Appointment.from_dict(appointment) for appointment in raw_appointments]

    def save_appointments(self):
        """Save the appointment list to the repository."""
        appointment_data = [appointment.to_dict() for appointment in self.appointments]
        self.repository.save(appointment_data)

    def get_next_id(self):
        """Find the next appointment ID based on saved appointments."""
        if not self.appointments:
            return 1

        ids = [appointment.appointment_id for appointment in self.appointments]
        return max(ids) + 1

    @staticmethod
    def validate_date(date_text):
        """Check whether the date matches YYYY-MM-DD."""
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_time(time_text):
        """Check whether the time matches HH:MM."""
        try:
            datetime.strptime(time_text, "%H:%M")
            return True
        except ValueError:
            return False

    def is_slot_available(self, doctor_name, date_text, time_text):
        """Return True if no existing appointment matches that doctor/time."""
        for appointment in self.appointments:
            if (
                appointment.doctor_name.lower() == doctor_name.lower()
                and appointment.date == date_text
                and appointment.time == time_text
            ):
                return False
        return True

    def add_appointment(self, patient_name, doctor_name, date_text, time_text, reason=""):
        """Add one appointment and save it to the data file."""
        if not patient_name.strip():
            raise ValueError("Patient name is required.")
        if not doctor_name.strip():
            raise ValueError("Doctor name is required.")
        if not self.validate_date(date_text):
            raise ValueError("Date must be in YYYY-MM-DD format.")
        if not self.validate_time(time_text):
            raise ValueError("Time must be in HH:MM format.")
        normalized_doctor_name = doctor_name.strip()
        if not self.is_slot_available(normalized_doctor_name, date_text, time_text):
            raise ValueError(
                f"That date and time are already booked for Dr. {normalized_doctor_name}."
            )

        appointment = Appointment(
            appointment_id=self.next_id,
            patient_name=patient_name.strip(),
            doctor_name=normalized_doctor_name,
            date=date_text,
            time=time_text,
            reason=reason.strip(),
        )

        self.appointments.append(appointment)
        self.next_id += 1
        self.save_appointments()
        return appointment

    def list_appointments(self):
        """Return appointments sorted by date and time."""
        return sorted(self.appointments, key=lambda appt: (appt.date, appt.time))

    def cancel_appointment(self, appointment_id):
        """Remove and return one appointment if it exists."""
        for index, appointment in enumerate(self.appointments):
            if appointment.appointment_id == appointment_id:
                cancelled = self.appointments.pop(index)
                self.save_appointments()
                return cancelled
        raise ValueError(f"Appointment {appointment_id} not found.")



def display_appointments(appointments):
    """Print a list of appointments in a readable format."""
    if not appointments:
        print("No appointments scheduled.")
        return

    for appointment in appointments:
        print(
            f"ID: {appointment.appointment_id} | "
            f"Patient: {appointment.patient_name} | "
            f"Doctor: {appointment.doctor_name} | "
            f"Date: {appointment.date} | "
            f"Time: {appointment.time}"
        )


def add_appointment_from_input(scheduler):
    """Prompt for appointment information and add it."""
    patient_name = input("Patient name: ")
    doctor_name = input("Doctor name: ")
    date_text = input("Appointment date (YYYY-MM-DD): ")
    time_text = input("Appointment time (HH:MM): ")
    reason = input("Reason for visit (optional): ")

    try:
        appointment = scheduler.add_appointment(
            patient_name, doctor_name, date_text, time_text, reason
        )
        print(f"Appointment booked successfully: #{appointment.appointment_id}")
    except ValueError as error:
        print(f"Error: {error}")


def cancel_appointment_from_input(scheduler):
    """Prompt for an ID and cancel that appointment."""
    try:
        appointment_id = int(input("Enter appointment ID to cancel: "))
        cancelled = scheduler.cancel_appointment(appointment_id)
        print(
            f"Cancelled appointment #{cancelled.appointment_id} for "
            f"{cancelled.patient_name}"
        )
    except ValueError as error:
        print(f"Error: {error}")


def main():
    try:
        scheduler = AppointmentScheduler()
    except ValueError as error:
        print(f"Error: {error}")
        return

    while True:
        print("\nDoctor's Office Appointment Scheduler")
        print("1. Add appointment")
        print("2. View appointments")
        print("3. Cancel appointment")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_appointment_from_input(scheduler)
        elif choice == "2":
            display_appointments(scheduler.list_appointments())
        elif choice == "3":
            cancel_appointment_from_input(scheduler)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
