# Generated by Django 4.2.6 on 2023-11-03 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0002_myuser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
