# Generated by Django 5.1.2 on 2024-12-19 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0005_alter_lesson_classroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='quartergrade',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
