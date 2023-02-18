"""View module for handling requests about highlights"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import Highlight

class HighlightSerializer(serializers.ModelSerializer):
  """JSON serializer for Highlights"""
  class Meta:
    model = Highlight
    fields = ('id', 'title', 'content', 'image', 'location', 'thumbnail')
    
class HighlightView(ViewSet):
  """Vacationista Highlight View"""
  
  def retrieve(self, request, pk):
    """Handle GET single highlight"""
    try:
      highlight = Highlight.objects.get(pk=pk)
      serializer = HighlightSerializer(highlight)
      return Response(serializer.data)
    
    except Highlight.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get all highlights"""
    highlights = Highlight.objects.all()
    
    id = request.query_params.get('id', None)
    if id is not None:
      highlights = highlights.filter(id=id)
      
    serializer = HighlightSerializer(highlights, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for highlights

    Returns:
        Response -- Empty body with 204 status code
    """

    highlight = Highlight.objects.get(pk=pk)
    highlight.title = request.data["title"]
    highlight.content = request.data["content"]
    highlight.image = request.data["image"]
    highlight.location = request.data["location"]
    highlight.thumbnail = request.data["thumbnail"]
    
    highlight.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    highlight = Highlight.objects.get(pk=pk)
    highlight.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
