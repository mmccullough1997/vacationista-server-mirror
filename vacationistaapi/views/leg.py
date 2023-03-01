"""View module for handling requests about legs"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import Leg, User, Event, Trip, TripLeg
from .event import EventSerializer

class LegSerializer(serializers.ModelSerializer):
  """JSON serializer for Legs"""
  class Meta:
    model = Leg
    fields = ('id', 'user', 'start', 'end', 'location', 'budget', 'events', 'trip')
    depth = 1
    
class LegView(ViewSet):
  """Vacationista Leg View"""
  
  def retrieve(self, request, pk):
    """Handle GET single leg"""
    try:
      leg = Leg.objects.get(pk=pk)
      
      user = request.query_params.get('user', None)
      if user is not None:
        leg = Leg.objects.get(pk=pk, user=user)
      else:
        leg = Leg.objects.get(pk=pk)
      
      events = Event.objects.filter(leg=leg)
      leg_events = []
      for event in events:
        theevent = Event.objects.get(id=event.id)
        theeventserialized = EventSerializer(theevent)
        leg_events.append(theeventserialized.data)
        
      leg.events = leg_events
      
      leg_trip = TripLeg.objects.get(leg=leg)
      leg.trip = leg_trip.trip.id

      serializer = LegSerializer(leg)
      return Response(serializer.data)
    
    except Leg.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get all legs"""
    legs = Leg.objects.all()
    
    id = request.query_params.get('id', None)
    if id is not None:
      legs = legs.filter(id=id)
      
    for leg in legs:
      events = Event.objects.filter(leg=leg)
      leg_events = []
      for event in events:
        theevent = Event.objects.get(id=event.id)
        theeventserialized = EventSerializer(theevent)
        leg_events.append(theeventserialized.data)
        
      leg.events = leg_events
      
    serializer = LegSerializer(legs, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for legs

    Returns:
        Response -- Empty body with 204 status code
    """

    leg = Leg.objects.get(pk=pk)
    
    leg_user_id = request.data['user']
    if leg_user_id == "true":
      leg_user = User.objects.get(id=leg.user.id)
      leg.user = leg_user
    else:
      leg.user = leg_user_id
    
    start_input = request.data["start"]
    if start_input == "true":
      leg.start = leg.start
    else:
      leg.start = start_input
    
    end_input = request.data["end"]
    if end_input == "true":
      leg.end = leg.end
    else:
      leg.end = end_input

    location_input = request.data["location"]
    if location_input == "true":
      leg.location = leg.location
    else:
      leg.location = location_input
      
    budget_input = request.data["budget"]
    if budget_input == "true":
      leg.budget = leg.budget
    else:
      leg.budget = budget_input
    
    leg.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def create(self, request):
    """Handle POST requests for a single leg"""
    
    user = User.objects.get(id=request.data["user"])
    leg = Leg.objects.create(
      user = user,
      start = request.data["start"],
      end = request.data["end"],
      location = request.data["location"],
      budget = request.data["budget"]
      )
    serializer = LegSerializer(leg)
    return Response(serializer.data)
  
  def destroy(self, request, pk):
    leg = Leg.objects.get(pk=pk)
    leg.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
