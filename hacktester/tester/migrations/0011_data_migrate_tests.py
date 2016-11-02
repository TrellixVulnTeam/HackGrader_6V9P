# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    def migrate(apps, schema_editor):
        TestWithPlainText = apps.get_model('tester', 'TestWithPlainText')
        TestWithBinaryFile = apps.get_model('tester', 'TestWithBinaryFile')

        PlainUnittest = apps.get_model('tester', 'PlainUnittest')
        BinaryUnittest = apps.get_model('tester', 'BinaryUnittest')

        for t in TestWithPlainText.objects.all():
            plain_unittest = PlainUnittest.objects.create(tests=t.test_code)
            t.tests = plain_unittest
            t.save()

        for t in TestWithBinaryFile.objects.all():
            binary_unittest = BinaryUnittest.objects.create(tests=t.tests_file)
            t.tests = binary_unittest
            t.save()

    dependencies = [
        ('tester', '0010_auto_20161028_1450'),
    ]

    operations = [
        migrations.RunPython(migrate)
    ]
