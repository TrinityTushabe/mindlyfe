# Generated by Django 4.2 on 2023-04-30 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
