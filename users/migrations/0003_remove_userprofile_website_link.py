# Generated by Django 5.0.2 on 2024-02-27 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='website_link',
        ),
    ]
