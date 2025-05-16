from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from django.db.models import Field as ModelField

from .models import UserProfile, Job, ContactMessage, Availability, Appointment

admin.site.register(UserProfile)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "experience")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "submitted_at")
    search_fields = ("name", "email", "message")
    list_filter = ("submitted_at",)

class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("date", "display_times")

    def display_times(self, obj: Availability) -> str:
        return ", ".join(obj.time_slots)

admin.site.register(Availability, AvailabilityAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("user", "reason", "date", "time")
    list_filter = ("reason", "date")
    search_fields = ("user__username", "reason", "date")
    date_hierarchy = "date"
    ordering = ("-date",)

    def formfield_for_choice_field(
        self, db_field: ModelField, request: HttpRequest, **kwargs: Any
    ) -> Any:
        if db_field.name == "time" and (
            hasattr(db_field, "choices") or db_field.get_internal_type() == "CharField"
        ):
            kwargs["choices"] = [(f"{hour:02}:00", f"{hour:02}:00") for hour in range(9, 19)]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

admin.site.register(Appointment, AppointmentAdmin)
