"""View module for handling requests about trips"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import Trip, User

class TripSerializer(serializers.ModelSerializer):
  """JSON serializer for Trips"""
  class Meta:
    model = Trip
    fields = ('id', 'user', 'start', 'end', 'travel_from', 'travel_to', 'budget')
    depth = 2
    
class TripView(ViewSet):
  """Vacationista Trip View"""
  
  def retrieve(self, request, pk):
    """Handle GET single trip"""
    try:
      trip = Trip.objects.get(pk=pk)
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
