# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0003_auto_20160410_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testrun',
            name='code',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='test',
        ),
    ]
