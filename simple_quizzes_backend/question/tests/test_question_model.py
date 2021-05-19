from django.test import TestCase
from django.contrib.auth import get_user_model

from question import models


def sample_user(email='dai@gmail.com', password='passwordpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_category_str(self):
        """Test the tag string representation"""
        category = models.Category.objects.create(
            user=sample_user(),
        )
        self.assertEqual(str(category), category.name)
