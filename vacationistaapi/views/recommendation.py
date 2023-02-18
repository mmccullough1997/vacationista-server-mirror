"""View module for handling requests about recommendations"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import Recommendation

class RecommendationSerializer(serializers.ModelSerializer):
  """JSON serializer for Recommendations"""
  class Meta:
    model = Recommendation
    fields = ('id', 'title', 'category', 'description', 'location', 'rating', "image")
    
class RecommendationView(ViewSet):
  """Vacationista Recommendation View"""
  
  def retrieve(self, request, pk):
    """Handle GET single recommendation"""
    try:
      recommendation = Recommendation.objects.get(pk=pk)
      serializer = RecommendationSerializer(recommendation)
      return Response(serializer.data)
    
    except Recommendation.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get all recommendations"""
    recommendations = Recommendation.objects.all()
    
    id = request.query_params.get('id', None)
    if id is not None:
      recommendations = recommendations.filter(id=id)
      
    serializer = RecommendationSerializer(recommendations, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for recommendations

    Returns:
        Response -- Empty body with 204 status code
    """

    recommendation = Recommendation.objects.get(pk=pk)
    recommendation.title = request.data["title"]
    recommendation.category = request.data["category"]
    recommendation.description = request.data["description"]
    recommendation.location = request.data["location"]
    recommendation.rating = request.data["rating"]
    recommendation.image = request.data["image"]
    
    recommendation.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    recommendation = Recommendation.objects.get(pk=pk)
    recommendation.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
