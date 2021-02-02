
from django.urls import path
from proyectoApp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home, name="inicio"),
    path('<tienda_url>/',views.local, name="local"),
    path('info',views.infor, name="tuto"),
    path('tiendas',views.tiendas, name="tiendas"),
    path('mitienda/<int:us_id>/',views.tiendash, name="mistiendas"),
    path('dashboard/<int:tienda_id>/',views.dashboard, name="dashboard"),
    path('archivados/<int:tienda_id>/',views.archivados, name="archivados"),
    path('pedidos/<int:tienda_id>/',views.pedi, name="pedidos"),
    path('ipost/<int:tienda_id>/',views.ipost,name="ipost"),
    path('cn/<int:producto_id>/',views.modalel, name="modalel"),
    path('ped/<int:pedido_id>/',views.modalpe, name="modalpe"),
    path('ent/<int:producto_id>/<int:tienda_id>/',views.modalme, name="modalme"),
    path('entra', views.entra , name="entra"),
    path('salir', views.salir , name="salir"),
    path('registro', views.registro, name="registro"),
    path('contacto',views.contacto, name="contacto"),
    path('unete',views.solicitud, name="unete"),
    path('editar/<int:tienda_id>/',views.editienda, name="editar"),
    path('nuevatienda',views.creatienda, name ="nueva"),
    path('accounts/profile/',views.home, name="inicio"),
    
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

