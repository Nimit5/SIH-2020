# Generated by Django 2.2.6 on 2020-01-17 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tribal', '0005_auto_20200116_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='tribalskills',
            name='img',
            field=models.ImageField(default=' ', upload_to='skillpics'),
        ),
    ]
