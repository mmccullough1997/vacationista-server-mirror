"""View module for handling requests about Events"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import Leg, Trip, EventType, Event, User

class EventSerializer(serializers.ModelSerializer):
  """JSON serializer for Events"""
  class Meta:
    model = Event
    fields = ('id', 'event_type', 'trip', 'leg', 'description', 'location', 'date', 'image', 'title', 'user')
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
    
    input = request.data["event_type"]
    if input == "true":
      event_type = EventType.objects.get(id=event.event_type.id)
      event.event_type = event_type
    else:
      event.event_type = EventType.objects.get(id=input)
    
    event_trip_input = request.data["trip"]
    if event_trip_input == "true":
      event_trip = Trip.objects.get(id=event.trip.id)
      event.trip = event_trip
    else:
      event.trip = Trip.objects.get(id=event_trip_input)
    
    event_leg_input = request.data["leg"]
    if event_leg_input == "true":
      try:
        event_leg = Leg.objects.get(id=event.leg.id)
      except:
        event_leg = None
      event.leg = event_leg
    else:
      event.leg = Leg.objects.get(id=event_leg_input)
      
    description_input = request.data["description"]
    if description_input == "true":
      event.description = event.description
    else:
      event.description = description_input
      
    location_input = request.data["location"]
    if location_input == "true":
      event.location = event.location
    else:
      event.location = location_input
      
    date_input = request.data["date"]
    if date_input == "true":
      event.date = event.date
    else:
      event.date = date_input
      
    image_input = request.data["image"]
    if image_input == "true":
      event.image = event.image
    else:
      event.image = image_input
      
    title_input = request.data["title"]
    if title_input == "true":
      event.title = event.title
    else:
      event.title = title_input
  
    event.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def create(self, request):
    """Handle POST requests for a single event"""
    
    event_type = EventType.objects.get(id=request.data["event_type"])
    trip = Trip.objects.get(id=request.data["trip"])
    
    try:
      leg = Leg.objects.get(id=request.data["leg"])
    except:
      leg = None
      
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
