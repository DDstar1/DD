# Generated by Django 4.1.3 on 2022-12-18 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_userinfo_points_userpoints'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpoints',
            old_name='points',
            new_name='point',
        ),
    ]