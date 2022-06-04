from django.contrib import admin
from .models import PokedexCreature


@admin.register(PokedexCreature)
class PokedexCreatureAdmin(admin.ModelAdmin):
    pass
