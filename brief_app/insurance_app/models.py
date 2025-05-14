from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date


class UserProfile(AbstractUser):
    """Extends the default Django user model to include additional personal information
    for users, including physical attributes and lifestyle choices.

    This model includes fields for the user's age, weight, height, number of
    children, smoking status, region, and sex. It also provides a BMI calculation
    based on the user's weight and height, with safety checks for division by zero.

    Attributes:
        age (PositiveIntegerField): The user's age. Default is 25.
        weight (PositiveIntegerField): The user's weight in kilograms. Default is 60.
        height (PositiveIntegerField): The user's height in centimeters. Default is 170.
        num_children (PositiveIntegerField): The number of children the user has. Default is 0.
        smoker (CharField): Whether the user is a smoker ('Yes' or 'No').
        region (CharField): The user's geographical region, one of 'Northeast', 'Northwest', 'Southeast', or 'Southwest'.
        sex (CharField): The user's sex ('Male' or 'Female').

    Methods:
        bmi (property):
            Calculates the user's BMI based on weight and height.
            If the height is zero or negative, it returns 0.0 to avoid division by zero errors.

        __str__():
            Returns a string representation of the user profile, using the username field.
            Example: 'johndoe'

    Nested Enum-like Classes:
        SmokerType (TextChoices): Defines the choices for the smoker field ('Yes' or 'No').
        RegionType (TextChoices): Defines the choices for the region field ('Northeast', 'Northwest', 'Southeast', 'Southwest').
        SexType (TextChoices): Defines the choices for the sex field ('Male' or 'Female').

    Args:
        username (str): The user's username (inherits from AbstractUser).
        password (str): The user's password (inherits from AbstractUser).
        age (int): The user's age (default: 25).
        weight (int): The user's weight in kilograms (default: 60).
        height (int): The user's height in centimeters (default: 170).
        num_children (int): The number of children the user has (default: 0).
        smoker (str): Whether the user is a smoker ('Yes' or 'No').
        region (str): The user's geographical region (one of 'Northeast', 'Northwest', 'Southeast', 'Southwest').
        sex (str): The user's sex ('Male' or 'Female').

    Returns:
        str: The string representation of the user profile (username).
    """

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

    # Personal Info
    age = models.PositiveIntegerField(default=25)
    weight = models.PositiveIntegerField(default=60, help_text="Weight in kilograms")
    height = models.PositiveIntegerField(default=170, help_text="Height in centimeters")
    num_children = models.PositiveIntegerField(default=0)

    # Choice-based Fields
    smoker = models.CharField(blank=False, max_length=10, choices=SmokerType.choices)
    region = models.CharField(
        blank=False,
        max_length=10,
        choices=RegionType.choices,
    )
    sex = models.CharField(
        blank=False,
        max_length=10,
        choices=SexType.choices,
    )

    # Calculated Property
    @property
    def bmi(self):
        """Calculate BMI safely with zero division protection."""
        if self.height <= 0:
            return 0.0
        return round(self.weight / ((self.height / 100) ** 2), 1)

    def __str__(self):
        return f"{self.username}"


class PredictionHistory(models.Model):
    """Represents a record of an insurance prediction for a user.

    This model stores the details of a user's historical insurance prediction,
    including the user's personal information at the time of the prediction and
    the predicted insurance charges.

    Attributes:
        user (ForeignKey): A reference to the associated user profile for the prediction.
        timestamp (DateTimeField): The date and time when the prediction was created.
        age (PositiveIntegerField): The user's age at the time of the prediction.
        weight (PositiveIntegerField): The user's weight (in kg) at the time of the prediction.
        height (PositiveIntegerField): The user's height (in cm) at the time of the prediction.
        num_children (PositiveIntegerField): The number of children the user has.
        smoker (CharField): Whether the user is a smoker ('Yes' or 'No').
        region (CharField): The geographical region the user is in.
        sex (CharField): The user's sex ('Male' or 'Female').
        predicted_charges (DecimalField): The predicted insurance charges in USD.

    Methods:
        bmi (property):
            Calculates the user's BMI based on their weight and height.
            If the height is less than or equal to zero, it returns 0.0.
        __str__():
            Returns a string representation of the prediction, showing the user and timestamp.
            Example: 'John Doe prediction @ 2025-02-01'

    Meta:
        ordering (list): Orders predictions by timestamp in descending order.
        verbose_name (str): The singular name for the prediction record.
        verbose_name_plural (str): The plural name for the prediction records.
        indexes (list): Adds an index for efficient querying of user predictions by timestamp.

    Args:
        user (UserProfile): The user for whom the insurance prediction was made.
        timestamp (datetime): The timestamp of the prediction.
        age (int): The user's age at the time of the prediction.
        weight (int): The user's weight at the time of the prediction.
        height (int): The user's height at the time of the prediction.
        num_children (int): The number of children the user has.
        smoker (str): Whether the user is a smoker ('Yes' or 'No').
        region (str): The geographical region of the user.
        sex (str): The user's sex ('Male' or 'Female').
        predicted_charges (Decimal): The predicted charges in USD.

    Returns:
        str: The string representation of the insurance prediction.
    """

    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="insurance_predictions"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    # Frozen User State
    age = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    num_children = models.PositiveIntegerField()
    smoker = models.CharField(max_length=10)
    region = models.CharField(max_length=10)
    sex = models.CharField(max_length=10)

    # Prediction Result
    predicted_charges = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Predicted insurance charges in USD"
    )

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Insurance Prediction"
        verbose_name_plural = "Insurance Predictions"
        indexes = [
            models.Index(fields=["user", "-timestamp"]),
        ]

    # Derived Field
    @property
    def bmi(self):
        """Preserve historical BMI calculation."""
        if self.height <= 0:
            return 0.0
        return round(self.weight / ((self.height / 100) ** 2), 1)

    def __str__(self):
        return f"{self.user} prediction @ {self.timestamp:%Y-%m-%d}"


# For the join us job application form
class JobApplication(models.Model):
    """Represents a job application submitted by a candidate.

    This model stores the details of a candidate’s application for a job, including their name,
    email address, uploaded resume, and cover letter.

    Attributes:
        name (CharField): The full name of the applicant.
        email (EmailField): The email address of the applicant.
        resume (FileField): The resume of the applicant, uploaded to the 'resumes/' directory.
        cover_letter (TextField): A text field for the applicant's cover letter.

    Methods:
        __str__():
            Returns the name of the applicant as a string representation of the application.
            Example: 'John Doe'

    Args:
        name (str): The full name of the job applicant.
        email (str): The email address of the job applicant.
        resume (File): The file containing the applicant’s resume.
        cover_letter (str): The text content of the applicant's cover letter.

    Returns:
        str: The name of the applicant as a string.
    """

    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField()

    def __str__(self):
        return self.name


class Job(models.Model):
    """Represents a job listing in the application.

    This model stores information about a specific job position, including its title, description,
    location, experience requirements, and a unique job ID.

    Attributes:
        title (CharField): The title or name of the job position.
        description (TextField): A detailed description of the job role and responsibilities.
        location (CharField): The location of the job, defaulting to 'Remote'.
        experience (CharField): The experience required for the job, defaulting to 'Not specified'.
        job_id (AutoField): A unique identifier for the job listing, automatically assigned by Django.

    Methods:
        __str__():
            Returns the job title as a string representation of the job listing.
            Example: 'Software Developer'

    Args:
        title (str): The name or title of the job position.
        description (str): The detailed description of the job.
        location (str): The location of the job (e.g., 'Remote', 'New York').
        experience (str): The experience required for the job (e.g., '2+ years', 'Not specified').
        job_id (int): The unique job identifier (automatically generated).

    Returns:
        str: The title of the job position as a string.
    """

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100, default="Remote")
    experience = models.CharField(max_length=100, default="Not specified")
    job_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Represents a contact message submitted by a user.

    This model stores information about a contact message, including the sender's name, email,
    the content of the message, and the timestamp when the message was submitted.

    Attributes:
        name (CharField): The name of the person submitting the message.
        email (EmailField): The email address of the person submitting the message.
        message (TextField): The content of the contact message.
        submitted_at (DateTimeField): The timestamp when the message was submitted. It is automatically set to the current time when the message is created.

    Methods:
        __str__():
            Returns a string representation of the contact message, which includes the sender's name and email.
            Example: 'Message from John Doe (john.doe@example.com)'

    Args:
        name (str): The name of the person sending the message.
        email (str): The email address of the person sending the message.
        message (str): The content of the message.
        submitted_at (datetime): The timestamp when the message was submitted (automatically set by Django).

    Returns:
        str: A string representing the contact message in a readable format.
    """

    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class Availability(models.Model):
    """Represents the availability of time slots for a specific date.

    This model stores the available time slots for a given date, where each date has a
    list of available times. The time slots are stored as a JSON field for flexibility,
    and the date field is unique, ensuring that each date can only have one set of time slots.

    Attributes:
        date (DateField): The date for which the availability is being tracked. This field is unique.
        time_slots (JSONField): A JSON field that stores a list of available time slots for the given date.

    Methods:
        __str__():
            Returns a string representation of the availability, combining the date and time slots.
            Example: '2025-01-31 - 09:00, 14:00, 16:00'

    Args:
        date (datetime.date): The date for which the availability is recorded.
        time_slots (list): A list of strings representing the available time slots for that date.

    Returns:
        str: A string that represents the date and available time slots in a readable format.
    """

    date = models.DateField(unique=True)
    time_slots = models.JSONField(default=list)  # Store available times as a list

    def __str__(self):
        return f"{self.date} - {', '.join(self.time_slots)}"


class Appointment(models.Model):
    """Represents an appointment made by a user.

    This model stores the details of an appointment, including the user who made the appointment,
    the reason for the appointment, the date and time of the appointment, and the reason for the appointment.

    Attributes:
        user (ForeignKey): A reference to the user who made the appointment. This is a foreign key to the user model.
        reason (CharField): A field to store the reason for the appointment, with choices like 'Consultation',
                             'Insurance Claim', and 'Policy Inquiry'.
        date (DateField): The date of the appointment. The default date is set to February 3, 2025.
        time (CharField): The time of the appointment, stored as a string in the format of HH:MM.

    Methods:
        __str__():
            Returns a string representation of the appointment, including the reason, date, and time.
            Example: 'Consultation on 2025-02-03 at 10:00'

    Args:
        user (User): The user who is making the appointment.
        reason (str): The reason for the appointment (e.g., 'Consultation', 'Insurance Claim', etc.).
        date (datetime.date): The date the appointment is scheduled for.
        time (str): The time the appointment is scheduled for (e.g., '10:00').

    Returns:
        str: A string that represents the appointment in a readable format.
    """

    REASON_CHOICES = [
        ("Consultation", "Consultation"),
        ("Insurance Claim", "Insurance Claim"),
        ("Policy Inquiry", "Policy Inquiry"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    date = models.DateField(default=date(2025, 2, 3))  # Correct default date
    time = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.reason} on {self.date} at {self.time}"
