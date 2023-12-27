from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User as Account
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from .serializers import AccountSerializer

class AccountTests(APITestCase):
    # Test data
    test_user = {'username': 'test_user', 'email': 'test@email.com', 'first_name': 'test_first_name', 'last_name': 'test_last_name'}
    test_user_1 = {'username': 'test_user_1', 'email': 'test1@email.com', 'first_name': 'test1_first_name', 'last_name': 'test1_last_name'}
    test_user_2 = {'username': 'test_user_2', 'email': 'test2@email.com', 'first_name': 'test2_first_name', 'last_name': 'test2_last_name'}
    test_user_3 = {'username': 'test_user_3', 'email': 'test3@email.com', 'first_name': 'test3_first_name', 'last_name': 'test3_last_name'}
    test_user_4 = {'username': 'test_user_4', 'email': 'test4@email.com', 'first_name': 'test4_first_name', 'last_name': 'test4_last_name'}
    test_user_5 = {'username': 'test_user_5', 'email': 'test5@email.com', 'first_name': 'test5_first_name', 'last_name': 'test5_last_name'}

    test_admin = {'username': 'test_admin', 'email': 'admin@email.com', 'first_name': 'admin_first_name', 'last_name': 'admin_last_name'}
    test_admin_1 = {'username': 'test_admin_1', 'email': 'admin1@email.com', 'first_name': 'admin1_first_name', 'last_name': 'admin1_last_name'}
    test_admin_2 = {'username': 'test_admin_2', 'email': 'admin2@email.com', 'first_name': 'admin2_first_name', 'last_name': 'admin2_last_name'}
    test_admin_3 = {'username': 'test_admin_3', 'email': 'admin3@email.com', 'first_name': 'admin3_first_name', 'last_name': 'admin3_last_name'}
    test_admin_4 = {'username': 'test_admin_4', 'email': 'admin4@email.com', 'first_name': 'admin4_first_name', 'last_name': 'admin4_last_name'}
    test_admin_5 = {'username': 'test_admin_5', 'email': 'admin5@email.com', 'first_name': 'admin5_first_name', 'last_name': 'admin5_last_name'}
    
    test_su = {'username': 'test_suser', 'email': 'sutest@email.com', 'first_name': 'su_first_name', 'last_name': 'su_last_name'}
    test_su_1 = {'username': 'test_suser_1', 'email': 'sutest1@email.com', 'first_name': 'su1_first_name', 'last_name': 'su1_last_name'}
    test_su_2 = {'username': 'test_suser_2', 'email': 'sutest2@email.com', 'first_name': 'su2_first_name', 'last_name': 'su2_last_name'}
    test_su_3 = {'username': 'test_suser_3', 'email': 'sutest3@email.com', 'first_name': 'su3_first_name', 'last_name': 'su3_last_name'}
    test_su_4 = {'username': 'test_suser_4', 'email': 'sutest4@email.com', 'first_name': 'su4_first_name', 'last_name': 'su4_last_name'}
    test_su_5 = {'username': 'test_suser_5', 'email': 'sutest5@email.com', 'first_name': 'su5_first_name', 'last_name': 'su5_last_name'}
    
    valid_password = 'StrongPassword123!'
    valid_password_1 = 'SecurePass456!'
    valid_password_2 = 'P@ssw0rd789'

    def test_create_account(self):
        """
        Permissions: IsAdmin
        """
        # Test case 1: Anonymous user - should fail
        response = self.client.post(reverse('account-list'), self.test_user)
        self.assertTrue(status.is_client_error(response.status_code))

        # Test case 2: Regular user - should fail
        account = Account.objects.create_user(self.test_user_1['username'], self.test_user_1['email'], self.valid_password)
        self.client.force_authenticate(user=account)
        response = self.client.post(reverse('account-list'), self.test_user)
        self.assertTrue(status.is_client_error(response.status_code))

        # Test case 3: Admin user - should succeed
        account = Account.objects.create_user(self.test_admin['username'], self.test_admin['email'], self.valid_password, is_staff=True) 
        self.client.force_authenticate(user=account)
        response = self.client.post(reverse('account-list'), self.test_user)
        self.assertIsNotNone(Account.objects.get(username=self.test_user['username']))
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(status.is_success(response.status_code))

    def test_list_acocunts(self):
        Account.objects.create_user(self.test_user_1['username'], self.test_user_1['email'], self.valid_password)
        Account.objects.create_user(self.test_user_2['username'], self.test_user_2['email'], self.valid_password)
        Account.objects.create_user(self.test_user_3['username'], self.test_user_3['email'], self.valid_password)
        Account.objects.create_user(self.test_user_4['username'], self.test_user_4['email'], self.valid_password)
        # Test case 1: Anonymous user - should fail
        response = self.client.get(reverse('account-list'))
        self.assertTrue(status.is_client_error(response.status_code))
        # Test case 2: Regular user - should succeed
        account = Account.objects.create_user(self.test_user['username'], self.test_user['email'], self.valid_password)
        self.client.force_authenticate(user=account)
        response = self.client.get(reverse('account-list'))
        self.assertTrue(status.is_success(response.status_code))
        # Test case 3: Admin user - should succeed
        account = Account.objects.create_user(self.test_admin['username'], self.test_admin['email'], self.valid_password, is_staff=True) 
        self.client.force_authenticate(user=account)
        response = self.client.get(reverse('account-list'))
        self.assertTrue(status.is_success(response.status_code))

    def test_set_password(self):
        """
        Permissions: AllowAny
        """
         # Test case: Setting a new password with a valid token - should succeed
        account = Account.objects.create_user(self.test_user['username'], self.test_user['email'], self.valid_password)
        token = default_token_generator.make_token(account)
        response = self.client.post(reverse('account-set-password', args=[account.id]), {'token': token, 'password': self.valid_password_1} )
        account = Account.objects.get(pk=account.id)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(account.check_password(self.valid_password_1))
        self.assertFalse(account.check_password(self.valid_password))

    def test_login(self):
        """
        Permissions: AllowAny
        """
        # Test case: Logging in with valid credentials - should succeed
        account = Account.objects.create_user(self.test_user['username'], self.test_user['email'], self.valid_password)
        response = self.client.post(reverse('account-login'), { 'username': account.username, 'password': self.valid_password})
        self.assertTrue(status.is_success(response.status_code))

    def test_reset_password(self):
        """
        Permissions: IsAdmin or IsSelf
        """
        account = Account.objects.create_user(self.test_user['username'], self.test_user['email'], self.valid_password)
        
        # Test case 1: Anonymous user - should fail
        response = self.client.get(reverse('account-reset-password', args=[account.id]))
        self.assertTrue(status.is_client_error(response.status_code))

        # Test case 2: Regular user - should fail
        account_op = Account.objects.create_user(self.test_user_1['username'], self.test_user_1['email'], self.valid_password)
        self.client.force_authenticate(user=account_op)
        response = self.client.get(reverse('account-reset-password', args=[account.id]))
        self.assertTrue(status.is_client_error(response.status_code))

        # Test case 3: Same user - should succeed
        self.client.force_authenticate(user=account)

        response = self.client.get(reverse('account-reset-password', args=[account.id]))
        account = Account.objects.get(pk=account.id)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(mail.outbox), 1)
        self.assertFalse(account.check_password(self.valid_password))

        # Test case 4: Admin user - should succeed
        account_op = Account.objects.create_user(self.test_admin['username'], self.test_admin['email'], self.valid_password, is_staff=True) 
        self.client.force_authenticate(user=account_op)
        account.set_password(self.valid_password)

        response = self.client.get(reverse('account-reset-password', args=[account.id]))
        account = Account.objects.get(pk=account.id)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(mail.outbox), 2)
        self.assertFalse(account.check_password(self.valid_password))

    def test_retrieve(self):
        account = Account.objects.create_user(self.test_user_1['username'], self.test_user_1['email'], self.valid_password)

        # Test case 1: Anonymous user - should fail
        response = self.client.get(reverse('account-detail', args=[account.id]))
        self.assertTrue(status.is_client_error(response.status_code))
        # Test case 2: Regular user - should succeed
        account_op = Account.objects.create_user(self.test_user['username'], self.test_user['email'], self.valid_password)
        self.client.force_authenticate(user=account_op)
        response = self.client.get(reverse('account-detail', args=[account.id]))
        self.assertTrue(status.is_success(response.status_code))

    def test_update(self):
        account = Account.objects.create_user(self.test_user_1['username'], self.test_user_1['email'], self.valid_password)
        account_data = AccountSerializer(account).data
        del account_data['last_login']

        # Test case 1: Anonymous user - should fail
        response = self.client.put(reverse('account-detail', args=[account.id]), account_data)
        self.assertTrue(status.is_client_error(response.status_code))

        # Test case 2: Regular user - should fail
        account_op = Account.objects.create_user(self.test_user['username'], self.test_user['email'], self.valid_password)
        self.client.force_authenticate(user=account_op)
        response = self.client.put(reverse('account-detail', args=[account.id]), account_data)
        self.assertTrue(status.is_client_error(response.status_code))

        # Test case 3: Same user - should succeed
        self.client.force_authenticate(user=account)
        response = self.client.put(reverse('account-detail', args=[account.id]), account_data)
        self.assertTrue(status.is_success(response.status_code))

        # Test case 3.1: Priviledge escalation - should fail
        account_data['is_staff'] = True
        response = self.client.put(reverse('account-detail', args=[account.id]), account_data)
        self.assertTrue(status.is_client_error(response.status_code))
        account_data['is_staff'] = False

        account_data['is_superuser'] = True
        response = self.client.put(reverse('account-detail', args=[account.id]), account_data)
        self.assertTrue(status.is_client_error(response.status_code))
        account_data['is_superuser'] = False

        # Test case 4: Admin user- should succeed
        account_op = Account.objects.create_user(self.test_admin['username'], self.test_admin['email'], self.valid_password, is_staff=True) 
        self.client.force_authenticate(user=account_op)
        response = self.client.put(reverse('account-detail', args=[account.id]), account_data)
        self.assertTrue(status.is_success(response.status_code))

        # Test case 4.1: Priviledge escalation - should fail
        account_data['is_superuser'] = True
        response = self.client.put(reverse('account-detail', args=[account.id]), account_data)
        self.assertTrue(status.is_client_error(response.status_code))
        
    def test_partial_update(self):
        account = Account.objects.create_user(self.test_user_1['username'], self.test_user_1['email'], self.valid_password)

        # Test case 1: Anonymous user - should fail
        response = self.client.patch(reverse('account-detail', args=[account.id]), self.test_user_2)
        self.assertTrue(status.is_client_error(response.status_code))

        # Test case 2: Regular user - should fail
        account_op = Account.objects.create_user(self.test_user['username'], self.test_user['email'], self.valid_password)
        self.client.force_authenticate(user=account_op)
        response = self.client.patch(reverse('account-detail', args=[account.id]), self.test_user_2)
        self.assertTrue(status.is_client_error(response.status_code))

        # Test case 3: Same user - should succeed
        self.client.force_authenticate(user=account)
        response = self.client.patch(reverse('account-detail', args=[account.id]), self.test_user_2)
        self.assertTrue(status.is_success(response.status_code))

        # Test case 4: Admin user- should succeed
        account_op = Account.objects.create_user(self.test_admin['username'], self.test_admin['email'], self.valid_password, is_staff=True) 
        self.client.force_authenticate(user=account_op)
        response = self.client.patch(reverse('account-detail', args=[account.id]), self.test_user_2)
        self.assertTrue(status.is_success(response.status_code))

    def test_destroy(self):
        account = Account.objects.create_user(self.test_user_1['username'], self.test_user_1['email'], self.valid_password)

        # Test case 1: Anonymous user - should fail
        response = self.client.delete(reverse('account-detail', args=[account.id]))
        self.assertTrue(status.is_client_error(response.status_code))

        # Test case 2: Regular user - should fail
        account_op = Account.objects.create_user(self.test_user['username'], self.test_user['email'], self.valid_password)
        self.client.force_authenticate(user=account_op)
        response = self.client.delete(reverse('account-detail', args=[account.id]))
        self.assertTrue(status.is_client_error(response.status_code))

        # Test case 3: Same user - should succeed
        self.client.force_authenticate(user=account)
        response = self.client.delete(reverse('account-detail', args=[account.id]))
        self.assertTrue(status.is_success(response.status_code))

        # Test case 4: Admin user- should succeed
        account_op = Account.objects.create_user(self.test_admin['username'], self.test_admin['email'], self.valid_password, is_staff=True) 
        account = Account.objects.create_user(self.test_user_1['username'], self.test_user_1['email'], self.valid_password)
        self.client.force_authenticate(user=account_op)
        response = self.client.delete(reverse('account-detail', args=[account.id]))
        self.assertTrue(status.is_success(response.status_code))