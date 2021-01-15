# Generated by Django 3.0.9 on 2021-01-15 08:23

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0005_auto_20200923_0246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concept',
            name='mnemonic',
            field=models.CharField(db_index=True, max_length=255, validators=[django.core.validators.RegexValidator(regex=re.compile('^[a-zA-Z0-9\\-\\.\\_\\@]+$'))]),
        ),
        migrations.AlterField(
            model_name='concept',
            name='uri',
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
    ]
