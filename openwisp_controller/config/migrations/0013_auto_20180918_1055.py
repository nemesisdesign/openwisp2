# Generated by Django 2.0.8 on 2018-09-18 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0012_auto_20180219_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='notes',
            field=models.TextField(blank=True, help_text='internal notes'),
        ),
    ]
