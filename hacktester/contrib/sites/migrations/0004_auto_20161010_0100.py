# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.sites.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0003_auto_20160811_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='domain',
            field=models.CharField(verbose_name='domain name', max_length=100, validators=[django.contrib.sites.models._simple_domain_name_validator]),
        ),
    ]
