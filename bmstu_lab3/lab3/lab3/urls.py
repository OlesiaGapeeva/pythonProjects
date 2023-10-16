from django.contrib import admin
from app import views
from django.urls import include, path
from rest_framework import routers


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),

    path('vacancies/', views.GetVacancies, name = 'vacancies'),
    path('vacancies/post/', views.PostVacancies, name = 'vacancies_post'),
    path('vacancies/<str:keyword>/', views.GetVacancy, name = 'vacancy'),
    path('vacancies/<int:pk>/delete/', views.DeleteVac, name = 'vacancy_delete'),
    path('vacancies/<int:pk>/put/', views.PutVacancy, name = 'vacancy_put'),
    path('vacancies/<int:pk>/add/', views.AddVacToRes, name = 'vacancy_add'),

    #Resp
    path('resp/', views.GetResponses, name = 'responses'),
    path('resp/<int:pk>/', views.GetResponse, name = 'response'),
    path('resp/<int:pk>/delete/', views.DeleteResponce, name = 'resp_delete'),
    path('resp/<int:pk>/put/', views.PutResponce, name = 'resp_put'),
    path('resp/<int:pk>/confirm/', views.ConfirmResponce, name = 'resp_confirm'),
    path('resp/<int:pk>/accept/', views.ToResponce, name = 'resp_accept'),

    #RespVac
    path('rv/<int:pk>/put/', views.PutVacResp, name = 'rv_put'),
    path('rv/<int:pk>/delete/', views.DeleteVacResp, name = 'rv_delete'),
]
