# Generated by Django 3.2.3 on 2021-05-23 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0010_alter_question_category'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('name', 'user'), name='unique_category'),
        ),
    ]
