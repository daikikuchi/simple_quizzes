from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test that crate a new user with an email"""
        email = 'kikuchi.dai@gmail.com'
        password = 'testpassword'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'kikuchi.dai@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'testpassword')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        # if value error does not happen, this test fails
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpassword')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        email = 'kikuchi.dai@gmail.com'
        password = 'testpassword'
        admin_user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertTrue(admin_user.email, email)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
