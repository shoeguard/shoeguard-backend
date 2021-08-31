# Generated by Django 3.2.6 on 2021-08-31 01:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('parent_child_pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.parentchildpair')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
