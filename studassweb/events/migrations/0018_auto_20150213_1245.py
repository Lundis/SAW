# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20150213_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventitem',
            name='type',
            field=models.CharField(max_length=1, help_text='Decides what kind of data is allowed in this field. The options are:<br />Checkbox: A simple checkbox (yes/no)<br />Text (one line): A text field with one line <br />Text (multiple lines): A larger resizeable text field that allows multiple lines<br />Integer: A number<br />Choice: A multiple-choices field. syntax for name: question//alternative1//alternative2//alternative3', choices=[('B', 'Checkbox'), ('S', 'Text (one line)'), ('T', 'Text (multiple lines)'), ('I', 'Integer'), ('C', 'Choice')], verbose_name='Data type', default='I'),
            preserve_default=True,
        ),
    ]
