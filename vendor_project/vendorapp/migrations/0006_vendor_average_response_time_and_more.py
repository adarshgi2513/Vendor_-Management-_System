# Generated by Django 5.0.4 on 2024-05-02 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0005_rename_response_time_avg_historicalperformance_average_response_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='average_response_time',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vendor',
            name='on_time_delivery_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vendor',
            name='quality_rating_avg',
            field=models.FloatField(default=0),
        ),
    ]