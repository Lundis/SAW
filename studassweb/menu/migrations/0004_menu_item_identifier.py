# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_default_identifiers(apps, schema_editor):
    print(apps)
    MenuItem = apps.get_model("menu", "menuitem")
    db_alias = schema_editor.connection.alias
    items = MenuItem.objects.using(db_alias).all()
    for item in items:
        item.identifier = item.app_name + "_" + item.display_name
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_mainmenusettings_inverted_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='identifier',
            field=models.CharField(unique=True, null=True, default=None, max_length=100),
            preserve_default=True,
        ),
        migrations.RunPython(
            set_default_identifiers,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='identifier',
            field=models.CharField(unique=True, null=True, default=None, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='menuitem',
            unique_together=set([]),
        ),
    ]
