# Generated by Django 4.2.1 on 2023-05-10 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0002_like_post_like_post_like_user'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'post')},
        ),
    ]
