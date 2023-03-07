"""View module for handling requests about users"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import User, Event, Trip
from .event import EventSerializer

class UserSerializer(serializers.ModelSerializer):
  """JSON serializer for Users"""
  class Meta:
    model = User
    fields = ('id', 'uid', 'first_name', 'last_name', 'date_registered', 'username', 'bio', 'image', 'events')
    
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
    
    
    uid_input = request.data["uid"]
    if uid_input == "true":
      user.uid = user.uid
    else:
      user.uid = uid_input
      
    first_name_input = request.data["first_name"]
    if first_name_input == "true":
      user.first_name = user.first_name
    else:
      user.first_name = first_name_input
      
    last_name_input = request.data["last_name"]
    if last_name_input == "true":
      user.last_name = user.last_name
    else:
      user.last_name = last_name_input
      
    date_registered_input = request.data["date_registered"]
    if date_registered_input == "true":
      user.date_registered = user.date_registered
    else:
      user.date_registered = date_registered_input
      
    username_input = request.data["username"]
    if username_input == "true":
      user.username = user.username
    else:
      user.username = username_input
      
    bio_input = request.data["bio"]
    if bio_input == "true":
      user.bio = user.bio
    else:
      user.bio = bio_input
      
    image_input = request.data["image"]
    if image_input == "true":
      user.image = user.image
    else:
      user.image = image_input
    
    
    user.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)


class NewEventSerializer(serializers.ModelSerializer):
  """JSON serializer for events"""
  class Meta:
    model = Event
    fields = ('id', 'event_type')
    depth = 1
