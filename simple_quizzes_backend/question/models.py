from django.db import models
from django.conf import settings


class Category(models.Model):
    """Category for quizze"""
    CATEGORY_CHOICES = (
        ('math', 'Math'),
        ('riddle', 'Riddle'),
    )
    name = models.CharField(max_length=10,
                            choices=CATEGORY_CHOICES,
                            default='math')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
    )

    def __str__(self):
        return self.name


class Question(models.Model):
    """Model for question"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    answer = models.TextField()
    category = models.ForeignKey(
        Category,
        related_name='category_questions',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.category} - {self.content}'
