# Generated by Django 4.1.3 on 2022-12-18 16:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_rename_points_userpoints_point'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserPoints',
            new_name='UserPoint',
        ),
    ]
