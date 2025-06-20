# Generated by Django 5.2 on 2025-05-05 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarthome', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Switch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('icon', models.CharField(default='🔘', max_length=10)),
                ('linked_lamps', models.ManyToManyField(limit_choices_to={'device_type': 'light'}, related_name='controlled_by', to='smarthome.device')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='switches', to='smarthome.room')),
            ],
        ),
    ]
