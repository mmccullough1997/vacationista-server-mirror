"""View module for handling requests about legs"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import Leg, User

class LegSerializer(serializers.ModelSerializer):
  """JSON serializer for Legs"""
  class Meta:
    model = Leg
    fields = ('id', 'user', 'start', 'end', 'location', 'budget')
    depth = 1
    
class LegView(ViewSet):
  """Vacationista Leg View"""
  
  def retrieve(self, request, pk):
    """Handle GET single leg"""
    try:
      leg = Leg.objects.get(pk=pk)
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
      
    serializer = LegSerializer(legs, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for legs

    Returns:
        Response -- Empty body with 204 status code
    """

    leg = Leg.objects.get(pk=pk)
    leg.user = User.objects.get(id=request.data["user"])
    leg.start = request.data["start"]
    leg.end = request.data["end"]
    leg.location = request.data["location"]
    leg.budget = request.data["budget"]
    
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
