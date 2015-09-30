# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyRelevate', '0002_auto_20150928_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demographicdata',
            name='addictive',
            field=models.CharField(blank=True, max_length=1, choices=[(b'n', b'never'), (b'r', b'rarely'), (b's', b'sometimes'), (b'o', b'often'), (b'f', b'frequently')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='addictiveOther',
            field=models.CharField(blank=True, max_length=1, choices=[(b'n', b'never'), (b'r', b'rarely'), (b's', b'sometimes'), (b'o', b'often'), (b'f', b'frequently')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='breakups',
            field=models.CharField(blank=True, max_length=1, choices=[(b'n', b'never'), (b'r', b'rarely'), (b's', b'sometimes'), (b'o', b'often'), (b'f', b'frequently')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='breakupsOther',
            field=models.CharField(blank=True, max_length=1, choices=[(b'n', b'never'), (b'r', b'rarely'), (b's', b'sometimes'), (b'o', b'often'), (b'f', b'frequently')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='currentRelationshipHappiness',
            field=models.IntegerField(blank=True, choices=[(0, b'strongly disagree'), (1, b'disagree'), (2, b'neither agree nor disagree'), (3, b'agree'), (4, b'strongly agree')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='education',
            field=models.IntegerField(blank=True, choices=[(0, b'Completed high school/GED'), (1, b'Some college no longer attending'), (2, b'Some college currently attending'), (3, b'Graduated with bachelors'), (4, b'Graduated with bachelors'), (5, b'Graduated with PhD'), (6, b'Did not complete high school')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='employmentStatus',
            field=models.CharField(blank=True, max_length=1, choices=[(b'p', b'part time'), (b'f', b'full time'), (b'n', b'not employed'), (b's', b'student')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='infidelity',
            field=models.CharField(blank=True, max_length=1, choices=[(b'n', b'never'), (b'r', b'rarely'), (b's', b'sometimes'), (b'o', b'often'), (b'f', b'frequently')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='infidelityOther',
            field=models.CharField(blank=True, max_length=1, choices=[(b'n', b'never'), (b'r', b'rarely'), (b's', b'sometimes'), (b'o', b'often'), (b'f', b'frequently')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='race',
            field=models.CharField(blank=True, max_length=1, choices=[(b'a', b'asian'), (b'b', b'black'), (b'h', b'hispanic/latino'), (b'w', b'white'), (b'i', b'native american/alaskan'), (b'o', b'other')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='relationshipStatus',
            field=models.CharField(blank=True, max_length=1, choices=[(b's', b'single'), (b'c', b'casually dating'), (b'r', b'seriously dating'), (b'o', b'committed'), (b'e', b'engaged'), (b'm', b'married'), (b'j', b'just talking')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='religion',
            field=models.CharField(blank=True, max_length=1, choices=[(b'c', b'christianity'), (b'j', b'judaism'), (b'i', b'islam'), (b'b', b'buddhism'), (b'h', b'hinduism'), (b'a', b'atheism'), (b'g', b'agnostic'), (b'n', b'none'), (b'o', b'other')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='religiousInfluence',
            field=models.IntegerField(blank=True, choices=[(0, b'strongly disagree'), (1, b'disagree'), (2, b'neither agree nor disagree'), (3, b'agree'), (4, b'strongly agree')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='salary',
            field=models.IntegerField(blank=True, choices=[(0, b'Below $10,000'), (1, b'$10,000 - $30,000'), (2, b'$30,000 - $50,000'), (3, b'$50,000 - $80,000'), (4, b'$80,000 - $100,000'), (5, b'$100,000+')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='sex',
            field=models.CharField(blank=True, max_length=1, choices=[(b'f', b'female'), (b'm', b'male'), (b't', b'transgender'), (b'q', b'queer')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='sexualPreference',
            field=models.CharField(blank=True, max_length=1, choices=[(b'm', b'men'), (b'b', b'men and women'), (b'w', b'women'), (b'o', b'otheruser = models.ForeignKey(User)')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='verbalEmotionalAbuse',
            field=models.CharField(blank=True, max_length=1, choices=[(b'n', b'never'), (b'r', b'rarely'), (b's', b'sometimes'), (b'o', b'often'), (b'f', b'frequently')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='verbalEmotionalAbuseOther',
            field=models.CharField(blank=True, max_length=1, choices=[(b'n', b'never'), (b'r', b'rarely'), (b's', b'sometimes'), (b'o', b'often'), (b'f', b'frequently')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='violence',
            field=models.CharField(blank=True, max_length=1, choices=[(b'n', b'never'), (b'r', b'rarely'), (b's', b'sometimes'), (b'o', b'often'), (b'f', b'frequently')]),
        ),
        migrations.AlterField(
            model_name='demographicdata',
            name='violenceOther',
            field=models.CharField(blank=True, max_length=1, choices=[(b'n', b'never'), (b'r', b'rarely'), (b's', b'sometimes'), (b'o', b'often'), (b'f', b'frequently')]),
        ),
    ]
