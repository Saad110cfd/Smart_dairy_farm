# Generated by Django 5.0.2 on 2024-03-24 19:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dairymanagementsystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeatObservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observation_date', models.DateField()),
                ('notes', models.TextField(blank=True)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='heat_observations', to='dairymanagementsystem.animal')),
            ],
        ),
        migrations.CreateModel(
            name='Pregnancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('pregnancy_scan_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pregnancies', to='dairymanagementsystem.animal')),
            ],
        ),
    ]
