"""View module for handling requests about expense types"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import ExpenseType

class ExpenseTypeSerializer(serializers.ModelSerializer):
  """JSON serializer for expense types"""
  class Meta:
    model = ExpenseType
    fields = ('id', 'label')
    
class ExpenseTypeView(ViewSet):
  """Vacationista expense Type View"""
  
  def retrieve(self, request, pk):
    """Handle GET single expense type"""
    try:
      expense_type = ExpenseType.objects.get(pk=pk)
      serializer = ExpenseTypeSerializer(expense_type)
      return Response(serializer.data)
    
    except ExpenseType.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get all expense_types"""
    expense_types = ExpenseType.objects.all()
    
    id = request.query_params.get('id', None)
    if id is not None:
      expense_types = expense_types.filter(id=id)
      
    serializer = ExpenseTypeSerializer(expense_types, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for expense types

    Returns:
        Response -- Empty body with 204 status code
    """

    expense_type = ExpenseType.objects.get(pk=pk)
    expense_type.label = request.data["label"]
    
    expense_type.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    expense_type = ExpenseType.objects.get(pk=pk)
    expense_type.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
