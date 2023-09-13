from rest_framework.parsers import (
    FormParser,
    MultiPartParser,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CustomerSerializer,
)
from .services import CustomerService


class ApiView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request: Request) -> Response:
        queryset = CustomerService.top_five_total()
        serializer = CustomerSerializer(queryset, many=True)
        return Response({
            'response': serializer.data,
        })

    def post(self, request: Request) -> Response:
        file_object = request.FILES.get('deals')
        return CustomerService.import_csv(file_object=file_object)
