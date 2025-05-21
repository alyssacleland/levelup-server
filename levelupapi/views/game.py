"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, GameType, Gamer


class GameView(ViewSet):
    """Level up game view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()

      # Filter by game type if provided
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        # retrieve gamer object from the database. To make sure the user we're trying to add and the new game actually exist in the database.this is being sourced from UserId in the body of the request.
        gamer = Gamer.objects.get(uid=request.data["userId"])
        # retrieve game type object from the database. this is being sourced from the body of the request. this way passes an actual model instance of GameType. it would be relational either way though bc the game_type field in the Game model is a foreign key to the GameType model.
        game_type = GameType.objects.get(pk=request.data["gameType"])

        # using ORM create method
        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["numberOfPlayers"],
            skill_level=request.data["skillLevel"],
            game_type=game_type,
            gamer=gamer,
        )
        # after above, game variavle is now the new game instance, including id.

        # serialize obj and return to client
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:
        model = Game
        fields = ('id', 'game_type', 'maker', 'gamer',
                  'number_of_players', 'skill_level', 'title')
        depth = 1
