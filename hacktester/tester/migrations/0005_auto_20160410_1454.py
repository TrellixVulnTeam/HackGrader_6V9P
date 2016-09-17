# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hacktester.tester.models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0004_auto_20160410_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='testwithbinaryfile',
            name='solution',
            field=models.FileField(default='', upload_to=hacktester.tester.models.solution_upload_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testwithbinaryfile',
            name='test',
            field=models.FileField(default='', upload_to=hacktester.tester.models.tests_upload_path),
            preserve_default=False,
        ),
    ]
