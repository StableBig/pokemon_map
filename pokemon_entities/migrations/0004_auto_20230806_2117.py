# Generated by Django 3.1.14 on 2023-08-06 21:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0003_pokemonentity'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonentity',
            name='appeared_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='pokemonentity',
            name='disappeared_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
