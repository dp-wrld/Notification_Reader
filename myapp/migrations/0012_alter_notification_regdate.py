# Generated by Django 4.0.4 on 2022-04-15 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_notification_ntime_registrationdetais_ntime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='RegDate',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]