# Generated by Django 3.2.3 on 2021-05-21 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0007_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('math', 'Math'), ('riddle', 'Riddle')], default='math', max_length=10),
        ),
    ]
