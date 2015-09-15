# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DemographicData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birthday', models.DateField()),
                ('education', models.IntegerField(choices=[(0, b'Completed high school/GED'), (1, b'Some college no longer attending'), (2, b'Some college currently attending'), (3, b'Graduated with bachelors'), (4, b'Graduated with bachelors'), (5, b'Graduated with PhD')])),
                ('employmentStatus', models.CharField(max_length=1, choices=[(b'e', b'employed'), (b'n', b'not employed'), (b's', b'self employed')])),
                ('familySize', models.IntegerField()),
                ('gender', models.CharField(max_length=1, choices=[(b'f', b'female'), (b'm', b'male'), (b't', b'transgender')])),
                ('relationshipStatus', models.CharField(max_length=1, choices=[(b'e', b'engaged'), (b'm', b'married'), (b'r', b'relationship'), (b's', b'single')])),
                ('postalCode', models.CharField(max_length=32)),
                ('race', models.CharField(max_length=2)),
                ('salary', models.IntegerField(choices=[(0, b'Below $10,000'), (1, b'$10,000 - $30,000'), (2, b'$30,000 - $50,000'), (3, b'$50,000 - $80,000'), (4, b'$80,000 - $100,000'), (5, b'$100,000+')])),
                ('sexual_orientation', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('confirmed', models.BooleanField()),
                ('email', models.EmailField(unique=True, max_length=100)),
                ('password', models.CharField(max_length=500)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=150)),
                ('createdDate', models.DateField()),
                ('lastLogin', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='demographicdata',
            name='user',
            field=models.ForeignKey(to='MyRelevate.User'),
        ),
    ]
