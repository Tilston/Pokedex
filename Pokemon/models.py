from django.db import models
from PokedexCreature.models import PokedexCreature


class Pokemon(models.Model):
    id = models.AutoField(primary_key=True)
    pokedex_creature_id = models.ForeignKey(PokedexCreature, on_delete=models.CASCADE)
    trainer_id = models.IntegerField(null=True)
    surname = models.CharField(max_length=255)
    level = models.IntegerField()
    experience = models.IntegerField()

    def __str__(self):
        return self.surname

    def add_xp(self, xp):
        """

        Met a jour l'experience et le level du pokemon en fonction de l'xp recu

        """
        self.experience += xp
        if self.experience > 100:
            self.level += self.experience // 100
            self.experience %= 100
        self.save()
