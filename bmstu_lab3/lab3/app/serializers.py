from app.models import *
from rest_framework import serializers


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ['login']

class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'full_name', 'phone_number', 'is_staff', 'is_superuser']

class UserOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email',  'full_name']

class VacanciesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vacancies
        fields = "__all__"


class ResponsesSerializer(serializers.ModelSerializer):
    user = UserOnlySerializer(source='id_user')
    moderator = UserOnlySerializer(source='id_moderator')
    class Meta:
        model = Responses
        fields = ['id', 'user', 'moderator', 'creation_date', 'editing_date', 'approving_date','status', 'suite']

class RespIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responses
        fields = ['id']

class RespVacSerializer(serializers.ModelSerializer):
    vac = serializers.StringRelatedField(read_only=True)
    resp = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ResponsesVacancies
        fields = "__all__"

class FullRespSerializer(serializers.ModelSerializer):
    vac = serializers.SerializerMethodField()

    def get_vac(self, obj):
        response_vacancies = ResponsesVacancies.objects.filter(id_responses=obj.id)
        vacancy_ids = response_vacancies.values_list('id_vacancies', flat=True)
        vacancies = Vacancies.objects.filter(id__in=vacancy_ids)
        return VacanciesSerializer(vacancies, many=True).data

    class Meta:
        model = Responses
        fields = ['id', 'status', 'creation_date', 'editing_date', 'approving_date', 'id_moderator', 'id_user', 'vac']