# Generated by Django 5.1 on 2024-11-10 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0015_alter_course_course_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
