# Generated by Django 3.2.3 on 2021-05-19 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('math', 'Math'), ('riddle', 'Riddle')], default='math', max_length=10),
        ),
    ]
