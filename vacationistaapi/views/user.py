"""View module for handling requests about users"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import User

class UserSerializer(serializers.ModelSerializer):
  """JSON serializer for Users"""
  class Meta:
    model = User
    fields = ('id', 'uid', 'first_name', 'last_name', 'date_registered', 'username', 'bio', 'image')
    
class UserView(ViewSet):
  """Vacationista User View"""
  
  def retrieve(self, request, pk):
    """Handle GET single user"""
    try:
      user = User.objects.get(pk=pk)
      serializer = UserSerializer(user)
      return Response(serializer.data)
    
    except User.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get all users"""
    users = User.objects.all()
    
    id = request.query_params.get('id', None)
    if id is not None:
      users = users.filter(id=id)
      
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for users

    Returns:
        Response -- Empty body with 204 status code
    """

    user = User.objects.get(pk=pk)
    user.uid = request.data["uid"]
    user.first_name = request.data["first_name"]
    user.last_name = request.data["last_name"]
    user.date_registered = request.data["date_registered"]
    user.username = request.data["username"]
    user.bio = request.data["bio"]
    user.image = request.data["image"]
    
    user.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
