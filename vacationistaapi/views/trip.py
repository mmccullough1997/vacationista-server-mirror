"""View module for handling requests about trips"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import Trip, User, Event, Leg, TripLeg
from datetime import date, datetime
from .event import EventSerializer
from .trip_leg import TripLegSerializer
from .leg import LegSerializer

class TripSerializer(serializers.ModelSerializer):
  """JSON serializer for Trips"""
  class Meta:
    model = Trip
    fields = ('id', 'user', 'start', 'end', 'travel_from', 'travel_to', 'budget', 'duration', 'events', 'legs')
    depth = 1
    
class NewLegSerializer(serializers.ModelSerializer):
  """JSON serializer for legs"""
  class Meta:
    model = Leg
    fields = ('id', 'user', 'start', 'end', 'location', 'budget', 'duration', 'events')
    
class NewEventSerializer(serializers.ModelSerializer):
  """JSON serializer for events"""
  class Meta:
    model = Event
    fields = ('id', 'event_type','description', 'location', 'date', 'image', 'title')
    depth = 1
    
class TripView(ViewSet):
  """Vacationista Trip View"""
  
  def retrieve(self, request, pk):
    """Handle GET single trip"""
    try:
      trip = Trip.objects.get(pk=pk)
      
      trip.duration = (trip.end - trip.start).days
      
      user = request.query_params.get('user', None)
      if user is not None:
        trip = Trip.objects.get(pk=pk, user=user)
      else:
        trip = Trip.objects.get(pk=pk)
        
      events = Event.objects.filter(trip=trip)
      trip_events = []
      for event in events:
        if event.leg is not None:
          trip_events = []
        else:
          theevent = Event.objects.get(id=event.id)
          theeventserialized = NewEventSerializer(theevent)
          trip_events.append(theeventserialized.data)
        
      trip.events = trip_events
      
      trip_legs = TripLeg.objects.filter(trip=trip)
      legs = []
      for tripleg in trip_legs:
        leg = Leg.objects.get(id=tripleg.leg.id)
        
        events = Event.objects.filter(leg=leg)
        leg_events = []
        for event in events:
          theevent = Event.objects.get(id=event.id)
          theeventserialized = NewEventSerializer(theevent)
          leg_events.append(theeventserialized.data)
        
        leg.events = leg_events
        leg.duration = (leg.end - leg.start).days
        thelegserialized = NewLegSerializer(leg)
        legs.append(thelegserialized.data)
        
      trip.legs = legs
  
      serializer = TripSerializer(trip)
      return Response(serializer.data)
    
    except Trip.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    
  def list(self, request):
    """Handle GET requests to get all trips"""
    trips = Trip.objects.all()
    
    
    id = request.query_params.get('id', None)
    if id is not None:
      trips = trips.filter(id=id)
      
    user = request.query_params.get('user', None)
    if user is not None:
      trips = trips.filter(user=user)
      
    upcoming = request.query_params.get('upcoming', None)
    if user is not None and upcoming is not None:
      user_trips = trips.filter(user=user)
      
      for trip in user_trips:
        today = date.today().strftime('%Y-%m-%d')
        trips = [trip for trip in trips if today < datetime.strftime(trip.start, '%Y-%m-%d')]

    for trip in trips:
      try:
        trip.duration = (trip.end - trip.start).days
      except:
        pass
      
    serializer = TripSerializer(trips, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for trips

    Returns:
        Response -- Empty body with 204 status code
    """

    trip = Trip.objects.get(pk=pk)
    trip.user = User.objects.get(id=request.data["user"])
    trip.start = request.data["start"]
    trip.end = request.data["end"]
    trip.travel_from = request.data["travel_from"]
    trip.travel_to = request.data["travel_to"]
    trip.budget = request.data["budget"]
    
    trip.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def create(self, request):
    """Handle POST requests for a single trip"""
    
    user = User.objects.get(id=request.data["user"])
    trip = Trip.objects.create(
      user = user,
      start = request.data["start"],
      end = request.data["end"],
      travel_from = request.data["travel_from"],
      travel_to = request.data["travel_to"],
      budget = request.data["budget"]
      )
    serializer = TripSerializer(trip)
    return Response(serializer.data)
  
  def destroy(self, request, pk):
    trip = Trip.objects.get(pk=pk)
    trip.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
class LegsOnTripSerializer(serializers.ModelSerializer):
  """JSON serializer for legs on trips"""
  class Meta:
    model = TripLeg
    fields = ('id', 'leg')
    depth = 2
