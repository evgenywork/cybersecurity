from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import NlpResultListSerializer


class NlpResultListView(APIView):

    def get(self, request):
        nlp_results = NlpResult.objects.filter(is_active=True)

        serializer = NlpResultListSerializer(nlp_results, many=True)
        return Response(serializer.data)
