# Generated by Django 3.2.9 on 2021-11-16 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_uername_chat_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='coin',
            new_name='mining_time',
        ),
        migrations.AddField(
            model_name='profile',
            name='token',
            field=models.FloatField(default=0),
        ),
    ]
