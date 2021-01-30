from rest_framework import serializers
from .models import *


class NlpResultListSerializer(serializers.ModelSerializer):

    class Meta:
        model = NlpResult
        fields = ("document_id", "cve", "cwe", "software", "malware", "course_of_action", "intrusion_set",
                 "threat_actor", "tool", "attack_pattern", "industry", "mitre_attack", "campaign", "org",
                 "country", "city", "geolocation", "time_stamp", "ioc", "technique")


# class DocumentListSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Document
