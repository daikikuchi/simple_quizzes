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
