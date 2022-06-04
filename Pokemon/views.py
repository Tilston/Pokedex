from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from PokedexCreature.models import PokedexCreature
from django.core.exceptions import ObjectDoesNotExist
from .models import Pokemon
from .serializers import PokemonSerializer


class PokemonView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):

    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

    def create(self, request, *args, **kwargs):
        """

        Permet la creation d'un Pokemon
        Si le champs surname n'est pas present il est remplace par le champs name de la creature
        correspondante a pokedex_creature_id

        """
        if not request.data.get("surname"):
            try:
                pkmn = PokedexCreature.objects.get(id=request.data["pokedex_creature_id"])
                request.data["surname"] = pkmn.name
            except KeyError:
                return Response({"pokedex_creature_id": ["This field is required."]}, status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response({"pokedex_creature_id": ["Invalid value - PokedexCreature does not exist."]}, status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["post"],
        url_path="give-xp",
    )
    def give_xp(self, request, pk=None):
        """

        Permet de donner de l'xp à un Pokemon
        Doit contenir un champs amount avec une valeur positive

        """
        try:
            data = request.data
            xp = int(data["amount"])
            pkmn = self.get_queryset().get(id=pk)
            if xp < 0:
                return Response({"amount": ["Positive integer is required"]}, status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"amount": ["This field is required."]}, status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"amount": ["Positive integer is required"]}, status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"{id}": ["Invalid value for id - PokedexCreature does not exist."]}, status.HTTP_400_BAD_REQUEST)

        pkmn.add_xp(xp)
        serializer = self.get_serializer(pkmn)
        return Response(serializer.data)

