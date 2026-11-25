import os
import tempfile
import unittest

from appointment_scheduler import AppointmentRepository, AppointmentScheduler


class AppointmentSchedulerTests(unittest.TestCase):
    def setUp(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        temp_file.close()
        self.temp_file = temp_file.name

        with open(self.temp_file, "w", encoding="utf-8") as file:
            file.write("[]")

        self.scheduler = AppointmentScheduler(repository=AppointmentRepository(self.temp_file))

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_add_appointment_success(self):
        appointment = self.scheduler.add_appointment(
            "Alice Smith",
            "Dr. Jones",
            "2026-11-01",
            "09:00",
            "Checkup",
        )

        self.assertEqual(appointment.patient_name, "Alice Smith")
        self.assertEqual(appointment.doctor_name, "Dr. Jones")
        self.assertEqual(len(self.scheduler.list_appointments()), 1)

    def test_duplicate_appointment_is_rejected(self):
        self.scheduler.add_appointment(
            "Alice Smith",
            "Dr. Jones",
            "2026-11-01",
            "09:00",
            "Checkup",
        )

        with self.assertRaises(ValueError):
            self.scheduler.add_appointment(
                "Bob Smith",
                "Dr. Jones",
                "2026-11-01",
                "09:00",
                "Follow-up",
            )

    def test_invalid_date_is_rejected(self):
        with self.assertRaises(ValueError):
            self.scheduler.add_appointment(
                "Alice Smith",
                "Dr. Jones",
                "2026/11/01",
                "09:00",
                "Checkup",
            )

    def test_cancel_appointment_removes_it(self):
        appointment = self.scheduler.add_appointment(
            "Alice Smith",
            "Dr. Jones",
            "2026-11-01",
            "09:00",
            "Checkup",
        )

        cancelled = self.scheduler.cancel_appointment(appointment.appointment_id)

        self.assertEqual(cancelled.patient_name, "Alice Smith")
        self.assertEqual(len(self.scheduler.list_appointments()), 0)


if __name__ == "__main__":
    unittest.main()
