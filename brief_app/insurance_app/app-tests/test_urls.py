from django.test import SimpleTestCase
from django.urls import reverse, resolve
from insurance_app.views import (
    HomeView, SignupView, CustomLoginView, UserLogoutView, WelcomeView, UserProfileView,
    PredictChargesView, PredictionHistoryView, book_appointment, AboutView, JoinUsView,
    apply, contact_view, contact_view_user, ApplyView, HealthAdvicesView, CybersecurityAwarenessView,
    message_list_view, solve_message, predict_charges, ChangePasswordView, get_available_times, TestingView
)
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func.view_class, SignupView)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)

    def test_logout_url_resolves(self):
        url = reverse('logout_user')
        self.assertEqual(resolve(url).func.view_class, UserLogoutView)

    def test_welcome_url_resolves(self):
        url = reverse('welcome')
        self.assertEqual(resolve(url).func.view_class, WelcomeView)

    def test_profile_url_resolves(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func.view_class, UserProfileView)

    def test_predict_charges_url_resolves(self):
        url = reverse('predict')
        self.assertEqual(resolve(url).func.view_class, PredictChargesView)

    def test_prediction_history_url_resolves(self):
        url = reverse('prediction_history')
        self.assertEqual(resolve(url).func.view_class, PredictionHistoryView)

    def test_book_appointment_url_resolves(self):
        url = reverse('book_appointment')
        self.assertEqual(resolve(url).func, book_appointment)

    def test_about_url_resolves(self):
        url = reverse('about')
        self.assertEqual(resolve(url).func.view_class, AboutView)

    def test_join_us_url_resolves(self):
        url = reverse('join_us')
        self.assertEqual(resolve(url).func.view_class, JoinUsView)

    def test_apply_url_resolves(self):
        url = reverse('apply')
        self.assertEqual(resolve(url).func, apply)

    def test_contact_url_resolves(self):
        url = reverse('contact')
        self.assertEqual(resolve(url).func, contact_view)

    def test_contact_form_url_resolves(self):
        url = reverse('contact_form')
        self.assertEqual(resolve(url).func, contact_view_user)

    def test_apply_view_url_resolves(self):
        url = reverse('apply_thank_you')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_health_advices_url_resolves(self):
        url = reverse('health_advices')
        self.assertEqual(resolve(url).func.view_class, HealthAdvicesView)

    def test_cybersecurity_awareness_url_resolves(self):
        url = reverse('cybersecurity_awareness')
        self.assertEqual(resolve(url).func.view_class, CybersecurityAwarenessView)

    def test_messages_list_url_resolves(self):
        url = reverse('messages_list')
        self.assertEqual(resolve(url).func, message_list_view)

    def test_solve_message_url_resolves(self):
        url = reverse('solve_message', args=[1])
        self.assertEqual(resolve(url).func, solve_message)

    def test_predict_charges_function_url_resolves(self):
        url = reverse('predict_charges')
        self.assertEqual(resolve(url).func, predict_charges)

    def test_password_reset_url_resolves(self):
        url = reverse('password_reset')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetView)

    def test_password_reset_done_url_resolves(self):
        url = reverse('password_reset_done')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_confirm_url_resolves(self):
        url = reverse('password_reset_confirm', args=['uidb64', 'token'])
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)

    def test_password_reset_complete_url_resolves(self):
        url = reverse('password_reset_complete')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)

    def test_change_password_url_resolves(self):
        url = reverse('changepassword')
        self.assertEqual(resolve(url).func.view_class, ChangePasswordView)

    def test_get_available_times_url_resolves(self):
        url = reverse('get_available_times')
        self.assertEqual(resolve(url).func, get_available_times)

    def test_testing_url_resolves(self):
        url = reverse('testing')
        self.assertEqual(resolve(url).func.view_class, TestingView)