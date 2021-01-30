from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import *
from .serializers import NlpResultListSerializer


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