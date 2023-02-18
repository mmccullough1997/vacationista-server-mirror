"""View module for handling requests about event types"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import EventType

class EventTypeSerializer(serializers.ModelSerializer):
  """JSON serializer for Event types"""
  class Meta:
    model = EventType
    fields = ('id', 'label')
    
class EventTypeView(ViewSet):
  """Vacationista Event Type View"""
  
  def retrieve(self, request, pk):
    """Handle GET single event type"""
    try:
      event_type = EventType.objects.get(pk=pk)
      serializer = EventTypeSerializer(event_type)
      return Response(serializer.data)
    
    except EventType.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get all event_types"""
    event_types = EventType.objects.all()
    
    id = request.query_params.get('id', None)
    if id is not None:
      event_types = event_types.filter(id=id)
      
    serializer = EventTypeSerializer(event_types, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for event types

    Returns:
        Response -- Empty body with 204 status code
    """

    event_type = EventType.objects.get(pk=pk)
    event_type.label = request.data["label"]
    
    event_type.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    event_type = EventType.objects.get(pk=pk)
    event_type.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
