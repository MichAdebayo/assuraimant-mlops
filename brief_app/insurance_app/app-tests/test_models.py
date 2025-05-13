from datetime import date
from django.test import TestCase
from insurance_app.models import (
    UserProfile,
    PredictionHistory,
    JobApplication,
    Job,
    ContactMessage,
    Availability,
    Appointment,
)

class UserProfileModelTest(TestCase):
    def test_userprofile_creation(self):
        user = UserProfile.objects.create_user(
            username="testuser",
            password="testpass123",
            age=30,
            weight=70,
            height=170,
            num_children=2,
            smoker=UserProfile.SmokerType.NO,
            region=UserProfile.RegionType.NORTHEAST,
            sex=UserProfile.SexType.FEMALE,
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.bmi, 24.2)
        
    def test_bmi_calculation_various_cases(self):
        # Arrange, Act & Assert
        user = UserProfile(username="bmiuser1", weight=60, height=170)
        self.assertEqual(user.bmi, 20.8)  # normal case

        user = UserProfile(username="bmiuser2", weight=0, height=170)
        self.assertEqual(user.bmi, 0.0)  # zero weight

        user = UserProfile(username="bmiuser3", weight=70, height=0)
        self.assertEqual(user.bmi, 0.0)  # zero height

        user = UserProfile(username="bmiuser4", weight=70, height=-10)
        self.assertEqual(user.bmi, 0.0)  # negative height

        user = UserProfile(username="bmiuser5", weight=80, height=180)
        self.assertEqual(user.bmi, 24.7)  # another normal case

class PredictionHistoryModelTest(TestCase):
    def test_predictionhistory_creation(self):
        user = UserProfile.objects.create_user(username="testuser", password="testpass123")
        prediction = PredictionHistory.objects.create(
            user=user,
            age=30,
            weight=70,
            height=170,
            num_children=2,
            smoker=UserProfile.SmokerType.NO,
            region=UserProfile.RegionType.NORTHEAST,
            sex=UserProfile.SexType.FEMALE,
            predicted_charges=1234.56,
        )
        self.assertEqual(prediction.user, user)
        self.assertEqual(prediction.predicted_charges, 1234.56)

    def test_predictionhistory_bmi_calculation_various_cases(self):
            # Arrange
            user = UserProfile.objects.create_user(username="bmi_ph_user", password="testpass123")
            # Act & Assert
            prediction = PredictionHistory(
                user=user, age=30, weight=60, height=170, num_children=0,
                smoker=UserProfile.SmokerType.NO, region=UserProfile.RegionType.NORTHEAST,
                sex=UserProfile.SexType.FEMALE, predicted_charges=1000
            )
            self.assertEqual(prediction.bmi, 20.8)  # normal case

            prediction = PredictionHistory(
                user=user, age=30, weight=0, height=170, num_children=0,
                smoker=UserProfile.SmokerType.NO, region=UserProfile.RegionType.NORTHEAST,
                sex=UserProfile.SexType.FEMALE, predicted_charges=1000
            )
            self.assertEqual(prediction.bmi, 0.0)  # zero weight

            prediction = PredictionHistory(
                user=user, age=30, weight=70, height=0, num_children=0,
                smoker=UserProfile.SmokerType.NO, region=UserProfile.RegionType.NORTHEAST,
                sex=UserProfile.SexType.FEMALE, predicted_charges=1000
            )
            self.assertEqual(prediction.bmi, 0.0)  # zero height

            prediction = PredictionHistory(
                user=user, age=30, weight=70, height=-10, num_children=0,
                smoker=UserProfile.SmokerType.NO, region=UserProfile.RegionType.NORTHEAST,
                sex=UserProfile.SexType.FEMALE, predicted_charges=1000
            )
            self.assertEqual(prediction.bmi, 0.0)  # negative height

            prediction = PredictionHistory(
                user=user, age=30, weight=80, height=180, num_children=0,
                smoker=UserProfile.SmokerType.NO, region=UserProfile.RegionType.NORTHEAST,
                sex=UserProfile.SexType.FEMALE, predicted_charges=1000
            )
            self.assertEqual(prediction.bmi, 24.7)  # another normal case

class JobApplicationModelTest(TestCase):
    def test_jobapplication_creation(self):
        application = JobApplication.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            resume="resume.pdf",
            cover_letter="I am interested in this job."
        )
        self.assertEqual(application.name, "John Doe")
        self.assertEqual(application.email, "john.doe@example.com")

class JobModelTest(TestCase):
    def test_job_creation(self):
        job = Job.objects.create(
            title="Software Engineer",
            description="Develop and maintain software.",
            location="Remote",
            experience="2+ years"
        )
        self.assertEqual(job.title, "Software Engineer")
        self.assertEqual(job.location, "Remote")

class ContactMessageModelTest(TestCase):
    def test_contactmessage_creation(self):
        message = ContactMessage.objects.create(
            name="Jane Smith",
            email="jane.smith@example.com",
            message="I have a question about your services."
        )
        self.assertEqual(message.name, "Jane Smith")
        self.assertEqual(message.email, "jane.smith@example.com")

class AvailabilityModelTest(TestCase):
    def test_availability_creation(self):
        availability = Availability.objects.create(
            date=date(2025, 5, 13),
            time_slots=["09:00", "14:00", "16:00"]
        )
        self.assertEqual(availability.date.strftime("%Y-%m-%d"), "2025-05-13")
        self.assertEqual(availability.time_slots, ["09:00", "14:00", "16:00"])

class AppointmentModelTest(TestCase):
    def test_appointment_creation(self):
        user = UserProfile.objects.create_user(username="testuser", password="testpass123")
        appointment = Appointment.objects.create(
            user=user,
            reason="Consultation",
            date="2025-05-13",
            time="10:00"
        )
        self.assertEqual(appointment.user, user)
        self.assertEqual(appointment.reason, "Consultation")
