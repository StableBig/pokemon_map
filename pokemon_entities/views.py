import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone
from .models import Pokemon


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision"
    "/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832"
    "&fill=transparent"
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now = timezone.localtime()
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for entity in pokemon.pokemonentity_set.filter(appeared_at__lte=now, disappeared_at__gte=now):
            img_url = DEFAULT_IMAGE_URL
            if pokemon.image and hasattr(pokemon.image, "url"):
                img_url = request.build_absolute_uri(pokemon.image.url)
            add_pokemon(
                folium_map, entity.latitude,
                entity.longitude,
                img_url,
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        img_url = DEFAULT_IMAGE_URL
        if pokemon.image and hasattr(pokemon.image, "url"):
            img_url = request.build_absolute_uri(pokemon.image.url)
        pokemons_on_page.append({
            "pokemon_id": pokemon.id,
            "img_url": img_url,
            "title_ru": pokemon.title,
        })

    return render(request, "mainpage.html", context={
        "map": folium_map._repr_html_(),
        "pokemons": pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound("<h1>Такой покемон не найден</h1>")

    img_url = DEFAULT_IMAGE_URL
    if pokemon.image and hasattr(pokemon.image, "url"):
        img_url = request.build_absolute_uri(pokemon.image.url)

    now = timezone.localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon.pokemonentity_set.filter(appeared_at__lte=now, disappeared_at__gte=now):
        add_pokemon(
            folium_map, entity.latitude,
            entity.longitude,
            img_url,
        )

    pokemon_profile = {
        "pokemon_id": pokemon.id,
        "img_url": img_url,
        "title_ru": pokemon.title,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description,
        "previous_evolution": None,
        "next_evolution": None,
    }

    if pokemon.evolved_from:
        previous_evolution = {
            "pokemon_id": pokemon.evolved_from.id,
            "img_url": request.build_absolute_uri(pokemon.evolved_from.image.url) if pokemon.evolved_from.image else DEFAULT_IMAGE_URL,
            "title_ru": pokemon.evolved_from.title,
        }
        pokemon_profile["previous_evolution"] = previous_evolution

    next_evolution = pokemon.evolutions.first()
    if next_evolution:
        next_evolution_characteristics = {
            "pokemon_id": next_evolution.id,
            "img_url": request.build_absolute_uri(next_evolution.image.url) if next_evolution.image else DEFAULT_IMAGE_URL,
            "title_ru": next_evolution.title,
        }
        pokemon_profile["next_evolution"] = next_evolution_characteristics

    return render(request, "pokemon.html", context={
        "map": folium_map._repr_html_(),
        "pokemon": pokemon_profile,
    })
