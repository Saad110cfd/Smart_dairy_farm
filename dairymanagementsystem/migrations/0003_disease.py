# Generated by Django 5.0.2 on 2024-03-24 19:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dairymanagementsystem', '0002_heatobservation_pregnancy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('occurrence_date', models.DateField()),
                ('is_recovered', models.BooleanField(default=False)),
                ('recovered_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('symptoms', models.TextField(blank=True)),
                ('treatment', models.TextField(blank=True)),
                ('cows', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diseases', to='dairymanagementsystem.animal')),
            ],
            options={
                'verbose_name': 'Disease 💊',
                'verbose_name_plural': 'Diseases 💊',
            },
        ),
    ]