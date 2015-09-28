# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('publishDate', models.DateField()),
                ('updateDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='DemographicData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birthday', models.DateField()),
                ('education', models.IntegerField(choices=[(0, b'Completed high school/GED'), (1, b'Some college no longer attending'), (2, b'Some college currently attending'), (3, b'Graduated with bachelors'), (4, b'Graduated with bachelors'), (5, b'Graduated with PhD'), (6, b'Did not complete high school')])),
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
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tagName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TagTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article', models.ForeignKey(to='MyRelevate.Article')),
                ('tag', models.ForeignKey(to='MyRelevate.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=254, db_index=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('confirmed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(to='MyRelevate.User'),
        ),
    ]
