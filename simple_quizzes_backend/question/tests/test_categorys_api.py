from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from question.models import Category

from question.serializers import CategorySerializer


CATEGORIES_URL = reverse('question:category-list')


class PublicCategoriesApiTests(TestCase):
    """Test the publicaly available Categories API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving categories"""
        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoriesTests(TestCase):
    """"Test the authorized user categories API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'dai@gmail.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_categories(self):
        """Test retrieving categories"""
        Category.objects.create(user=self.user,)
        Category.objects.create(user=self.user, name='riddle')

        res = self.client.get(CATEGORIES_URL)

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_categories_limited_to_user(self):
        """Test that categories returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'otheruser@gmail.com',
            'user2password',
        )
        Category.objects.create(user=user2, name='riddle')
        category = Category.objects.create(user=self.user,)

        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], category.name)

    def test_create_category_successful(self):
        """Test creating a new category"""
        payload = {'name': 'riddle'}
        self.client.post(CATEGORIES_URL, payload)

        exists = Category.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_category_invalid(self):
        """Test creating a new category with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(CATEGORIES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
