# Generated by Django 2.2.11 on 2020-04-20 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_wish'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wish',
            name='quantity',
        ),
    ]
