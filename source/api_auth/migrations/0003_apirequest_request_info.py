# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0002_auto_20160103_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='apirequest',
            name='request_info',
            field=models.CharField(max_length=140, default='POST /grade'),
            preserve_default=False,
        ),
    ]
