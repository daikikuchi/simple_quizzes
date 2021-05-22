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

    def test_question_str(self):
        """Test the question string representation"""
        user = sample_user()
        category = models.Category.objects.create(
            user=user
        )
        question = models.Question.objects.create(
            category=category,
            user=user,
            content='1+1',
            answer='2',
        )
        self.assertEqual(str(question),
                         f'{question.category} - {question.content}')
