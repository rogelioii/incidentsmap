# Generated by Django 2.2.4 on 2019-08-15 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cad', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incident',
            name='id',
        ),
        migrations.AlterField(
            model_name='incident',
            name='incident_number',
            field=models.CharField(max_length=12, primary_key=True, serialize=False),
        ),
    ]
