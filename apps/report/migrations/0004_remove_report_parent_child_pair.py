# Generated by Django 3.2.6 on 2021-09-23 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_auto_20210923_2052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='parent_child_pair',
        ),
    ]