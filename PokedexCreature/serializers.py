from rest_framework import serializers
from .models import PokedexCreature


class PokedexCreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokedexCreature
        fields = '__all__'


class PokedexCreatureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokedexCreature
        fields = ('id', 'name', 'type1', 'type2', 'generation', 'legendary')
