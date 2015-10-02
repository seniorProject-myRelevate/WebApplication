# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyRelevate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demographicdata',
            name='currentRelationshipHappiness',
            field=models.IntegerField(choices=[(0, b'strongly disagree'), (1, b'disagree'), (2, b'neither agree nor disagree'), (3, b'agree'), (4, b'strongly agree')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='religiousInfluence',
            field=models.IntegerField(choices=[(0, b'strongly disagree'), (1, b'disagree'), (2, b'neither agree nor disagree'), (3, b'agree'), (4, b'strongly agree')]),
        ),
    ]
