# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('host', models.CharField(max_length=140)),
                ('key', models.CharField(max_length=64)),
                ('secret', models.CharField(max_length=64)),
            ],
        ),
    ]
