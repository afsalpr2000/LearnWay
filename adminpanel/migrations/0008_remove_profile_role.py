# Generated by Django 5.1 on 2024-11-03 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0007_alter_profile_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='role',
        ),
    ]
