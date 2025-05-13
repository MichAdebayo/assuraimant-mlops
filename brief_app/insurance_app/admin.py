from django.contrib import admin
from .models import UserProfile, Job, ContactMessage, Availability
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import Appointment

# Register your models here.
admin.site.register(UserProfile)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Job model in the Django admin interface.

    This class customizes how the `Job` model is displayed and managed in the
    Django admin panel. It defines which fields should be displayed in the
    list view for the `Job` model and allows the admin to manage job listings 
    efficiently.

    Attributes:
        list_display: A tuple of field names to display in the list view of 
                      the Job model. Includes 'title', 'location', and 
                      'experience'.

    Methods:
        None. This class inherits from `ModelAdmin` and uses its default 
        functionality with some customizations.

    Example:
        In the Django admin, job listings will be displayed with the title, 
        location, and experience level.
    """
    list_display = ('title', 'location', 'experience')



@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ContactMessage model in the Django admin interface.

    This class customizes how the `ContactMessage` model is displayed and 
    managed in the Django admin panel. It defines which fields should be 
    displayed in the list view, allows searching for messages by name, email, 
    or content, and provides filtering options based on submission date.

    Attributes:
        list_display: A tuple of field names to display in the list view 
                      of the ContactMessage model. Includes 'name', 'email', 
                      and 'submitted_at'.
        search_fields: A tuple of field names that are searchable in the admin 
                       interface. Includes 'name', 'email', and 'message'.
        list_filter: A tuple of field names for filtering records in the list 
                     view. Includes 'submitted_at' for filtering by the submission date.

    Methods:
        None. This class inherits from `ModelAdmin` and uses its default 
        functionality with customizations for displaying and filtering data.

    Example:
        In the Django admin, contact messages can be viewed by name, email, 
        and submission date, and filtered by the 'submitted_at' field.
    """
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('submitted_at',)



class AvailabilityAdminForm(forms.ModelForm):
    """
    Form for managing availability data in the Django admin interface.

    This form is used to manage the availability of time slots for specific dates 
    within the Django admin interface. The form includes multiple time slots that 
    can be selected by the user for each specific date.

    Attributes:
        TIME_CHOICES: A list of tuples representing time slots from 09:00 AM to 
                      06:00 PM (inclusive) with each hour formatted as "HH:00".
        time_slots: A MultipleChoiceField with checkboxes that allows the admin 
                    to select multiple time slots for the selected date.
    
    Methods:
        clean_time_slots: This method ensures the selected time slots are returned 
                          as a list and performs any necessary validation.
    
    Example:
        In the admin panel, an admin user can select multiple available time slots 
        for a given date using checkboxes from 09:00 AM to 06:00 PM.
    """
    TIME_CHOICES = [(f"{hour:02d}:00", f"{hour:02d}:00") for hour in range(9, 19)]  # 09:00 - 18:00

    time_slots = forms.MultipleChoiceField(choices=TIME_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Availability
        fields = ['date', 'time_slots']

    def clean_time_slots(self):
        """
        Ensures the selected time slots are returned as a list.

        This method validates the time slots selected by the admin user and 
        ensures that they are returned in a consistent list format.

        Returns:
            list: A list of selected time slots from the form data.
        """
        return self.cleaned_data['time_slots']  # Ensure list format


class AvailabilityAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Availability model.

    This class customizes the admin interface for the Availability model to manage 
    the availability of time slots for specific dates. It uses a custom form for 
    handling the time slots and displays the selected time slots in a user-friendly format.

    Attributes:
        form: The form used to manage availability data in the admin panel, which 
              includes time slots as multiple checkboxes.
        list_display: Specifies the fields to display in the admin list view. 
                      It shows the date of availability and the formatted time slots.
    
    Methods:
        display_times: A method that formats the time slots as a comma-separated 
                       string for display in the admin list view.

    Example:
        In the admin panel, availability entries are displayed with the date and 
        a list of selected time slots in a comma-separated format. Admins can use 
        the form to manage time slots for each date.
    """
    form = AvailabilityAdminForm
    list_display = ['date', 'display_times']

    def display_times(self, obj):
        """
        Formats the selected time slots as a comma-separated string.

        This method is used to display the selected time slots for each availability 
        entry in the admin list view.

        Args:
            obj (Availability): The Availability object being displayed.

        Returns:
            str: A comma-separated list of selected time slots.
        """
        return ", ".join(obj.time_slots)

admin.site.register(Availability, AvailabilityAdmin)



class AppointmentAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Appointment model.

    This class customizes the Django admin interface for managing appointments, 
    offering a user-friendly way to view, filter, search, and organize appointment data. 
    It also provides time slot customization for appointment scheduling.

    Attributes:
        list_display: Specifies the fields to display in the admin list view. 
                      It shows the user, reason, date, and time of the appointment.
        list_filter: Adds filter options for the admin list view, allowing filtering 
                     by appointment reason and date.
        search_fields: Allows searching through the appointments by user username, 
                       reason, and date.
        date_hierarchy: Adds a hierarchical date filter to the admin interface, 
                         enabling easy navigation by date.
        ordering: Specifies the default ordering of appointments, with the most recent 
                  appointments displayed first (by date descending).
    
    Methods:
        formfield_for_choice_field: Customizes the choices for the "time" field to 
                                     show available time slots from 09:00 to 18:00.

    Example:
        In the admin panel, appointments are displayed with the user, reason, date, 
        and time. Admins can filter appointments by reason and date, search by user 
        or reason, and view appointments in chronological order, with time slots 
        presented as choices between 09:00 and 18:00.
    """
    list_display = ('user', 'reason', 'date', 'time')
    list_filter = ('reason', 'date')
    search_fields = ('user__username', 'reason', 'date')
    date_hierarchy = 'date'
    ordering = ('-date',)

    # def formfield_for_choice_field(self, db_field, request, **kwargs):
    #     """
    #     Customizes the choices for the time field.

    #     This method is used to provide predefined time slots from 09:00 to 18:00 
    #     for the "time" field in the appointment form.

    #     Args:
    #         db_field (Field): The database field being customized.
    #         request (HttpRequest): The HTTP request object.
    #         kwargs (dict): Additional arguments for customizing the field.

    #     Returns:
    #         Field: The customized choice field with time slot options.
    #     """
    #     if db_field.name == 'time':
    #         kwargs['choices'] = [(f"{hour:02}:00", f"{hour:02}:00") for hour in range(9, 19)]
    #     return super().formfield_for_choice_field(db_field, request, **kwargs)

def formfield_for_choice_field(self, db_field, request, **kwargs):
        """
        Customizes the choices for the time field.

        This method is used to provide predefined time slots from 09:00 to 18:00 
        for the "time" field in the appointment form.

        Args:
            db_field (Field): The database field being customized.
            request (HttpRequest): The HTTP request object.
            kwargs (dict): Additional arguments for customizing the field.

        Returns:
            Field: The customized choice field with time slot options.
        """
        if db_field.name == 'time' and (hasattr(db_field, 'choices') or db_field.get_internal_type() == 'CharField'):
            kwargs['choices'] = [(f"{hour:02d}:00", f"{hour:02d}:00") for hour in range(9, 19)]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

# Register the model and custom admin
admin.site.register(Appointment, AppointmentAdmin)
