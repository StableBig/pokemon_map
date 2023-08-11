# Generated by Django 3.1.14 on 2023-08-11 20:54

from django.db import migrations, models


def replace_null_with_empty_string(apps, schema_editor):
    Pokemon = apps.get_model('pokemon_entities', 'Pokemon')
    for pokemon in Pokemon.objects.filter(title_en=None):
        pokemon.title_en = ''
        pokemon.save()
    for pokemon in Pokemon.objects.filter(title_jp=None):
        pokemon.title_jp = ''
        pokemon.save()


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0009_auto_20230807_1607'),
    ]

    operations = [
        migrations.RunPython(replace_null_with_empty_string, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='pokemon',
            name='title_en',
            field=models.CharField(blank=True, max_length=200, verbose_name='Имя на английском'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='title_jp',
            field=models.CharField(blank=True, max_length=200, verbose_name='Имя на японском'),
        ),
    ]