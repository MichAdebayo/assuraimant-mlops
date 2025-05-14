from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from insurance_app.models import ContactMessage, Job, Availability

User = get_user_model()

class SimpleTemplateViewsTest(TestCase):
    def setUp(self):
        """Sets up the test client for each test case.

        This method initializes the Django test client to simulate requests in test cases.
        """
        self.client = Client()

    def test_home_view(self):
        """Test the home view.

        Ensures the home view returns a 200 status code and uses the correct template.
        """
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'insurance_app/home.html')

    def test_about_view(self):
        """Test the about view.

        Ensures the about view returns a 200 status code and uses the correct template.
        """
        resp = self.client.get(reverse('about'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'insurance_app/about.html')

    def test_join_us_view_and_context(self):
        """Test the join us view and its context.

        Ensures the join us view returns a 200 status code, uses the correct template,
        and includes the correct context data (jobs).
        """
        Job.objects.create(title="Job A")
        Job.objects.create(title="Job B")
        resp = self.client.get(reverse('join_us'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'insurance_app/join_us.html')
        self.assertIn('jobs', resp.context)
        self.assertEqual(resp.context['jobs'].count(), 2)

    def test_health_and_cybersecurity_views(self):
        """Test multiple views related to health and cybersecurity.

        Ensures the views return a 200 status code and use the correct templates.
        """
        for name, template in [
            ('health_advices', 'insurance_app/health_advices.html'),
            ('cybersecurity_awareness', 'insurance_app/cybersecurity_awareness.html'),
            ('welcome', 'insurance_app/welcome.html'),
        ]:
            resp = self.client.get(reverse(name))
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateUsed(resp, template)

class FunctionBasedViewsTest(TestCase):
    def setUp(self):
        """Sets up the test client for each test case."""
        self.client = Client()

    def test_apply_redirect_on_get(self):
        """Test the apply view with a GET request.

        Ensures the apply view redirects to the join us page when accessed via GET.
        """
        resp = self.client.get(reverse('apply'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('join_us'))

    def test_apply_post_success(self):
        """Test the apply view with a POST request.

        Ensures the apply view processes the form data correctly and returns a success message.
        """
        data = {'name': 'Alice', 'email': 'a@example.com', 'job_id': '1'}
        resp = self.client.post(reverse('apply'), data)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Application submitted successfully")

    def test_contact_view_and_message_list(self):
        """Test the contact view and the messages list.

        Ensures the contact view renders the form for anonymous users,
        creates a ContactMessage on POST, and allows staff to view the messages list.
        """
        # anonymous GET renders form
        resp = self.client.get(reverse('contact'))
        self.assertEqual(resp.status_code, 200)

        # POST creates a ContactMessage and redirects
        resp = self.client.post(reverse('contact'),
                                {'name': 'Bob', 'email': 'b@b.com', 'message': 'Hi'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(ContactMessage.objects.exists())

        # staff member can view messages list
        staff = User.objects.create_user('staff', 's@s.com', 'pass', is_staff=True)
        self.client.login(username='staff', password='pass')
        resp = self.client.get(reverse('messages_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'insurance_app/messages_list.html')

    def test_solve_message_deletes_and_returns_json(self):
        """Test the solve message view.

        Ensures the solve message view deletes a ContactMessage and returns a JSON response.
        """
        msg = ContactMessage.objects.create(name='X', email='x@x', message='test')
        url = reverse('solve_message', args=[msg.pk])
        resp = self.client.post(url)
        self.assertJSONEqual(resp.content, {'success': True})
        self.assertFalse(ContactMessage.objects.filter(pk=msg.pk).exists())

    def test_get_available_times(self):
        """Test the get available times view.

        Ensures the view returns the correct JSON response based on the provided date
        and available time slots.
        """
        # no date provided
        resp = self.client.get(reverse('get_available_times'))
        self.assertJSONEqual(resp.content, {'times': []})

        # with a date but no availability
        resp = self.client.get(reverse('get_available_times') + '?date=2099-01-01')
        self.assertJSONEqual(resp.content, {'times': []})

        # with an availability
        av = Availability.objects.create(date='2050-12-31', time_slots=["09:00", "10:00"])
        resp = self.client.get(reverse('get_available_times') + '?date=2050-12-31')
        self.assertJSONEqual(resp.content, {'times': ["09:00", "10:00"]})
