# Generated by Django 4.0.4 on 2022-09-02 09:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('phil', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Measurements',
            new_name='Measurements1',
        ),
    ]
