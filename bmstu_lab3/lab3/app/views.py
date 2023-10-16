from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from app.serializers import *
from app.models import *
from minio import Minio
from rest_framework import status
from datetime import datetime

user = Users(id=1, passw="root", role = "user", login="student")

#Vacancies
@api_view(['GET'])
def GetVacancies(request):
    vacancy = Vacancies.objects.filter(status="enabled")
    serializer = VacanciesSerializer(vacancy, many=True)
    return Response(serializer.data)

@api_view(['POST'])      
def PostVacancies(request):
    serializer = VacanciesSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    nv = serializer.save()
    #картинки выгрузить в minio и в поле в бд внести адрес к этому объекту в хранилище
    client = Minio(endpoint="localhost:9000",
                   access_key='minioadmin',
                   secret_key='minioadmin',
                   secure=False)
    i=nv.id
    img_obj_name = f"vac_{i}.png"
    # Загружаем изображение в Minio
    try:
        client.fput_object(bucket_name='img',
                           object_name=img_obj_name,
                           file_path=request.data["url"])
        nv.image = f"minio://localhost:9000/img/{img_obj_name}"
    except Exception as e:
        return Response({"error": str(e)})
    
    nv.save()

    vacancies = Vacancies.objects.filter(status="enabled")
    serializer = VacanciesSerializer(vacancies, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def GetVacancy(request, keyword):
    keyword = keyword[0].upper()+keyword[1:]
    vacancies = Vacancies.objects.filter(status='enabled').filter(title=keyword)
    if not vacancies.exists():
        return Response("Такой вакансии нет")
    serializer = VacanciesSerializer(vacancies, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def DeleteVac(request, pk):
    if not Vacancies.objects.filter(id=pk).exists():
        return Response(f"Вакансии с таким id нет")
    vacancy = Vacancies.objects.get(id=pk)
    vacancy.status = "deleted"
    vacancy.save()

    vacancy = Vacancies.objects.filter(status="enabled")
    serializer = VacanciesSerializer(vacancy, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def PutVacancy(request, pk):
    try:
        vacancy = Vacancies.objects.get(id=pk)
    except Vacancies.DoesNotExist:
        return Response("Вакансии с таким id нет")

    serializer = VacanciesSerializer(vacancy, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        vacancy = Vacancies.objects.filter(status="enabled")
        serializer = VacanciesSerializer(vacancy, many=True)
        return Response(serializer.data)
    else:
        return Response(serializer.errors)

@api_view(['POST'])
def AddVacToRes(request, pk):
    try: 
        resp = Responses.objects.filter(id_user=user, status="registered").latest('creation_date') 
    except Responses.DoesNotExist:
        resp = Responses(                             
            status='registered',
            creation_date=datetime.now(),
            id_user=user,
        )
        resp.save()

    id_responses = resp.id
    id_vacancies = pk
    try:
        vacancy = Vacancies.objects.get(id=id_vacancies)
        id_vacancies = ResponsesVacancies.objects.get(id_responses=id_responses, id_vacancies=vacancy) # проверка есть ли такая м-м
        return Response(f"Такой отклик на эту вакансию уже есть")
    except ResponsesVacancies.DoesNotExist:
        rv = ResponsesVacancies(                            # если нет, создаем м-м
            id_responses=resp, id_vacancies=vacancy
        )
        rv.save()

    resp = Responses.objects.all()  # выводим все заказы
    serializer = ResponsesSerializer(resp, many=True)
    return Response(serializer.data)
#Responces

@api_view(['GET'])
def GetResponses(request):
    date_format = "%Y-%m-%d"
    start_date_str = request.query_params.get('start', '2023-01-01')
    end_date_str = request.query_params.get('end', '2023-12-31')
    start = datetime.strptime(start_date_str, date_format).date()
    end = datetime.strptime(end_date_str, date_format).date()
    responses = Responses.objects.filter(creation_date__range=(start, end)).order_by('creation_date')
    serializer = ResponsesSerializer(responses, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def GetResponse(request, pk):
    if not Responses.objects.filter(id=pk).exists():
        return Response(f"Отклика с таким id нет")

    resp = Responses.objects.get(id=pk)
    serializer = ResponsesSerializer(resp)
    return Response(serializer.data)

@api_view(['DELETE'])
def DeleteResponce(request, pk):
    if not Responses.objects.filter(id=pk).exists():
        return Response(f"Отклика с таким id нет")
    resp = Responses.objects.get(id=pk)
    resp.status = "denied"
    resp.save()

    resp = Responses.objects.all()
    serializer = ResponsesSerializer(resp, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def PutResponce(request, pk):
    try:
        resp = Responses.objects.get(id=pk)
    except Responses.DoesNotExist:
        return Response("Отклика с таким id нет")
    serializer = ResponsesSerializer(resp, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors)
    serializer.save()

    resp = Responses.objects.all()
    serializer = ResponsesSerializer(resp, many=True)
    return Response(serializer.data)

@api_view(['PUT'])                                  # статусы админа
def ConfirmResponce(request, pk):
    if not Responses.objects.filter(id=pk).exists():
        return Response(f"Отклика с таким id нет")

    resp = Responses.objects.get(id=pk)

    if resp.status != "made":
        return Response("Такой заказ не сформирован")
    if request.data["status"] not in ["denied", "approved"]:
        return Response("Ошибка, неверный статус")
    resp.status = request.data["status"]
    resp.approving_date=datetime.now()
    resp.save()

    serializer = ResponsesSerializer(resp)
    return Response(serializer.data)


@api_view(['PUT'])
def ToResponce(request, pk):
    if not Responses.objects.filter(id=pk).exists():
        return Response(f"Отклика с таким id нет")

    resp = Responses.objects.get(id=pk)

    if resp.status != "registered":
        return Response("Такой отклик не зарегистрирован")
    
    status = request.data.get("status")
    if status not in ["deleted", "made"]:
        return Response("Ошибка, неверный статус")

    resp.status = status
    resp.editing_date = datetime.now()
    resp.save()

    serializer = ResponsesSerializer(resp)
    return Response(serializer.data)


from .models import Vacancies

@api_view(['PUT'])
def PutVacResp(request, pk):
    if not ResponsesVacancies.objects.filter(id=pk).exists():
        return Response("Связи м-м с таким id нет")

    rv = ResponsesVacancies.objects.get(id=pk)
    id_vacancies = request.data.get("id_vacancies")

    if id_vacancies is not None:
        try:
            vacancy = Vacancies.objects.get(id=id_vacancies)
            rv.id_vacancies = vacancy
        except Vacancies.DoesNotExist:
            return Response("Вакансии с таким id не существует")

    rv.save()

    responses_vacancies = ResponsesVacancies.objects.all()
    serializer = RespVacSerializer(responses_vacancies, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])                                # удаление м-м
def DeleteVacResp(request, pk):
    if not ResponsesVacancies.objects.filter(id=pk).exists():
        return Response(f"Связи м-м с таким id нет?")

    rv = get_object_or_404(ResponsesVacancies, id=pk)
    rv.delete()

    rv = ResponsesVacancies.objects.all()
    serializer = RespVacSerializer(rv, many=True)
    return Response(serializer.data)


