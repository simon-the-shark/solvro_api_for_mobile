# Generated by Django 4.2.6 on 2023-10-29 15:19

from django.db import migrations
import taskmanager.user_manager


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='myuser',
            managers=[
                ('objects', taskmanager.user_manager.UserManager()),
            ],
        ),
    ]