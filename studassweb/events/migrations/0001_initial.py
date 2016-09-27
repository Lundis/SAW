# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import events.models
import django.core.validators
import base.fields


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('text', base.fields.ValidatedRichTextField(verbose_name='Description')),
                ('start', models.DateTimeField(verbose_name='Event ends')),
                ('stop', models.DateTimeField(verbose_name='Event starts')),
                ('signup_start', models.DateTimeField(verbose_name='Signup starts', default=django.utils.timezone.now)),
                ('signup_deadline', models.DateTimeField(verbose_name='Deadline for signups')),
                ('permission', models.CharField(
                    choices=[
                        ('can_view_and_join_public_events', 'Public event'),
                        ('can_view_and_join_member_events', 'Members-only event'),
                        ('can_view_and_join_board_member_events', 'Board members-only event')],
                    default='can_view_and_join_public_events', max_length=100)),
                ('max_participants', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)],
                                                         default=50)),
                ('use_captcha', models.BooleanField(verbose_name='Use captcha when anonymous people sign up',
                                                    default=False)),
                ('send_email_for_reserves', models.BooleanField(
                    verbose_name='Send email when someone is moved from reserve list to attending', default=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('required', models.BooleanField(verbose_name='Is this field mandatory', default=False)),
                ('public', models.BooleanField(verbose_name='Is this field shown to everyone?', default=False)),
                ('hide_in_print_view', models.BooleanField(verbose_name='Is this field hidden from the print view?',
                                                           default=False)),
                ('type', models.CharField(choices=[('B', 'Checkbox'), ('S', 'Text (one line)'),
                                                   ('T', 'Text (multiple lines)'), ('I', 'Integer'), ('C', 'Choice')],
                                          verbose_name='Data type', default='I',
                                          help_text='Decides what kind of data is allowed in this field. ' +
                                                    'The options are:<br />Checkbox: A simple checkbox (yes/no)<br />' +
                                                    'Text (one line): A text field with one line <br />Text (multiple' +
                                                    ' lines): A larger resizeable text field that allows multiple ' +
                                                    'lines<br />Integer: A number<br />Choice: A multiple-choices ' +
                                                    'field. syntax for name: question//alternative1//alternative2//' +
                                                    'alternative3',
                                          max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('is_setup', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventSignup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Full name', max_length=100)),
                ('email', models.EmailField(max_length=75)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('auth_code', models.CharField(max_length=32, unique=True)),
                ('order_id', models.IntegerField(validators=django.core.validators.MinValueValidator(1), default=1)),
                ('event', models.ForeignKey(to='events.Event')),
                ('user', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemInEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('event', models.ForeignKey(to='events.Event')),
                ('item', models.ForeignKey(to='events.EventItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemInSignup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('value', events.models.MultiInputField(blank=True, max_length=500, null=True)),
                ('item', models.ForeignKey(to='events.EventItem')),
                ('signup', models.ForeignKey(to='events.EventSignup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
