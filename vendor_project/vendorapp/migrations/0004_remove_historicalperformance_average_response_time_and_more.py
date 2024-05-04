# Generated by Django 5.0.4 on 2024-05-02 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0003_historicalperformance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalperformance',
            name='average_response_time',
        ),
        migrations.AddField(
            model_name='historicalperformance',
            name='response_time_avg',
            field=models.FloatField(default=0.0),
        ),
    ]