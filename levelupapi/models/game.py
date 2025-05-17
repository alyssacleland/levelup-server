from django.db import models
from models import Gamer, GameType


class Game(models.Model):

    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    number_of_players = models.PositiveIntegerField()
    skill_level = models.IntegerField()
