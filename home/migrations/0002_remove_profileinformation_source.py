# Generated by Django 5.1.2 on 2025-03-16 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profileinformation',
            name='source',
        ),
    ]
