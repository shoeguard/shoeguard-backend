# Generated by Django 3.2.6 on 2021-09-25 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_remove_report_parent_child_pair'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
