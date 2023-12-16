from django.contrib import admin
from app import views
from django.urls import include, path
from rest_framework import routers
from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router.register(r'user', views.UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login',  views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('user_info', views.user_info, name='user_info'),
    path('', include(router.urls)),

    path('vacancies/', views.GetVacancies, name = 'vacancies'),
    path('vacancies/post', views.PostVacancies, name = 'vacancies_post'),
    path('vacancies/<int:pk>', views.GetVacancy, name = 'vacancy'),
    #path('vacancies/<int:pk>', views.VacDetails, name = 'vacancy'),
    path('vacancies/<int:pk>/delete', views.DeleteVac, name = 'vacancy_del'),
    path('vacancies/<int:pk>/put/', views.PutVacancy, name = 'vacancy_put'),
    path('vacancies/<int:pk>/add/', views.AddVacToRes, name = 'vacancy_add'),
    path('vacancies/<int:pk>/image', views.postImageToVacancies, name="post-image-to-vacancies"),
    #Resp
    path('resp/', views.GetResponses, name = 'responses'),
    path('resp/<int:pk>/', views.GetResponse, name = 'response'),
    path('resp/delete', views.DeleteResponce, name = 'resp_delete'),
    path('resp/<int:pk>/put', views.PutResponce, name = 'resp_put'),
    path('resp/<int:pk>/confirm/', views.ConfirmResponce, name = 'resp_confirm'),
    path('resp/made/', views.ToResponce, name = 'resp_made'),
    path('async_task', views.handle_async_task, name = 'async_task'),
    path('resp/update_async/', views.put_async, name = 'upd_async'),
    

    #RespVac
    # path('rv/<int:pk>/put/', views.PutVacResp, name = 'rv_put'),
    path('rv/<int:pk>/', views.DeleteVacResp, name = 'rv_delete'),
]
