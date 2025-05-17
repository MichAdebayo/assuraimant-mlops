from __future__ import annotations
from typing import List, Tuple
from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Manager
from django.contrib.auth import get_user_model


class UserProfile(AbstractUser):
    """Extends the default Django user model to include additional personal information
    for users, including physical attributes and lifestyle choices.

    Attributes:
        age (PositiveIntegerField): The user's age. Default is 25.
        weight (PositiveIntegerField): The user's weight in kilograms. Default is 60.
        height (PositiveIntegerField): The user's height in centimeters. Default is 170.
        num_children (PositiveIntegerField): The number of children the user has. Default is 0.
        smoker (CharField): Whether the user is a smoker ('Yes' or 'No').
        region (CharField): Geographical region.
        sex (CharField): Sex ('Male' or 'Female').

    Methods:
        bmi (property) -> float:
            Calculates BMI safely with zero division protection.
        __str__() -> str:
            String representation of the user profile.
    """

    insurance_predictions: Manager[PredictionHistory]

    class SmokerType(models.TextChoices):
        YES = "Yes", "Yes"
        NO = "No", "No"

    class RegionType(models.TextChoices):
        NORTHEAST = "Northeast", "Northeast"
        NORTHWEST = "Northwest", "Northwest"
        SOUTHEAST = "Southeast", "Southeast"
        SOUTHWEST = "Southwest", "Southwest"

    class SexType(models.TextChoices):
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    age: models.PositiveIntegerField = models.PositiveIntegerField(default=25)
    weight: models.PositiveIntegerField = models.PositiveIntegerField(
        default=60, help_text="Weight in kilograms"
    )
    height: models.PositiveIntegerField = models.PositiveIntegerField(
        default=170, help_text="Height in centimeters"
    )
    num_children: models.PositiveIntegerField = models.PositiveIntegerField(default=0)

    smoker: models.CharField = models.CharField(
        max_length=10, choices=SmokerType.choices, blank=False
    )
    region: models.CharField = models.CharField(
        max_length=10, choices=RegionType.choices, blank=False
    )
    sex: models.CharField = models.CharField(
        max_length=10, choices=SexType.choices, blank=False
    )

    @property
    def bmi(self) -> float:
        """Calculate BMI safely with zero division protection."""
        if self.height <= 0:
            return 0.0
        return round(self.weight / ((self.height / 100) ** 2), 1)

    def __str__(self) -> str:
        return self.username


class PredictionHistory(models.Model):
    """
    Represents a record of an insurance prediction for a user.

    Attributes:
        user (ForeignKey): Associated UserProfile.
        timestamp (DateTimeField): Auto-created timestamp.
        age, weight, height, num_children (PositiveIntegerField): User state.
        smoker, region, sex (CharField): User state.
        predicted_charges (DecimalField): Insurance charges prediction.

    Methods:
        bmi (property) -> float:
            Historical BMI calculation.
        __str__() -> str:
            String representation with user and timestamp.
    """

    user: models.ForeignKey[UserProfile] = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="insurance_predictions"
    )
    timestamp: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    age: models.PositiveIntegerField = models.PositiveIntegerField()
    weight: models.PositiveIntegerField = models.PositiveIntegerField()
    height: models.PositiveIntegerField = models.PositiveIntegerField()
    num_children: models.PositiveIntegerField = models.PositiveIntegerField()
    smoker: models.CharField = models.CharField(max_length=10)
    region: models.CharField = models.CharField(max_length=10)
    sex: models.CharField = models.CharField(max_length=10)

    predicted_charges: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Predicted insurance charges in USD"
    )

    class Meta:
        ordering: List[str] = ["-timestamp"]
        verbose_name: str = "Insurance Prediction"
        verbose_name_plural: str = "Insurance Predictions"
        indexes: List[models.Index] = [models.Index(fields=["user", "-timestamp"])]

    @property
    def bmi(self) -> float:
        """Historical BMI calculation."""
        if self.height <= 0:
            return 0.0
        return round(self.weight / ((self.height / 100) ** 2), 1)

    def __str__(self) -> str:
        return f"{self.user} prediction @ {self.timestamp:%Y-%m-%d}"


class JobApplication(models.Model):
    """Job application submitted by a candidate."""

    name: models.CharField = models.CharField(max_length=255)
    email: models.EmailField = models.EmailField()
    resume: models.FileField = models.FileField(upload_to="resumes/")
    cover_letter: models.TextField = models.TextField()

    def __str__(self) -> str:
        return self.name


class Job(models.Model):
    """Represents a job listing."""

    title: models.CharField = models.CharField(max_length=255)
    description: models.TextField = models.TextField()
    location: models.CharField = models.CharField(max_length=100, default="Remote")
    experience: models.CharField = models.CharField(
        max_length=100, default="Not specified"
    )
    job_id: models.AutoField = models.AutoField(primary_key=True)

    def __str__(self) -> str:
        return self.title


class ContactMessage(models.Model):
    """Contact message submitted by a user."""

    name: models.CharField = models.CharField(max_length=255)
    email: models.EmailField = models.EmailField()
    message: models.TextField = models.TextField()
    submitted_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Message from {self.name} ({self.email})"


class Availability(models.Model):
    """Availability of time slots for a specific date."""

    date: models.DateField = models.DateField(unique=True)
    time_slots: models.JSONField = models.JSONField(default=list)

    def __str__(self) -> str:
        return f"{self.date} - {', '.join(self.time_slots)}"


class Appointment(models.Model):
    """Appointment made by a user."""

    REASON_CHOICES: List[Tuple[str, str]] = [
        ("Consultation", "Consultation"),
        ("Insurance Claim", "Insurance Claim"),
        ("Policy Inquiry", "Policy Inquiry"),
    ]

    user: models.ForeignKey = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE
    )
    reason: models.CharField = models.CharField(max_length=50, choices=REASON_CHOICES)
    date: models.DateField = models.DateField(default=date(2025, 2, 3))
    time: models.CharField = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.reason} on {self.date} at {self.time}"
