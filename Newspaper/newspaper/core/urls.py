from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('articulo/<int:id>/', views.article_detail, name='article_detail'),
    path('categoria/<str:category_name>/', views.category_detail, name='category_detail'),
    path('article/<int:pk>/', views.article_detail_view, name='article_detail'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('buscar/', views.buscar_noticias, name='buscar_noticias'),
]
