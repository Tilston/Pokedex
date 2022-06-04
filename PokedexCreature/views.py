import pandas
from django.core.exceptions import ValidationError
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from .models import PokedexCreature
from .serializers import PokedexCreatureSerializer, PokedexCreatureListSerializer


class PokedexCreatureView(mixins.ListModelMixin, mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = PokedexCreature.objects.all()

    def get_serializer_class(self):
        """

        Retourne un serializer ne comprenant pas les stats de combat pour list
        Retourne un serializer contenant tout les champs pour les autres methodes

        """
        if self.action == 'list':
            return PokedexCreatureListSerializer
        return PokedexCreatureSerializer

    def list(self, request, *args, **kwargs):
        """
       Liste tout les creatures du pokedex sans afficher leurs stats de combat
       Possibilite de filtrer par type1, type2, generation, legendary avec query params

        """
        type1 = request.query_params.get("type1")
        type2 = request.query_params.get("type2")
        generation = request.query_params.get("generation")
        legendary = request.query_params.get("legendary")
        if type1:
            self.queryset = self.queryset.filter(type1=type1)
        if type2:
            self.queryset = self.queryset.filter(type2=type2)
        if generation:
            self.queryset = self.queryset.filter(generation=int(generation))
        if legendary == "True":
            self.queryset = self.queryset.filter(legendary=True)
        if legendary == "False":
            self.queryset = self.queryset.filter(legendary=False)
        return super().list(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        """
        Creation de creature dans le pokedex a partir d'un fichier csv contenant tout les champs du modele

        """
        try:
            file = request.data['file']
            reader = pandas.read_csv(file)
            for _, row in reader.iterrows():
                pokedex_creature = PokedexCreature(
                    id=row["#"],
                    name=row["Name"],
                    type1=row["Type 1"],
                    type2=row["Type 2"],
                    total=row["Total"],
                    hp=row["HP"],
                    attack=row["Attack"],
                    defense=row["Defense"],
                    sp_attack=row["Sp. Atk"],
                    sp_defense=row["Sp. Def"],
                    speed=row['Speed'],
                    generation=row["Generation"],
                    legendary=row["Legendary"],
                )
                pokedex_creature.save()
        except KeyError:
            return Response({"file": ["This field is required."]}, status.HTTP_400_BAD_REQUEST)
        except FileNotFoundError:
            return Response({"file": ["A valid file is required"]}, status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({"file": ["A valid file is required"]}, status.HTTP_400_BAD_REQUEST)

        return Response({"status": "success"}, status.HTTP_201_CREATED)

