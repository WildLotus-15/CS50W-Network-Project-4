# Generated by Django 4.0 on 2022-01-27 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0025_remove_userprofile_followers_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='userfollowing',
            constraint=models.UniqueConstraint(fields=('from_user', 'to_user'), name='network_userfollowing_unique_relationships'),
        ),
    ]