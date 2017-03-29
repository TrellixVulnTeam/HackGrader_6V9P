# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('extension', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='RunResult',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('status', model_utils.fields.StatusField(choices=[('ok', 'ok'), ('not_ok', 'not_ok')], max_length=100, default='ok', no_check_for_status=True)),
                ('output', models.TextField()),
                ('returncode', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', model_utils.fields.StatusField(db_index=True, default='pending', max_length=100, no_check_for_status=True)),
                ('extra_options', jsonfield.fields.JSONField(blank=True, null=True)),
                ('number_of_results', models.IntegerField(default=1)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tester.Language')),
            ],
        ),
        migrations.CreateModel(
            name='TestType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='testrun',
            name='test_type',
            field=models.ForeignKey(to='tester.TestType'),
        ),
        migrations.AddField(
            model_name='runresult',
            name='run',
            field=models.ForeignKey(to='tester.TestRun'),
        ),
    ]
