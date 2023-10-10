from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from stocks.serializers import StockSerializer
from stocks.models import Stock
from rest_framework.decorators import api_view

@api_view(['Get'])
def get_list(request, format=None):
    """
    Возвращает список акций
    """
    print('get')
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)

@api_view(['Post'])
def post_list(request, format=None):    
    """
    Добавляет новую акцию
    """
    print('post')
    serializer = StockSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Get'])
def get_detail(request, pk, format=None):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == 'GET':
        """
        Возвращает информацию об акции
        """
        serializer = StockSerializer(stock)
        return Response(serializer.data)

@api_view(['Put'])
def put_detail(request, pk, format=None):
    """
    Обновляет информацию об акции
    """
    stock = get_object_or_404(Stock, pk=pk)
    serializer = StockSerializer(stock, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Delete'])
def delete_detail(request, pk, format=None):    
    """
    Удаляет информацию об акции
    """
    stock = get_object_or_404(Stock, pk=pk)
    stock.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)