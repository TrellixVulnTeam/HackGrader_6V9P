# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hacktester.tester.models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0008_auto_20161028_1443'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testwithbinaryfile',
            old_name='tests',
            new_name='tests_file',
        )
    ]
