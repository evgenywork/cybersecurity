import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from document.rabbitmq_client import RabbitmqClient

from .models import *
from .serializers import *


class NlpResultListView(APIView):

    def get(self, request):
        nlp_results = NlpResult.objects.filter(is_active=True)

        serializer = NlpResultListSerializer(nlp_results, many=True)
        return Response(serializer.data)


class NlpResultFilteredListView(APIView):

    def get(self, request, value):

        split_value = value.split('___')

        column_name = split_value[0]
        column_value = split_value[1]

        nlp_results = NlpResult.objects.filter(is_active=True, **{column_name: column_value})

        serializer = NlpResultListSerializer(nlp_results, many=True)
        return Response(serializer.data)


class FilterMalwareListView(APIView):

    def get(self, request, *args, **kw):

        # Any URL parameters get passed in **kw
        nlp_results = NlpResult.objects.filter(is_active=True).distinct('malware')

        result = [{
            "label": "All",
            "value": "__all__",
        }]
        for nlp_result in nlp_results:
            result.append({
                "label": nlp_result.malware,
                "value": 'malware___' + nlp_result.malware,
            })

        response = Response(result, status=status.HTTP_200_OK)
        return response


class DocumentUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        original_name = request.data['file_path']
        serializer = DocumentSerializer(data=request.data)

        if not request.data:
            return Response({"Error": "No file selected"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(original_name=original_name)
            document_id = serializer.data['id']
            file_path = serializer.data['file_path']
            domain = request.get_host()
            file_url = 'https://' + domain + file_path

            # Config for RabbitMQ
            rabbitmq_cfg = {
                "host": "89.223.95.49",
                "port": 5672,
                "user": "devlabs",
                "password": "n3dF8dfXpweZv",
                "exchange": "rvision-hack"
            }
            url = 'http://89.223.95.49:8887/upload'
            print('Try to connect to RabbitmqClient...')
            # создаем клиента
            rabbitmq_client = RabbitmqClient(rabbitmq_cfg)

            doc = {
                "doc_id": document_id,
                "link": file_url,
            }

            # скорее всего, удобно будет отправлять сообщения в формате JSON, так что
            rabbitmq_client.send_msg(json.dumps(doc))

            # в конце работы закроем соединение
            rabbitmq_client.close_connection()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
