# Generated by Django 5.0.4 on 2024-05-02 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0004_remove_historicalperformance_average_response_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalperformance',
            old_name='response_time_avg',
            new_name='average_response_time',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='average_response_time',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='on_time_delivery_rate',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='quality_rating_avg',
        ),
    ]
