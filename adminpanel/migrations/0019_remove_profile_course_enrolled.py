# Generated by Django 5.1 on 2024-11-17 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0018_enrollment_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='course_enrolled',
        ),
    ]