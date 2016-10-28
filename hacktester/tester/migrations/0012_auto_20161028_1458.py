# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0011_data_migrate_tests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testwithbinaryfile',
            name='tests_file',
        ),
        migrations.RemoveField(
            model_name='testwithplaintext',
            name='test_code',
        ),
    ]
