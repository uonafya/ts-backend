# Generated by Django 4.1.7 on 2023-04-25 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0066_concept_checksums_conceptdescription_checksums_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='concept',
            name='default_locale',
        ),
        migrations.RemoveField(
            model_name='concept',
            name='description',
        ),
        migrations.RemoveField(
            model_name='concept',
            name='supported_locales',
        ),
        migrations.RemoveField(
            model_name='concept',
            name='website',
        ),
    ]
