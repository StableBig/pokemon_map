from django.db import models
from django.utils import timezone


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Имя покемона")
    image = models.ImageField(upload_to="images/", null=True, blank=True, verbose_name="Изображение")
    description = models.TextField(blank=True, verbose_name="Описание")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Имя на английском")
    title_jp = models.CharField(max_length=200, blank=True, verbose_name="Имя на японском")
    evolved_from = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evolves_to",
        verbose_name="В кого эволюционирует"
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон", related_name="entities")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(verbose_name="Время появления на карте")
    disappeared_at = models.DateTimeField(verbose_name="Время исчезновения с карты")

    level = models.IntegerField(verbose_name="Уровень")
    health = models.IntegerField(verbose_name="Здоровье")
    attack = models.IntegerField(verbose_name="Атака")
    defense = models.IntegerField(verbose_name="Защита")
    stamina = models.IntegerField(verbose_name="Выносливость")

    def __str__(self):
        return f"{self.pokemon.title} at {self.latitude}, {self.longitude}"
