"""View module for handling requests about articles"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import Article

class ArticleSerializer(serializers.ModelSerializer):
  """JSON serializer for Articles"""
  class Meta:
    model = Article
    fields = ('id', 'date_posted', 'content', 'image', 'thumbnail')
    
class ArticleView(ViewSet):
  """Vacationista Article View"""
  
  def retrieve(self, request, pk):
    """Handle GET single article"""
    try:
      article = Article.objects.get(pk=pk)
      serializer = ArticleSerializer(article)
      return Response(serializer.data)
    
    except Article.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get all articles"""
    articles = Article.objects.all()
    
    id = request.query_params.get('id', None)
    if id is not None:
      articles = articles.filter(id=id)
      
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for articles

    Returns:
        Response -- Empty body with 204 status code
    """

    article = Article.objects.get(pk=pk)
    article.title = request.data["title"]
    article.date_posted = request.data["date_posted"]
    article.content = request.data["content"]
    article.image = request.data["image"]
    article.thumbnail = request.data["thumbnail"]
    
    article.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
