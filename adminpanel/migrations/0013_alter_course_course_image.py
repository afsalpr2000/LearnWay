# Generated by Django 5.1 on 2024-11-05 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0012_remove_course_course_video_remove_course_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_image',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
    ]
