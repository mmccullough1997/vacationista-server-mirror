"""View module for handling requests about trips"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import Trip, User, Event, Leg, TripLeg, Expense, Transportation
from datetime import date, datetime
from .event import EventSerializer
from .trip_leg import TripLegSerializer
from .leg import LegSerializer

# bradbutter414
# jessfirestorm669

class TripSerializer(serializers.ModelSerializer):
  """JSON serializer for Trips"""
  class Meta:
    model = Trip
    fields = ('id', 'user', 'start', 'end', 'travel_from', 'travel_to', 'budget', 'duration', 'events', 'legs', 'expenses', 'expense_total', 'transportations', 'transportation_total', 'total')
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
      
      expenses = Expense.objects.filter(trip=trip)
      trip_expenses= []
      for expense in expenses:
        theexpense = Expense.objects.get(id=expense.id)
        trip_expenses.append(ExpensesOnTripSerializer(theexpense).data)
      trip.expenses = trip_expenses
      
      expense_total = 0
      for expense in expenses:
        expense_total += expense.amount
        
      trip.expense_total = expense_total
      
      transportations = Transportation.objects.filter(trip=trip)
      trip_transportations= []
      for transportation in transportations:
        thetransportations = Transportation.objects.get(id=transportation.id)
        trip_transportations.append(TransportationsOnTripSerializer(thetransportations).data)
      trip.transportations = trip_transportations
      
      transportation_total = 0
      for transportation in transportations:
        transportation_total += transportation.amount
        
      trip.transportation_total = transportation_total
      
      trip.total = expense_total + transportation_total
  
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
    if user is not None and upcoming == 'true':
      user_trips = trips.filter(user=user)
      
      for trip in user_trips:
        today = date.today().strftime('%Y-%m-%d')
        trips = [trip for trip in trips if today < datetime.strftime(trip.start, '%Y-%m-%d')]
        
    elif user is not None and upcoming == 'false':
      user_trips = trips.filter(user=user)
      
      for trip in user_trips:
        today = date.today().strftime('%Y-%m-%d')
        trips = [trip for trip in trips if today > datetime.strftime(trip.start, '%Y-%m-%d')]

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
    
    trip_user_id = request.data['user']
    if trip_user_id == "true":
      trip_user = User.objects.get(id=trip.user.id)
      trip.user = trip_user
    else:
      trip.user = trip_user_id
    
    start_input = request.data["start"]
    if start_input == "true":
      trip.start = trip.start
    else:
      trip.start = start_input
    
    end_input = request.data["end"]
    if end_input == "true":
      trip.end = trip.end
    else:
      trip.end = end_input

    travel_from_input = request.data["travel_from"]
    if travel_from_input == "true":
      trip.travel_from = trip.travel_from
    else:
      trip.travel_from = travel_from_input
      
    travel_to_input = request.data["travel_to"]
    if travel_to_input == "true":
      trip.travel_to = trip.travel_to
    else:
      trip.travel_to = travel_to_input
      
    budget_input = request.data["budget"]
    if budget_input == "true":
      trip.budget = trip.budget
    else:
      trip.budget = budget_input
    
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

class ExpensesOnTripSerializer(serializers.ModelSerializer):
  """JSON serializer for expenses on trips"""
  class Meta:
    model = Expense
    fields = ('id', 'expense_type', 'leg', 'amount', 'comment', 'title')
    depth = 1

class TransportationsOnTripSerializer(serializers.ModelSerializer):
  """JSON serializer for transportations on trips"""
  class Meta:
    model = Transportation
    fields = ('id', 'transportation_type', 'leg', 'travel_from', 'travel_to',  'amount', 'comment', 'round_trip')
    depth = 1
