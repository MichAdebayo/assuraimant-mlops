from typing import Any
from django import forms
from django.contrib import admin
from django.http import HttpRequest
from django.db.models import Field as ModelField

from .models import UserProfile, Job, ContactMessage, Availability, Appointment

# Register your models here.
admin.site.register(UserProfile)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """Admin configuration for the Job model."""

    list_display = ("title", "location", "experience")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin configuration for the ContactMessage model."""

    list_display = ("name", "email", "submitted_at")
    search_fields = ("name", "email", "message")
    list_filter = ("submitted_at",)


class AvailabilityAdminForm(forms.ModelForm):
    """
    Custom admin form for managing Availability objects.

    Provides a multiple choice field for selecting available time slots
    using checkboxes for hours between 09:00 and 18:00.
    """

    TIME_CHOICES = [
        (f"{hour:02d}:00", f"{hour:02d}:00") for hour in range(9, 19)
    ]  # 09:00 - 18:00

    time_slots = forms.MultipleChoiceField(
        choices=TIME_CHOICES, widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Availability
        fields = ["date", "time_slots"]

    def clean_time_slots(self) -> list[str]:
        """
        Ensure the selected time slots are returned as a list.
        """
        return self.cleaned_data["time_slots"]


class AvailabilityAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Availability model.

    Uses a custom form to allow selection of multiple time slots.
    Displays the date and a comma-separated list of available times.
    """

    form = AvailabilityAdminForm
    list_display = ("date", "display_times")

    def display_times(self, obj: Availability) -> str:
        """
        Returns a comma-separated string of available time slots for display.
        """
        return ", ".join(obj.time_slots)


admin.site.register(Availability, AvailabilityAdmin)


class AppointmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Appointment model.

    Provides list display, filtering, search, and customizes the time field choices.
    """

    list_display = ("user", "reason", "date", "time")
    list_filter = ("reason", "date")
    search_fields = ("user__username", "reason", "date")
    date_hierarchy = "date"
    ordering = ("-date",)

    def formfield_for_choice_field(
        self, db_field: ModelField, request: HttpRequest, **kwargs: Any
    ) -> Any:
        """
        Customizes the choices for the 'time' field to be every hour from 09:00 to 18:00.
        """
        if db_field.name == "time" and (
            hasattr(db_field, "choices") or db_field.get_internal_type() == "CharField"
        ):
            kwargs["choices"] = [
                (f"{hour:02}:00", f"{hour:02}:00") for hour in range(9, 19)
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)


admin.site.register(Appointment, AppointmentAdmin)
