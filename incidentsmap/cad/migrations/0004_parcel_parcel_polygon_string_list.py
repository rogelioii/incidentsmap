# Generated by Django 2.2.4 on 2019-08-15 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cad', '0003_auto_20190815_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='parcel_polygon_string_list',
            field=models.TextField(default=''),
        ),
    ]
