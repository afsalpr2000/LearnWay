# Generated by Django 5.1 on 2024-11-05 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0014_coursecontent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_image',
            field=models.ImageField(blank=True, null=True, upload_to='course_imgs'),
        ),
    ]
