# Generated by Django 3.2.5 on 2021-10-02 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0009_alter_purchase_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessions',
            name='free_seats',
        ),
    ]
