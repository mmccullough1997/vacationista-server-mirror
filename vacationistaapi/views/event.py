"""View module for handling requests about Events"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import Leg, Trip, EventType, Event

class EventSerializer(serializers.ModelSerializer):
  """JSON serializer for Events"""
  class Meta:
    model = Event
    fields = ('id', 'event_type', 'trip', 'leg', 'description', 'location', 'date', 'image', 'title')
    depth = 2
    
class EventView(ViewSet):
  """Vacationista Event View"""
  
  def retrieve(self, request, pk):
    """Handle GET single event"""
    try:
      event = Event.objects.get(pk=pk)
      serializer = EventSerializer(event)
      return Response(serializer.data)
    
    except Event.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get all events"""
    events = Event.objects.all()
    
    id = request.query_params.get('id', None)
    if id is not None:
      events = events.filter(id=id)
      
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for events

    Returns:
        Response -- Empty body with 204 status code
    """

    event = Event.objects.get(pk=pk)
    event.event_type = EventType.objects.get(id=request.data["event_type"])
    event.trip = Trip.objects.get(id = request.data["trip"])
    event.leg = Leg.objects.get(id = request.data["leg"])
    event.description = request.data["description"]
    event.location = request.data["location"]
    event.date = request.data["date"]
    event.image = request.data["image"]
    event.title = request.data["title"]
    
    event.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def create(self, request):
    """Handle POST requests for a single event"""
    
    event_type = EventType.objects.get(id=request.data["event_type"])
    trip = Trip.objects.get(id=request.data["trip"])
    leg = Leg.objects.get(id=request.data["leg"])
    event = Event.objects.create(
      event_type = event_type,
      trip = trip,
      leg = leg,
      description = request.data["description"],
      location = request.data["location"],
      date = request.data["date"],
      image = request.data["image"],
      title = request.data["title"]
      )
    serializer = EventSerializer(event)
    return Response(serializer.data)
  
  def destroy(self, request, pk):
    event = Event.objects.get(pk=pk)
    event.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
