# Generated by Django 4.0.4 on 2022-05-18 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationdetais',
            name='androidid1',
        ),
        migrations.RemoveField(
            model_name='registrationdetais',
            name='androidid2',
        ),
    ]