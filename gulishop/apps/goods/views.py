from .models import Goods
from rest_framework import status
from rest_framework.views import APIView
from .serializers import GoodsSerializer
from rest_framework.response import Response

# Create your views here.


class GoodsView(APIView):
    def get(self, request):
        all_goods = Goods.objects.all()
        serializer = GoodsSerializer(all_goods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



