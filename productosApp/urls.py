from django.contrib import admin
from django.urls import path
from productosApp import views



urlpatterns = [
    path('',views.productos, name="productos"),
    path('/categorias/<str:cate>/',views.categorias, name="categorias"),
    path('/vista/<int:producto_id>/',views.solo, name="solo"),
    path('/favorit/<int:producto_id>/',views.favorit,name="favorit"),
    path('/unfavorit/<int:producto_id>/',views.unfavorit,name="unfavorit"),
    path('/form/<int:tienda_id>/',views.form, name="form"),
    path('/eliminar/<int:tienda_id>/<int:producto_id>/',views.elimi, name="elimi"),
    path('/archivar/<int:tienda_id>/<int:producto_id>/',views.archivar, name="archivar"),
    path('/desarchivar/<int:tienda_id>/<int:producto_id>/',views.desarchivar, name="desarchivar"),
    path('/envia/<int:tienda_id>/<int:pedido_id>/',views.envia, name="envia"),
    path('/edit/<int:tienda_id>/<int:producto_id>/',views.edit, name="edit"),
    path('/pedi/<int:tienda_id>/<int:producto_id>/',views.pedidos, name="pedido")

]

