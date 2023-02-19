"""View module for handling requests about transportation types"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import TransportationType

class TransportationTypeSerializer(serializers.ModelSerializer):
  """JSON serializer for transportation types"""
  class Meta:
    model = TransportationType
    fields = ('id', 'label')
    
class TransportationTypeView(ViewSet):
  """Vacationista transportation Type View"""
  
  def retrieve(self, request, pk):
    """Handle GET single transportation type"""
    try:
      transportation_type = TransportationType.objects.get(pk=pk)
      serializer = TransportationTypeSerializer(transportation_type)
      return Response(serializer.data)
    
    except TransportationType.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get all transportation_types"""
    transportation_types = TransportationType.objects.all()
    
    id = request.query_params.get('id', None)
    if id is not None:
      transportation_types = transportation_types.filter(id=id)
      
    serializer = TransportationTypeSerializer(transportation_types, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for transportation types

    Returns:
        Response -- Empty body with 204 status code
    """

    transportation_type = TransportationType.objects.get(pk=pk)
    transportation_type.label = request.data["label"]
    
    transportation_type.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    transportation_type = TransportationType.objects.get(pk=pk)
    transportation_type.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
