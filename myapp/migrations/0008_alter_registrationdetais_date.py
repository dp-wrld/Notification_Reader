# Generated by Django 4.0.4 on 2022-06-14 09:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_registrationdetais_ncount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationdetais',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
