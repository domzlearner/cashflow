# Generated by Django 5.0.4 on 2024-10-27 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_email_verified',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='security_answer',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='security_question',
        ),
    ]