from django import forms
from .models import UserProfile
from .models import JobApplication, Appointment
from django.utils.html import format_html
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.forms import DateInput


class PredictChargesForm(forms.ModelForm):
    """
    Form for predicting insurance charges based on user profile information.

    This form allows users to input their personal details, such as age,
    height, weight, number of children, and smoking status, in order to
    predict insurance charges. It is based on the `UserProfile` model.

    Attributes:
        age: The user's age, which helps in predicting insurance charges.
        height: The user's height in centimeters, used to calculate BMI.
        weight: The user's weight in kilograms, used to calculate BMI.
        num_children: The number of children the user has, affecting the prediction.
        smoker: The user's smoking status, which influences the prediction.

    Methods:
        clean_age():
            Validates the age field to ensure it's within a reasonable range.
        clean_height():
            Validates the height field to ensure it's a positive value.
        clean_weight():
            Validates the weight field to ensure it's a positive value.
        clean_num_children():
            Validates the number of children field to ensure it's a non-negative value.
        clean_smoker():
            Validates the smoker field to ensure it contains a valid choice.

    """

    class Meta:
        model = UserProfile
        fields = ["age", "height", "weight", "num_children", "smoker"]


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information, based on the UserProfile model.

    This form is used to update various details of a user's profile, including
    personal information like name, username, email, as well as health-related
    details like age, weight, height, and lifestyle information like smoking status,
    region, and sex. The form provides an interface for users to update their profile
    information in the application.

    Attributes:
        first_name: The user's first name.
        last_name: The user's last name.
        username: The username of the user.
        email: The user's email address.
        smoker: The smoking status of the user (Yes or No).
        region: The region where the user is located.
        sex: The gender of the user.
        num_children: The number of children the user has.
        age: The user's age.
        weight: The user's weight (in kilograms).
        height: The user's height (in centimeters).

    Methods:
        save(commit=True):
            Saves the updated user profile to the database. If commit is True,
            the user profile is saved; otherwise, it is just returned without saving.
    """

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "smoker",
            "region",
            "sex",
            "num_children",
            "age",
            "weight",
            "height",
        ]


class UserSignupForm(forms.ModelForm):
    """
    Form for user signup, based on the UserProfile model.

    This form is used for creating a new user. It includes fields for the username,
    email, and password. The password field uses a password input widget to hide
    the user's input for security. Upon submission, the form hashes the password
    before saving the user to the database.

    Attributes:
        username: The username of the user signing up.
        email: The email address of the user signing up.
        password: The password of the user, entered as a hidden field for security.

    Methods:
        save(commit=True):
            Saves the user object to the database after hashing the password.
            If commit is set to True, the user is saved to the database; otherwise,
            it is just returned without being saved.
    """

    password = forms.CharField(
        widget=forms.PasswordInput, label="Password"
    )  # Password field with hidden input

    class Meta:
        model = UserProfile
        fields = ["username", "email", "password"]  # Fields displayed in the form

    def save(self, commit=True):
        user = super().save(
            commit=False
        )  # Create a user object without saving it to the database yet
        user.password = make_password(
            self.cleaned_data["password"]
        )  # Hash the password before saving
        if commit:
            user.save()  # Save the user to the database
        return user


class UserLoginForm(forms.Form):
    """
    Form for user login.

    This form is used to authenticate users by collecting their username and
    password. It is not based on a model but rather provides fields for the user
    to input their login credentials. The password field is hidden for security
    purposes.

    Attributes:
        username: The username of the user attempting to log in.
        password: The password of the user attempting to log in, entered as a
                  hidden field for security.
    """

    username = forms.CharField(
        max_length=150, label="Username"
    )  # Field for the username
    password = forms.CharField(
        widget=forms.PasswordInput, label="Password"
    )  # Password field with hidden input


class ApplicationForm(forms.ModelForm):
    """
    Form for submitting a job application.

    This form is used for candidates to apply for a job by providing their name,
    email, resume, and cover letter. The resume is optional, while the name, email,
    and cover letter are required fields. The form is linked to the `JobApplication`
    model for storing the application data.

    Attributes:
        name: The name of the applicant.
        email: The email address of the applicant.
        resume: The applicant's resume file (optional).
        cover_letter: The applicant's cover letter.
    """

    class Meta:
        model = JobApplication  # This will be the model for storing application data
        fields = ["name", "email", "resume", "cover_letter"]

    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    resume = forms.FileField(required=False)
    cover_letter = forms.CharField(widget=forms.Textarea, required=True)


class ChangePasswordForm(PasswordChangeForm):
    """
    Form for changing the user's password.

    This form allows the user to update their password by entering their current
    password and providing a new password (and confirming it). The form includes
    validation for password strength and ensures that the new password meets
    security requirements. It also customizes labels and adds help text with
    password guidelines for the user.

    Attributes:
        old_password: The current password field, required for verification.
        new_password1: The new password field, which must meet security criteria.
        new_password2: A confirmation field for the new password, ensuring it matches.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the ChangePasswordForm with custom labels, help text, and styles.

        Customizes the labels of the password fields, adds helpful text to
        guide users on password requirements, and applies Tailwind CSS styles
        to the form fields for consistent styling.
        """
        super().__init__(*args, **kwargs)

        # Customize labels for password fields
        self.fields["old_password"].label = "Current Password"
        self.fields["new_password1"].label = "New Password"
        self.fields["new_password2"].label = "Confirm New Password"

        # Add help text for new password requirements
        self.fields["new_password1"].help_text = format_html(
            '<ul class="text-sm text-gray-600 mt-2">'
            "<li>Your password must be at least 8 characters long.</li>"
            "<li>Your password cannot be entirely numeric.</li>"
            "<li>Your password cannot be too similar to your other personal information.</li>"
            "</ul>"
        )

        # Add Tailwind CSS classes to form fields for styling
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-400",
                }
            )


class AppointmentForm(forms.ModelForm):
    """
    Form for creating or updating an appointment.

    This form allows users to select a reason for the appointment, specify the
    date, and choose a time. It includes validation for the time field to ensure
    it follows the correct format (HH:MM, 24-hour clock). The date field is
    rendered with a custom widget for better styling.

    Attributes:
        reason: The reason for the appointment, selected from predefined choices.
        date: The date of the appointment, displayed with a date picker.
        time: The time of the appointment, validated to ensure it follows the HH:MM format.
    """

    class Meta:
        model = Appointment
        fields = ["reason", "date", "time"]
        widgets = {
            "date": DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control w-full bg-gray-100 rounded-md p-2",
                }
            ),
        }

    def clean_time(self):
        """
        Validates the time field to ensure it follows the HH:MM format.

        Checks if the time entered is not empty and adheres to a valid 24-hour
        clock format. Raises a validation error if the time is invalid.

        Returns:
            str: The validated time string in HH:MM format.

        Raises:
            forms.ValidationError: If the time format is invalid.
        """
        time = self.cleaned_data.get("time")
        try:
            if not time:
                raise forms.ValidationError("This field is required.")
            hour, minute = map(int, time.split(":"))
            if not (0 <= hour < 24 and 0 <= minute < 60):
                raise forms.ValidationError("Enter a valid time in HH:MM format.")
        except ValueError:
            raise forms.ValidationError("Time should be in HH:MM format.")
        return time
