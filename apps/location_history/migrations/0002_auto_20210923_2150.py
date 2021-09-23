# Generated by Django 3.2.6 on 2021-09-23 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0002_auto_20210923_1327'),
        ('location_history', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationhistory',
            name='reporter',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='user.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='locationhistory',
            name='parent_child_pair',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.parentchildpair'),
        ),
    ]