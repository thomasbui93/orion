# Generated by Django 2.0 on 2017-12-09 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='user',
        ),
        migrations.DeleteModel(
            name='Token',
        ),
    ]
