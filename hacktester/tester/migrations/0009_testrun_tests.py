# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0008_auto_20161010_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrun',
            name='tests',
            field=models.OneToOneField(to='tester.Test', null=True, blank=True, related_name='test_run'),
        ),
    ]
