# Generated by Django 2.2.6 on 2020-01-18 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tribal', '0014_tribalskills_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='name',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='organisation_name',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='password',
        ),
        migrations.AddField(
            model_name='organisation',
            name='desc',
            field=models.CharField(default=' ', max_length=600),
        ),
        migrations.AddField(
            model_name='organisation',
            name='org_name',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='email',
            field=models.CharField(default=' ', max_length=50),
        ),
    ]
