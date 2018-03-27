# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-27 17:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='postedby',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_quotes', to='quotes.User'),
        ),
    ]
