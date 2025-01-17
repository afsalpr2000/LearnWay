# Generated by Django 5.1 on 2024-11-18 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0023_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='asked_by',
        ),
        migrations.RemoveField(
            model_name='question',
            name='course',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='course',
        ),
        migrations.RemoveField(
            model_name='quizquestion',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quizoption',
            name='question',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Quiz',
        ),
        migrations.DeleteModel(
            name='QuizOption',
        ),
        migrations.DeleteModel(
            name='QuizQuestion',
        ),
    ]
