import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Pokemon


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision"
    "/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832"
    "&fill=transparent"
)


def get_image_url(pokemon, request):
    if pokemon.image and hasattr(pokemon.image, "url"):
        return request.build_absolute_uri(pokemon.image.url)
    return DEFAULT_IMAGE_URL


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

    pokemons = Pokemon.objects.prefetch_related("entities")

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_on_page = []

    for pokemon in pokemons:
        img_url = get_image_url(pokemon, request)

        active_entities = [entity for entity in pokemon.entities.all() if
                           entity.appeared_at <= now <= entity.disappeared_at]

        for entity in active_entities:
            add_pokemon(
                folium_map, entity.latitude,
                entity.longitude,
                img_url,
            )

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
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    img_url = get_image_url(pokemon, request)

    now = timezone.localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon.entities.filter(appeared_at__lte=now, disappeared_at__gte=now):
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

    next_evolution = pokemon.evolved_pokemon.first()
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
