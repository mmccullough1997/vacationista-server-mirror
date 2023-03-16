"""View module for handling requests about Transportations"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import Leg, Trip, TransportationType, Transportation

class TransportationSerializer(serializers.ModelSerializer):
  """JSON serializer for Transportations"""
  class Meta:
    model = Transportation
    fields = ('id', 'transportation_type', 'trip', 'leg', 'travel_from', 'travel_to', 'amount', 'comment', 'round_trip')
    depth = 2
    
class TransportationView(ViewSet):
  """Vacationista Transportation View"""
  
  def retrieve(self, request, pk):
    """Handle GET single transportation"""
    try:
      transportation = Transportation.objects.get(pk=pk)
      serializer = TransportationSerializer(transportation)
      return Response(serializer.data)
    
    except Transportation.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get all transportations"""
    transportations = Transportation.objects.all()
    
    id = request.query_params.get('id', None)
    if id is not None:
      transportations = transportations.filter(id=id)
      
    trip = request.query_params.get('trip', None)
    if trip is not None:
      transportations = transportations.filter(trip=trip)
      
    leg = request.query_params.get('leg', None)
    if leg is not None:
      transportations = transportations.filter(leg=leg)
      
    if trip and leg is not None:
      transportations = transportations.filter(trip=trip, leg=leg)
      
    serializer = TransportationSerializer(transportations, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for transportations

    Returns:
        Response -- Empty body with 204 status code
    """

    transportation = Transportation.objects.get(pk=pk)
    transportation.transportation_type = TransportationType.objects.get(id=request.data["transportation_type"])
    transportation.trip = Trip.objects.get(id = request.data["trip"])
    
    try:
      transportation.leg = Leg.objects.get(id = request.data["leg"])
    except:
      transportation.leg = None
  
    transportation.travel_from = request.data["travel_from"]
    transportation.travel_to = request.data["travel_to"]
    transportation.amount = request.data["amount"]
    transportation.comment = request.data["comment"]
    transportation.round_trip = request.data["round_trip"]
    
    transportation.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def create(self, request):
    """Handle POST requests for a single transportation"""
    
    transportation_type = TransportationType.objects.get(id=request.data["transportation_type"])
    trip = Trip.objects.get(id=request.data["trip"])
    
    try:
      leg = Leg.objects.get(id=request.data["leg"])
    except:
      leg = None
      
    transportation = Transportation.objects.create(
      transportation_type = transportation_type,
      trip = trip,
      leg = leg,
      travel_from = request.data["travel_from"],
      travel_to = request.data["travel_to"],
      amount = request.data["amount"],
      comment = request.data["comment"],
      round_trip = request.data["round_trip"]
      )
    serializer = TransportationSerializer(transportation)
    return Response(serializer.data)
  
  def destroy(self, request, pk):
    transportation = Transportation.objects.get(pk=pk)
    transportation.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
