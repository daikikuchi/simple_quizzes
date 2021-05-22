from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from question.models import Question, Category

from question.serializers import QuestionSerializer, QuestionDetailSerializer

QUESTIONS_URL = reverse('question:question-list')


def detail_url(question_id):
    """return question detail URL"""
    return reverse('question:question-detail', args=[question_id])


def sample_question(user, category, **params):
    defaults = {
        'content': '1+1',
        'answer': '2',
        'category': category
    }
    defaults.update(params)

    return Question.objects.create(user=user, **defaults)


class PublicQuestionApiTests(TestCase):
    """Test unauthenticated question API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(QUESTIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateQuestionApiTests(TestCase):
    """Test authenticated question API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'dai@gmail.com',
            'password'
        )
        self.category = Category.objects.create(user=self.user)
        self.client.force_authenticate(self.user)

    def test_retrieve_questions(self):
        """Test retrieving a list of questions"""
        sample_question(user=self.user, category=self.category)
        sample_question(user=self.user, category=self.category)

        res = self.client.get(QUESTIONS_URL)

        questions = Question.objects.all().order_by('-id')
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_questions_limited_to_user(self):
        """Test retrieving questions for user"""
        user2 = get_user_model().objects.create_user(
            'user2@gmail.com',
            'password2'
        )
        sample_question(user=self.user, category=self.category)
        sample_question(user=user2, category=self.category)

        res = self.client.get(QUESTIONS_URL)

        questions = Question.objects.filter(user=self.user)
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_question_detail(self):
        """Test Viewing a question detail"""
        question = sample_question(user=self.user, category=self.category)

        url = detail_url(question.id)
        res = self.client.get(url)
        serializer = QuestionDetailSerializer(question)
        self.assertEqual(res.data, serializer.data)

    def test_create_question(self):
        """Test creating question"""
        payload = {
            'content': '1+1',
            'answer': '2',
            'category': self.category.id,
        }
        res = self.client.post(QUESTIONS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        question = Question.objects.get(id=res.data['id'])

        # Check if correct values are assigned to Question model
        self.assertEqual(payload['content'], question.content)
        self.assertEqual(payload['answer'], question.answer)
        self.assertEqual(payload['category'], self.category.id)

    def test_partial_update_question(self):
        """Test updating a question with patch"""
        question = sample_question(user=self.user, category=self.category)
        another_category = Category.objects.create(
                           user=self.user, name='riddle'
                           )

        payload = {'content': '2+2', 'category': another_category.id}
        # Use detail url to update
        url = detail_url(question.id)
        self.client.patch(url, payload)

        question.refresh_from_db()

        self.assertEqual(question.content, payload['content'])
        category = Category.objects.get(id=another_category.id)
        self.assertEqual(question.category.id, category.id)

    def test_full_update_question(self):
        """Test updating a question with put"""
        question = sample_question(user=self.user, category=self.category)
        another_category = Category.objects.create(
                           user=self.user, name='riddle')

        payload = {'content': 'パンはパンでも食べられないパンは？', 'answer': 'フライパン',
                   'category': another_category.id}
        # Use detail url to update
        url = detail_url(question.id)
        self.client.put(url, payload)

        question.refresh_from_db()
        self.assertEqual(question.content, payload['content'])
        self.assertEqual(question.answer, payload['answer'])
        self.assertEqual(question.category, another_category)
