# Generated by Django 4.2.6 on 2023-10-29 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproffesion',
            name='proffesion',
            field=models.CharField(choices=[('FRONTEND', 'Frontend'), ('BACKEND', 'Backend'), ('DEVOPS', 'Devops'), ('UX/UI', 'Ux Ui')], max_length=20),
        ),
    ]
