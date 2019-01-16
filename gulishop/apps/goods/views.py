from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import GoodsSerializers
from rest_framework.response import Response
from .models import Goods
from rest_framework import status
from django.http import JsonResponse


class GoodsView(APIView):
    def get(self, request):
        all_goods = Goods.objects.all()
        serializer = GoodsSerializers(all_goods, many=True)
        # return Response(data=serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


class GoodsSingingView(APIView):
    def get(self, request, pk):
        goods = Goods.objects.filter(id=int(pk))
        serializer = GoodsSerializers(goods, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)