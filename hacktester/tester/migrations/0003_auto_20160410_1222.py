# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_data(apps, schema_editor):
    """
    The idea is as follows:
    Migrate existing data from TestRun model to TestWithPlainText

    This is needed because we are going to introduce TestWithBinaryFile
    """

    TestRun = apps.get_model('tester', 'TestRun')
    TestWithPlainText = apps.get_model('tester', 'TestWithPlainText')

    runs = TestRun.objects.all()

    for run in runs:
        plain_text = TestWithPlainText(testrun_ptr_id=run.id)

        plain_text.solution_code = run.code
        plain_text.test_code = run.test

        plain_text.__dict__.update(run.__dict__)

        plain_text.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0002_testwithbinaryfile_testwithplaintext'),
    ]

    operations = [
        migrations.RunPython(migrate_data)
    ]
