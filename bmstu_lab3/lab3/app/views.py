from django.shortcuts import get_object_or_404
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from app.serializers import *
from app.models import *
from minio import Minio
from rest_framework import status
from django.http import HttpResponseBadRequest
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import redis
from minio import Minio
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes, action
from django.http import HttpResponseServerError
import os
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from app.permissions import *
from django.conf import settings
import redis
import uuid
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.db.models import Q


session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

# class CurrentUserSingleton: 
#     _instance = None 
 
#     @classmethod 
#     def get_instance(cls): 
#         if not cls._instance: 
#             cls._instance = cls._get_user() 
#         return cls._instance 
 
#     @classmethod 
#     def _get_user(cls): 
#         return CustomUser.objects.get(email='test@mail.ru', password='1')
    


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    model_class = CustomUser
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        print('req is', request.data)
        if self.model_class.objects.filter(email=request.data['email']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = self.model_class.objects.create_user(email=serializer.data['email'],
                                     password=serializer.data['password'],
                                     full_name=serializer.data['full_name'],
                                     phone_number=serializer.data['phone_number'],
                                     is_superuser=serializer.data['is_superuser'],
                                     is_staff=serializer.data['is_staff'])
            user.save()
            random_key = str(uuid.uuid4())
            session_storage.set(random_key, serializer.data['email'])
            user_data = {
                "email": request.data['email'],
                "full_name": request.data['full_name'],
                "phone_number": request.data['phone_number'],
                "is_superuser": False
            }
            print('user data is ', user_data)
            response = Response(user_data, status=status.HTTP_201_CREATED)
            # response = HttpResponse("{'status': 'ok'}")
            response.set_cookie("session_id", random_key)
            return response
            # return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#Vacancies
# @permission_classes([IsAuthenticated])
# @permission_classes([IsAdmin])
# @permission_classes([IsManager])
@api_view(['GET'])
def GetVacancies(request):
    keyword = request.query_params.get('keyword')  # Получаем значение параметра "keyword" из запроса
    if keyword:
        keyword = keyword[0].upper() + keyword[1:]
        vacancies = Vacancies.objects.filter(status='enabled').filter(title__icontains=keyword)
        if not vacancies.exists():
            return Response("Такой вакансии нет")

    else:
        vacancies = Vacancies.objects.filter(status='enabled')
    
    try:
        ssid = request.COOKIES["session_id"]
        print(ssid)
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
        resp = Responses.objects.filter(id_user=current_user, status="registered").latest('creation_date')
        serializer = VacanciesSerializer(vacancies, many=True)
        resp_serializer = ResponsesSerializer(resp)
        result = {
            'resp_id':  resp_serializer.data['id'],
            'vacancies': serializer.data
        }
        return Response(result)
    except:
        print("no session")
        serializer = VacanciesSerializer(vacancies, many=True)
        result = {
            'vacancies': serializer.data
        }
        return Response(result)


@api_view(['GET'])
def GetVacancy(request, pk):
    if not Vacancies.objects.filter(id=pk).exists():
        return Response(f"Вакансии с таким id нет")
    vacancy = Vacancies.objects.get(id=pk)
    serializer = VacanciesSerializer(vacancy)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsManager])      
def PostVacancies(request):
    serializer = VacanciesSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    nv = serializer.save()
    vacancies = Vacancies.objects.filter(status="enabled")
    serializer = VacanciesSerializer(vacancies, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsManager])
def DeleteVac(request, pk):
    if not Vacancies.objects.filter(id=pk).exists():
        return Response(f"Вакансии с таким id нет")
    vacancy = Vacancies.objects.get(id=pk)
    vacancy.status = "deleted"
    vacancy.save()

    vacancy = Vacancies.objects.filter(status="enabled")
    serializer = VacanciesSerializer(vacancy, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsManager])
def postImageToVacancies(request, pk):
    if 'file' in request.FILES:
        file = request.FILES['file']
        vacancy = Vacancies.objects.get(pk=pk, status='enabled')
        
        client = Minio(endpoint="localhost:9000",
                       access_key='minioadmin',
                       secret_key='minioadmin',
                       secure=False)

        bucket_name = 'images'
        file_name = file.name
        file_path = "http://localhost:9000/images/" + file_name
        
        try:
            client.put_object(bucket_name, file_name, file, length=file.size, content_type=file.content_type)
            print("Файл успешно загружен в Minio.")
            
            serializer = VacanciesSerializer(instance=vacancy, data={'image': file_path}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse('Image uploaded successfully.')
            else:
                return HttpResponseBadRequest('Invalid data.')
        except Exception as e:
            print("Ошибка при загрузке файла в Minio:", str(e))
            return HttpResponseServerError('An error occurred during file upload.')

    return HttpResponseBadRequest('Invalid request.')



@swagger_auto_schema(method='put', request_body=VacanciesSerializer)
@api_view(['PUT'])
@permission_classes([IsManager])
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
        

# @api_view(['PUT'])
# def VacDetails(request, pk):
#     try:
#         vacancy = Vacancies.objects.get(id=pk)
#     except Vacancies.DoesNotExist:
#         return Response("Вакансии с таким id нет")

#     serializer = VacanciesSerializer(vacancy, data=request.data, partial=True)

#     if serializer.is_valid():
#         serializer.save()
#         vacancy = Vacancies.objects.filter(status="enabled")
#         serializer = VacanciesSerializer(vacancy, many=True)
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors)
    
    
# @api_view(['POST'])
# def AddVacToRes(request, pk):
#     try: 
#         resp = Responses.objects.filter(id_user=user, status="registered").latest('creation_date') 
#     except Responses.DoesNotExist:
#         resp = Responses(                             
#             status='registered',
#             creation_date=datetime.now(),
#             id_user=user,
#         )
#         resp.save()

#     id_responses = resp.id
#     id_vacancies = pk
#     try:
#         vacancy = Vacancies.objects.get(id=id_vacancies)
#         id_vacancies = ResponsesVacancies.objects.get(id_responses=id_responses, id_vacancies=vacancy) # проверка есть ли такая м-м
#         return Response(f"Такой отклик на эту вакансию уже есть")
#     except ResponsesVacancies.DoesNotExist:
#         rv = ResponsesVacancies(                            # если нет, создаем м-м
#             id_responses=resp, id_vacancies=vacancy
#         )
#         rv.save()

#     resp = Responses.objects.all()  # выводим все заказы
#     serializer = ResponsesSerializer(resp, many=True)
#     return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuth])
def AddVacToRes(request, pk):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response('Сессия не найдена')
    try: 
        resp = Responses.objects.filter(id_user=current_user, status="registered").latest('creation_date') 
    except Responses.DoesNotExist:
        resp = Responses(                             
            status='registered',
            creation_date=datetime.now(),
            id_user=current_user,
        )
        resp.save()
    id_responses = resp.id
    try:
        vacancies = Vacancies.objects.get(pk=pk, status='enabled')
    except Vacancies.DoesNotExist:
        return Response("Такой вакансии нет", status=400)
    try:
        id_vacancies = ResponsesVacancies.objects.get(id_responses=id_responses, id_vacancies=vacancies) # проверка есть ли такая м-м
        return Response(f"Такой отклик на эту вакансию уже есть", status=400)
    except ResponsesVacancies.DoesNotExist:
        rv = ResponsesVacancies(                            # если нет, создаем м-м
            id_responses=resp, id_vacancies=vacancies
        )
        rv.save()
    # resp = Responses.objects.filter(id_user=current_user, status='registered')
    # serializer = ResponsesSerializer(resp, many = True)
    addedvac = Vacancies.objects.get(pk = pk)
    serializer = VacanciesSerializer(addedvac)
    return Response(serializer.data)

#Responces

@api_view(['GET'])
@permission_classes([IsAuth])
def GetResponses(request):
    try:
        ssid = request.COOKIES["session_id"]
    except:
        return Response('Сессия не найдена', status=403)    
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response('Сессия не найдена')
    date_format = "%Y-%m-%d"
    start_date_str = request.query_params.get('start', '2023-01-01')
    end_date_str = request.query_params.get('end', '2023-12-31')
    status = request.query_params.get('status')  # Получаем параметр "status" из запроса

    start = datetime.strptime(start_date_str, date_format).date()
    end = datetime.strptime(end_date_str, date_format).date()

    # Формируем фильтр по дате и статусу
    filter_kwargs = {
        'creation_date__range': (start, end),
    }
    # if status:
    #     filter_kwargs['status'] = status

    if status:
        if status != 'deleted':
                # Используем Q-объект для исключения заявок со статусом "deleted"
            filter_kwargs['status'] = ~Q(status='deleted')
        else:
            # Если параметр статуса не указан, исключаем заявки со статусом "deleted"
            filter_kwargs['status'] = ~Q(status='deleted')

    if current_user.is_superuser: # Модератор может смотреть заявки всех пользователей
        resp = Responses.objects.filter(**filter_kwargs).order_by('creation_date')
        serializer = ResponsesSerializer(resp, many=True)

        return Response(serializer.data)
    else: # Авторизованный пользователь может смотреть только свои заявки
        resp = Responses.objects.filter(**filter_kwargs).filter(id_user = current_user).order_by('creation_date')
        serializer = ResponsesSerializer(resp, many=True)

        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuth])
def GetResponse(request, pk):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
        print(current_user)
    except:
        return Response('Сессия не найдена')
    
    try:
        resp = Responses.objects.get(pk=pk)
        if resp.status == "deleted" or not resp:
            return Response("Отклика с таким id нет")
        resp_serializer = ResponsesSerializer(resp)
        if (current_user.is_superuser):
            vac_resp = ResponsesVacancies.objects.filter(id_responses=resp)
            vacancy_ids = [rv.id_vacancies.id for rv in vac_resp]
            vacancies = Vacancies.objects.filter(id__in=vacancy_ids)
            vacancies_serializer = VacanciesSerializer(vacancies, many= True)
            response_data = {
                'response': resp_serializer.data,
                'id_vac':vacancy_ids,
                'vacancies':  vacancies_serializer.data
            }
            return Response(response_data)
        else:
            try:
                resp = Responses.objects.get(id_user=current_user, pk=pk)
                print("not superuser")
                vac_resp = ResponsesVacancies.objects.filter(id_responses=resp)
                vacancy_ids = [rv.id_vacancies.id for rv in vac_resp]
                vacancies = Vacancies.objects.filter(id__in=vacancy_ids)
                vacancies_serializer = VacanciesSerializer(vacancies, many= True)
                response_data = {
                    'response': resp_serializer.data,
                    'vacancies': vacancies_serializer.data
            }
                return Response(response_data)
            except Responses.DoesNotExist:
                return Response("Отклика с таким  id  у данного пользователя нет")
    except Responses.DoesNotExist:
        return Response("Отклика с таким id нет")
    
@api_view(['DELETE'])
@permission_classes([IsAuth])
def DeleteResponce(request):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response('Сессия не найдена')

    try: 
        resp = Responses.objects.get(id_user=current_user, status="registered")
        resp.status = "delited"
        resp.editing_date=datetime.now()
        resp.save()
        return Response({'status': 'Success'})
    except:
        return Response("У данного пользователя нет заявки", status=400)

@swagger_auto_schema(method='put', request_body=ResponsesSerializer)
@api_view(['PUT'])
@permission_classes([IsAuth])
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

@swagger_auto_schema(method='put', request_body=ResponsesSerializer)
@api_view(['PUT'])
@permission_classes([IsManager])                                  # статусы админа
def ConfirmResponce(request, pk):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
        print("get user:", current_user)
    except:
        return Response('Сессия не найдена')
    
    if not Responses.objects.filter(id=pk).exists():
        return Response(f"Отклика с таким id нет")

    resp = Responses.objects.get(id=pk)

    if resp.status != "made":
        return Response("Такой отклик не отправлен на проверку")
    if request.data["status"] not in ["denied", "approved"]:
        return Response("Ошибка, неверный статус")
    resp.status = request.data["status"]
    print(current_user)
    resp.approving_date=datetime.now()
    resp.id_moderator = CustomUser.objects.get(email=email)
    resp.save()

    serializer = ResponsesSerializer(resp)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuth])
def ToResponce(request):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response('Сессия не найдена')

    try: 
        resp = Responses.objects.get(id_user=current_user, status="registered")
        resp.status = "made"
        resp.editing_date_date=datetime.now()
        resp.save()
        return Response({"Cформировано, отправлено на проверку модератору"})
    except:
        return Response("У данного пользователя нет зарегистрированного отклика", status=400)



from .models import Vacancies

# @api_view(['PUT'])
# def PutVacResp(request, pk):
#     if not ResponsesVacancies.objects.filter(id=pk).exists():
#         return Response("Связи м-м с таким id нет")

#     rv = ResponsesVacancies.objects.get(id=pk)
#     id_vacancies = request.data.get("id_vacancies")

#     if id_vacancies is not None:
#         try:
#             vacancy = Vacancies.objects.get(id=id_vacancies)
#             rv.id_vacancies = vacancy
#         except Vacancies.DoesNotExist:
#             return Response("Вакансии с таким id не существует")

#     rv.save()

#     responses_vacancies = ResponsesVacancies.objects.all()
#     serializer = RespVacSerializer(responses_vacancies, many=True)
#     return Response(serializer.data)

@api_view(['DELETE'])                                # удаление м-м
def DeleteVacResp(request, pk):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response('Сессия не найдена')
    resp = get_object_or_404(Responses, id_user=current_user, status="registered")
    try:
        vacancy = Vacancies.objects.get(pk=pk, status='enabled')
        try:
            rv = get_object_or_404(ResponsesVacancies, id_responses=resp, id_vacancies=vacancy)
            rv.delete()
            return Response("Вакансия удалена из отклика", status=200)
        except ResponsesVacancies.DoesNotExist:
            return Response("Заявка не найдена", status=404)
    except Vacancies.DoesNotExist:
        return Response("Такая вакансия не была добавлена в отклик", status=400)
    # if not ResponsesVacancies.objects.filter(id=pk).filter(id_responses = resp).exists():
    #     return Response(f"Связи м-м с таким у id нет")

    # rv = get_object_or_404(ResponsesVacancies, id=pk)
    # rv.delete()

    # return GetResponse(request, resp)
    # rv = ResponsesVacancies.objects.all()
    # serializer = RespVacSerializer(rv, many=True)
    # return Response(serializer.data)

# @swagger_auto_schema(method='post', request_body=openapi.Schema(
#     type=openapi.TYPE_OBJECT,
#     properties={
#         'email': openapi.Schema(type=openapi.TYPE_STRING),
#         'password': openapi.Schema(type=openapi.TYPE_STRING)
#     },
#     required=['email', 'password']
# ))
@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=username, password=password)
    
    if user is not None:
        print(user)
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)
        user_data = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "phone_number": user.phone_number,
            "password": user.password,
            "is_superuser": user.is_superuser,
        }
        response = Response(user_data, status=status.HTTP_201_CREATED)
        response.set_cookie("session_id", random_key, samesite="Lax")
        return response
    else:
        return HttpResponse("login failed", status=400)
    
@api_view(['POST'])
@permission_classes([IsAuth])
def logout_view(request):
    ssid = request.COOKIES["session_id"]
    if session_storage.exists(ssid):
        session_storage.delete(ssid)
        response_data = {'status': 'Success'}
    else:
        response_data = {'status': 'Error', 'message': 'Session does not exist'}
    return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuth])
def user_info(request):
    try:
        ssid = request.COOKIES["session_id"]
        if session_storage.exists(ssid):
            email = session_storage.get(ssid).decode('utf-8')
            user = CustomUser.objects.get(email=email)
            user_data = {
                "user_id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "phone_number": user.phone_number,
                "is_superuser": user.is_superuser
            }
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Error', 'message': 'Session does not exist'})
    except:
        return Response({'status': 'Error', 'message': 'Cookies are not transmitted'})
    
    
@api_view(['GET'])
def handle_async_task(request):
    print("HHHHHHHHh")
    resp_id = int(request.data.get('resp_id'))
    token = 4321
    print(resp_id)
    second_service_url = "http://localhost:8088/async_task"
    data = {
        'resp_id': resp_id,
        'token': token
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(second_service_url, data=data)
    exp = Responses.objects.get(id=resp_id)
    
    # Обработка ответа от второго сервиса
    if response.status_code == 200:
        exp.suite = "Отправлено на ревью"
        exp.save()
        serializer = ResponsesSerializer(exp)
        return Response(serializer.data)
    else:
        return Response(data={'error': 'Запрос завершился с кодом: {}'.format(response.status_code)},
                        status=response.status_code)

@api_view(['PUT'])
@permission_classes([AllowAny])
def put_async(request, format=None):
    """
    Обновляет данные 
    """
    print("вызвалось")
    # Проверка метода запроса (должен быть PUT)
    if request.method != 'PUT':
        return Response({'error': 'Метод не разрешен'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    exp_id = request.data.get('resp_id')
    result = request.data.get('suite')

    # Проверка наличия всех необходимых параметров
    if not exp_id or not result :
        return Response({'error': 'Отсутствуют необходимые данные'}, status=status.HTTP_400_BAD_REQUEST)

  

    try:
        exp = Responses.objects.get(id=exp_id)
    except Responses.DoesNotExist:
        return Response({'error': 'Отклик не найден'}, status=status.HTTP_404_NOT_FOUND)

    exp.suite = str(result) + " %"
    exp.save()
    serializer = ResponsesSerializer(exp)
    print(serializer.data)
    return Response(serializer.data)

