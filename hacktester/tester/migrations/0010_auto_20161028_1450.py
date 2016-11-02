# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hacktester.tester.models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0009_auto_20161028_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrun',
            name='tests',
            field=models.OneToOneField(to='tester.Test', related_name='test_run', null=True, blank=True),
        )
    ]
