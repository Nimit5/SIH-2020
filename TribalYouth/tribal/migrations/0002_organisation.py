# Generated by Django 2.2.6 on 2020-01-16 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tribal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=25)),
                ('name', models.CharField(max_length=80)),
                ('mobile', models.IntegerField(max_length=13)),
                ('organisation_name', models.CharField(max_length=100)),
            ],
        ),
    ]