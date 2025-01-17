# Generated by Django 5.1 on 2024-11-05 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0013_alter_course_course_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_name', models.CharField(max_length=40)),
                ('course_video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('note', models.FileField(blank=True, null=True, upload_to='pdfs/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminpanel.course')),
            ],
        ),
    ]
