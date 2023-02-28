"""View module for handling requests about trip legs"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import Trip, Leg, TripLeg, Event
from .event import EventSerializer
from .leg import LegSerializer

class TripLegSerializer(serializers.ModelSerializer):
  """JSON serializer for TripLegs"""
  class Meta:
    model = TripLeg
    fields = ('id', 'trip', 'leg')
    depth = 2
    
class TripLegView(ViewSet):
  """Vacationista TripLeg View"""
  
  def retrieve(self, request, pk):
    """Handle GET single tripleg"""
    try:
      trip_leg = TripLeg.objects.get(pk=pk)
      
      serializer = TripLegSerializer(trip_leg)
      return Response(serializer.data)
    
    except TripLeg.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get all trip legs"""
    trip_legs = TripLeg.objects.all()
    
    id = request.query_params.get('id', None)
    if id is not None:
      trip_legs = trip_legs.filter(id=id)
      
    serializer = TripLegSerializer(trip_legs, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for trip legs

    Returns:
        Response -- Empty body with 204 status code
    """

    trip_leg = TripLeg.objects.get(pk=pk)
    trip_leg.trip = Trip.objects.get(id=request.data["trip"])
    trip_leg.leg = Leg.objects.get(id = request.data["leg"])
    
    trip_leg.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def create(self, request):
    """Handle POST requests for a single trip leg"""
    
    trip = Trip.objects.get(id = request.data["trip"])
    leg = Leg.objects.get(id = request.data["leg"])
    trip_leg = TripLeg.objects.create(
      trip = trip,
      leg = leg,
      )
    serializer = TripLegSerializer(trip_leg)
    return Response(serializer.data)
  
  def destroy(self, request, pk):
    trip_leg = TripLeg.objects.get(pk=pk)
    trip_leg.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)

class LegsOnTripLegsSerializer(serializers.ModelSerializer):
  """JSON serializer for legs on trip legs"""
  class Meta:
    model = Leg
    fields = ('id', 'user', 'start', 'end', 'location', 'budget', 'events')
    depth = 1
