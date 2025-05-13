from django.test import TestCase
from insurance_app.forms import (
    PredictChargesForm,
    UserProfileForm,
    UserSignupForm,
    UserLoginForm,
    ApplicationForm,
    ChangePasswordForm,
    AppointmentForm,
)
from insurance_app.models import UserProfile, JobApplication, Appointment

# Use the custom user model for all user creation
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

User = get_user_model()


class PredictChargesFormTest(TestCase):
    def test_valid_data(self):
        form = PredictChargesForm(
            data={
                "age": 30,
                "height": 170,
                "weight": 70,
                "num_children": 2,
                "smoker": UserProfile.SmokerType.NO,
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = PredictChargesForm(data={"age": -1})
        self.assertFalse(form.is_valid())


class UserProfileFormTest(TestCase):
    def test_valid_data(self):
        form = UserProfileForm(
            data={
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "johndoe@example.com",
                "smoker": UserProfile.SmokerType.NO,
                "region": UserProfile.RegionType.NORTHEAST,
                "sex": UserProfile.SexType.MALE,
                "num_children": 2,
                "age": 30,
                "weight": 70,
                "height": 170,
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = UserProfileForm(data={"username": ""})
        self.assertFalse(form.is_valid())


class UserSignupFormTest(TestCase):
    def test_valid_data(self):
        form = UserSignupForm(
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "securepassword123",
            }
        )
        self.assertTrue(form.is_valid())

    def test_password_hashed_on_save(self):
        form = UserSignupForm(
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "securepassword123",
            }
        )
        if form.is_valid():
            user = form.save()
            self.assertNotEqual(user.password, "securepassword123")


class UserLoginFormTest(TestCase):
    def test_valid_data(self):
        form = UserLoginForm(
            data={
                "username": "johndoe",
                "password": "password123",
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = UserLoginForm(data={"username": ""})
        self.assertFalse(form.is_valid())


class ApplicationFormTest(TestCase):
    def test_valid_data(self):
        resume_file = SimpleUploadedFile("resume.txt", b"resume content")
        form = ApplicationForm(
            data={
                "name": "Jane Doe",
                "email": "jane.doe@example.com",
                "cover_letter": "I am interested in this job.",
            },
            files={"resume": resume_file},
        )
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = ApplicationForm(data={"name": ""})
        self.assertFalse(form.is_valid())


class ChangePasswordFormTest(TestCase):
    def test_valid_data(self):
        user = User.objects.create_user(username="testuser", password="oldpassword")
        form = ChangePasswordForm(
            user=user,
            data={
                "old_password": "oldpassword",
                "new_password1": "newsecurepassword123",
                "new_password2": "newsecurepassword123",
            },
        )
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        user = User.objects.create_user(username="testuser", password="oldpassword")
        form = ChangePasswordForm(
            user=user,
            data={
                "old_password": "wrongpassword",
                "new_password1": "newsecurepassword123",
                "new_password2": "newsecurepassword123",
            },
        )
        self.assertFalse(form.is_valid())


class AppointmentFormTest(TestCase):
    def test_valid_data(self):
        user = UserProfile.objects.create_user(
            username="testuser", password="testpass123"
        )
        form = AppointmentForm(
            data={
                "reason": "Consultation",
                "date": date(2025, 5, 13),
                "time": "10:00",
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_time_format(self):
        form = AppointmentForm(
            data={
                "reason": "Consultation",
                "date": date(2025, 5, 13),
                "time": "invalid_time",
            }
        )
        self.assertFalse(form.is_valid())
