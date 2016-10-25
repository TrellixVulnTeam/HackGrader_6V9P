# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0009_testrun_tests'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BinaryArchiveTest',
            new_name='ArchiveTest',
        ),
    ]
