# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0006_problemtest_test_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='problemtest',
            name='language',
        ),
        migrations.RemoveField(
            model_name='problemtest',
            name='problem',
        ),
        migrations.RenameField(
            model_name='testrun',
            old_name='code',
            new_name='problem_code',
        ),
        migrations.AddField(
            model_name='testrun',
            name='language',
            field=models.ForeignKey(default='Python', to='tester.Language'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testrun',
            name='problem_test',
            field=models.TextField(),
        ),
        migrations.DeleteModel(
            name='Problem',
        ),
        migrations.DeleteModel(
            name='ProblemTest',
        ),
        migrations.AddField(
            model_name='testrun',
            name='test_type',
            field=models.ForeignKey(default='unittest', to='tester.TestType'),
            preserve_default=False,
        ),
    ]
