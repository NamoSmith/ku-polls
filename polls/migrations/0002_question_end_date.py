# Generated by Django 3.2.6 on 2021-10-09 14:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='ending date'),
        ),
    ]
