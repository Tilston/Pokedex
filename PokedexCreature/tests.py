import json
from django.contrib.auth.models import User
from django.test import TestCase
from .models import PokedexCreature
from rest_framework.test import APIClient


class RecipeTestCase(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'myemail@test.com', 'admin')
        self.client = APIClient()
        self.client.login(username='admin', password='admin')
        PokedexCreature.objects.create(id=911, name="Olivini", type1="Plante", type2="Normal", total=60, hp=10,
                                       attack=10, defense=10, sp_attack=10, sp_defense=10, speed=10, generation=9,
                                       legendary=False)

    def test_model(self):
        pkmn = PokedexCreature.objects.get(name="Olivini")
        self.assertEqual(pkmn.name, "Olivini")

    def test_get_pokedex(self):
        response = self.client.get('/api/pokedex/')
        self.assertEqual(json.loads(response.content), [{'id': 911, 'name': 'Olivini', 'type1': 'Plante',
                                                         'type2': 'Normal', 'generation': 9, 'legendary': False}])

    def test_get_pokedex_id(self):
        response = self.client.get('/api/pokedex/911/')
        print(response.content)
        self.assertEqual(json.loads(response.content), {'id': 911, 'name': 'Olivini', 'type1': 'Plante', 'type2':
            'Normal', 'total': 60, 'hp': 10, 'attack': 10, 'defense': 10, 'sp_attack': 10, 'sp_defense': 10,
                                                         'speed': 10, 'generation': 9, 'legendary': False})
