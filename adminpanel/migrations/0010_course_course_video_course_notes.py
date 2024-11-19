# Generated by Django 5.1 on 2024-11-04 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0009_rename_course_mentor_course_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
        migrations.AddField(
            model_name='course',
            name='notes',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/'),
        ),
    ]