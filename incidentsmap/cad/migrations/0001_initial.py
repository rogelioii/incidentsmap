# Generated by Django 2.2.4 on 2019-08-15 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parcel_owner_name', models.CharField(max_length=100)),
                ('parcel_mail_address', models.TextField()),
                ('parcel_land_value', models.FloatField()),
                ('parcel_land_sq_ft', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_number', models.CharField(max_length=12)),
                ('incident_latitude', models.FloatField()),
                ('incident_longitude', models.FloatField()),
                ('incident_address_string', models.CharField(max_length=200)),
                ('incident_type', models.CharField(max_length=100)),
                ('incident_sub_type', models.CharField(max_length=100)),
                ('incident_day_of_week', models.CharField(max_length=8)),
                ('incident_event_opened', models.DateTimeField()),
                ('incident_event_closed', models.DateTimeField()),
                ('incident_response_zone', models.CharField(max_length=10)),
                ('incident_units_involved', models.CharField(max_length=200)),
                ('incident_weather_description', models.TextField()),
                ('incident_parcel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cad.Parcel')),
            ],
        ),
    ]
