from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CustomerSerializer,
)
from .services import (
    top_five_total,
)


# class ApiView(ModelViewSet):
#     serializer_class = CustomerSerializer
#     queryset = top_five_total()


class ApiView(APIView):
    def get(self, request: Request) -> Response:
        queryset = top_five_total()
        serializer = CustomerSerializer(queryset, many=True)
        return Response({
            'response': serializer.data,
        })

    def post(self, request: Request) -> Response:
        pass
