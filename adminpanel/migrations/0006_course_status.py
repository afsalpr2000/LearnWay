# Generated by Django 5.1 on 2024-10-21 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0005_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[('hidden', 'Hidden'), ('visible', 'Visible')], default='Visible', max_length=20),
        ),
    ]
