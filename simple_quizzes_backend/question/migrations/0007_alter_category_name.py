# Generated by Django 3.2.3 on 2021-05-20 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_alter_question_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('math', 'Math'), ('riddle', 'Riddle')], default='math', max_length=10, unique=True),
        ),
    ]
