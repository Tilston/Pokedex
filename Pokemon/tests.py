import json
from django.contrib.auth.models import User
from django.test import TestCase
from PokedexCreature.models import PokedexCreature
from .models import Pokemon
from rest_framework.test import APIClient


class RecipeTestCase(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'myemail@test.com', 'admin')
        self.client = APIClient()
        self.client.login(username='admin', password='admin')
        pkmn = PokedexCreature.objects.create(id=911, name="Olivini", type1="Plante", type2="Normal", total=60, hp=10,
                                       attack=10, defense=10, sp_attack=10, sp_defense=10, speed=10, generation=9,
                                       legendary=False)
        Pokemon.objects.create(pokedex_creature_id=pkmn, trainer_id=1,
                               surname="Grosse Olive", level=3, experience=12)

    def test_model(self):
        pkmn = Pokemon.objects.get(surname="Grosse Olive")
        self.assertEqual(pkmn.surname, "Grosse Olive")

    def test_get_pokemon(self):
        response = self.client.get('/api/pokemon/')
        self.assertEqual(json.loads(response.content), [{
            "id": 1,
            "trainer_id": 1,
            "surname": "Grosse Olive",
            "level": 3,
            "experience": 12,
            "pokedex_creature_id": 911
        }])

    def test_create_pokemon_no_pokedex_creature_id(self):
        response = self.client.post('/api/pokemon/', {"trainer_id": 4, "surname": "Lol", "level": 10, "experience": 94}, format='json')
        self.assertEqual(json.loads(response.content), {'pokedex_creature_id': ['This field is required.']})

    def test_create_pokemon_invalid_pokedex_creature_id(self):
        response = self.client.post('/api/pokemon/', {"pokedex_creature_id": 0, "level": 10, "experience": 94},
                                    format='json')
        self.assertEqual(json.loads(response.content), {'pokedex_creature_id': ['Invalid value - PokedexCreature does not exist.']})

    def test_create_pokemon_no_surname_no_trainer_id(self):
        self.client.post('/api/pokemon/', {"pokedex_creature_id": 911, "level": 10, "experience": 94},
                                    format='json')
        pkmn = Pokemon.objects.get(id=2)
        self.assertEqual(pkmn.surname, "Olivini")
        self.assertEqual(pkmn.trainer_id, None)

    def test_give_xp_no_amount(self):
        response = self.client.post('/api/pokemon/1/give-xp/')
        print(response.content)
        self.assertEqual(json.loads(response.content), {'amount': ['This field is required.']})

    def test_give_xp_bad_id(self):
        response = self.client.post('/api/pokemon/342/give-xp/', {"amount": 154}, format='json')
        print(response.content)
        self.assertEqual(json.loads(response.content), {'{id}': ['Invalid value for id - PokedexCreature does not exist.']})

    def test_give_xp_string(self):
        response = self.client.post('/api/pokemon/1/give-xp/', {"amount": "fail"}, format='json')
        print(response.content)
        self.assertEqual(json.loads(response.content), {'amount': ['Positive integer is required']})

    def test_give_xp_negatif(self):
        response = self.client.post('/api/pokemon/1/give-xp/', {"amount": -154}, format='json')
        print(response.content)
        self.assertEqual(json.loads(response.content), {'amount': ['Positive integer is required']})

    def test_give_xp(self):
        response = self.client.post('/api/pokemon/1/give-xp/', {"amount": 154}, format='json')
        print(response.content)
        self.assertEqual(json.loads(response.content), {
            "id": 1,
            "trainer_id": 1,
            "surname": "Grosse Olive",
            "level": 4,
            "experience": 66,
            "pokedex_creature_id": 911
        })


