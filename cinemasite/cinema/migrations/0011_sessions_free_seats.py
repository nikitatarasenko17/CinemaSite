# Generated by Django 3.2.5 on 2021-10-02 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0010_remove_sessions_free_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessions',
            name='free_seats',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]