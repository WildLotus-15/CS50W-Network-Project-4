# Generated by Django 4.0 on 2022-01-26 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0015_remove_post_likes_post_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to='network.user')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='bio',
        ),
    ]