from django.contrib import admin
from stocks import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'stocks/', views.get_list, name='stocks-list'),
    path(r'stocks/post/', views.post_list, name='stocks-post'),
    path(r'stocks/<int:pk>/', views.get_detail, name='stocks-detail'),
    path(r'stocks/<int:pk>/put/', views.put_detail, name='stocks-put'),
    path(r'stocks/<int:pk>/delete/', views.delete_detail, name='stocks-delete'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('admin/', admin.site.urls),
]