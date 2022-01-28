# Generated by Django 4.0 on 2022-01-28 07:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0028_remove_userfollowing_network_userfollowing_unique_relationships_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='follower',
            field=models.ManyToManyField(related_name='following', through='network.UserFollowing', to=settings.AUTH_USER_MODEL),
        ),
    ]