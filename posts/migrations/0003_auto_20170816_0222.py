# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-16 09:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20170816_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='follower',
            field=models.ManyToManyField(blank=True, null=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
