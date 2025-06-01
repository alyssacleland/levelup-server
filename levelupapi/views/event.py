"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer, EventGamer
from rest_framework.decorators import action


class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()

        # filter events by game if provided
        game = request.query_params.get('game', None)
        if game is not None:
            events = events.filter(game_id=game)

        # wk 9: to set the joined property, we need to get the uid from the request headers
        # and then get the Gamer object associated with that uid
        # pass uid in the header of the request
        uid = request.META['HTTP_AUTHORIZATION']
        gamer = Gamer.objects.get(uid=uid)

        for event in events:
            # Check to see if there is a row in the Event Games table that has the passed in gamer and event.
            # check the length of how many rows there are that match the gamer and event. if there is at least one row, then it will return True, otherwise it will return False.
            # this will set the joined property to True or False based on whether the gamer is signed up for the event
            event.joined = len(EventGamer.objects.filter(
                gamer=gamer, event=event)) > 0

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized event instance
        """

        # retrieve game object by primary key from the request data. get the game obj where the pk matches 'game' in the request data (in client side).
        # retrieve organizer gamer object by uid from the request data. get the gamer obj where the uid's value matches 'organizer''s value in the request data (in client side)
        game = Game.objects.get(pk=request.data["game"])
        organizer = Gamer.objects.get(uid=request.data["organizer"])

        event = Event.objects.create(
            game=game,
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            organizer=organizer,
        )
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """Handle DELETE requests for an event

        Returns:
            Response -- 204 No Content
        """
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        event.game = Game.objects.get(pk=request.data["game"])
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.organizer = Gamer.objects.get(pk=request.data["organizer"])

        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        uid = request.META['HTTP_AUTHORIZATION']

        gamer = Gamer.objects.get(uid=uid)
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.create(
            gamer=gamer,
            event=event
        )
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    # Using the action decorator turns a method into a new route. In this case, the action will accept POST methods and because detail=True the url will include the pk. Since we need to know which event the user wants to sign up for we’ll need to have the pk. The route is named after the function. So to call this method the url would be http://localhost:8000/events/2/signup

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""

        uid = request.META['HTTP_AUTHORIZATION']
        gamer = Gamer.objects.get(uid=uid)
        event = Event.objects.get(pk=pk)

        try:
            event_gamer = EventGamer.objects.get(gamer=gamer, event=event)
            event_gamer.delete()
        except EventGamer.DoesNotExist:
            pass

        return Response(None, status=status.HTTP_204_NO_CONTENT)

        # Write a new method named leave
        # It should have the action decorator
        # It should accept DELETE requests
        # It should be a detail route
        # Get the gamer and the event objects
        # Use the gamer and event objects to find the event_gamer object.
        # Use the remove method on the event_gamer object to delete the gamer from the join table (jk use delete method since join table, not a many to many field)
        # Return a 204 Response
        # Test in Postman by sending a DELETE request to http://localhost:8000/events/1/leave
        # Pass the user_id in the body of the request


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date',
                  'time', 'organizer', 'joined')
        depth = 2
