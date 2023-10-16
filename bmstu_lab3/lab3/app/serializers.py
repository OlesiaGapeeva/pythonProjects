from app.models import *
from rest_framework import serializers


class VacanciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancies
        fields = "__all__"

class ResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responses
        fields = "__all__"

class RespVacSerializer(serializers.ModelSerializer):
    dish = serializers.StringRelatedField(read_only=True)
    order = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ResponsesVacancies
        fields = "__all__"