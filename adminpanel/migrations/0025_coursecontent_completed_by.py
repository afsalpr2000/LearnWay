# Generated by Django 5.1 on 2024-11-18 15:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0024_remove_question_asked_by_remove_question_course_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecontent',
            name='completed_by',
            field=models.ManyToManyField(blank=True, related_name='completed_contents', to=settings.AUTH_USER_MODEL),
        ),
    ]
