from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Contact
from django.contrib.auth.models import User as Account

# Create your tests here.
class ContactTests(APITestCase):
    test_contact = {
        'email': 'test@email.com',
        'subject': 'Inquiry about Your Product',
        'message': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
    }

    test_admin = {'username': 'test_admin', 'email': 'admin@email.com', 'first_name': 'admin_first_name', 'last_name': 'admin_last_name'}
    valid_password = 'StrongPassword123!'

    def test_create_contact(self):
        response = self.client.post(reverse('contact-list'), self.test_contact)
        self.assertTrue(status.is_success(response.status_code))
        self.assertIsNotNone(Contact.objects.get(email=self.test_contact['email']))

    def test_list_contact(self):
        account = Account.objects.create_user(self.test_admin['username'], self.test_admin['email'], self.valid_password, is_staff=True) 
        Contact(email = self.test_contact['email'],subject = self.test_contact['subject'], message = self.test_contact['message']).save()
        self.client.force_authenticate(user=account)
        response = self.client.get(reverse('contact-list'))
        self.assertTrue(status.is_success(response.status_code))