# Generated by Django 4.0 on 2022-01-23 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_remove_user_bio_remove_user_follower_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]