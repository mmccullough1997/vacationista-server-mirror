"""View module for handling requests about Expenses"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vacationistaapi.models import Leg, Trip, ExpenseType, Expense

class ExpenseSerializer(serializers.ModelSerializer):
  """JSON serializer for Expenses"""
  class Meta:
    model = Expense
    fields = ('id', 'expense_type', 'trip', 'leg', 'amount', 'comment', 'title')
    depth = 2
    
class ExpenseView(ViewSet):
  """Vacationista Expense View"""
  
  def retrieve(self, request, pk):
    """Handle GET single expense"""
    try:
      expense = Expense.objects.get(pk=pk)
      serializer = ExpenseSerializer(expense)
      return Response(serializer.data)
    
    except Expense.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get all expenses"""
    expenses = Expense.objects.all()
    
    id = request.query_params.get('id', None)
    if id is not None:
      expenses = expenses.filter(id=id)
      
    trip = request.query_params.get('trip', None)
    if trip is not None:
      expenses = expenses.filter(trip=trip)
      
    leg = request.query_params.get('leg', None)
    if leg is not None:
      expenses = expenses.filter(leg=leg)
      
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for expenses

    Returns:
        Response -- Empty body with 204 status code
    """

    expense = Expense.objects.get(pk=pk)
    expense.expense_type = ExpenseType.objects.get(id=request.data["expense_type"])
    expense.trip = Trip.objects.get(id = request.data["trip"])
    
    try:
      expense.leg = Leg.objects.get(id = request.data["leg"])
    except:
      expense.leg = None
      
    expense.amount = request.data["amount"]
    expense.comment = request.data["comment"]
    expense.title = request.data["title"]
    
    expense.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def create(self, request):
    """Handle POST requests for a single expense"""
    
    expense_type = ExpenseType.objects.get(id=request.data["expense_type"])
    trip = Trip.objects.get(id=request.data["trip"])
    
    try:
      leg = Leg.objects.get(id=request.data["leg"])
    except:
      leg = None
      
    expense = Expense.objects.create(
      expense_type = expense_type,
      trip = trip,
      leg = leg,
      amount = request.data["amount"],
      comment = request.data["comment"],
      title = request.data["title"]
      )
    serializer = ExpenseSerializer(expense)
    return Response(serializer.data)
  
  def destroy(self, request, pk):
    expense = Expense.objects.get(pk=pk)
    expense.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
