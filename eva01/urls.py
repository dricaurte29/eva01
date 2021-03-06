"""eva01 URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler500, handler404
from django.contrib.sitemaps.views import sitemap
from proyectoApp.sitemaps import tiendaSitemap, staticSitemap

sitemaps = {
    'tiendas': tiendaSitemap,
    'static': staticSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('proyectoApp.urls')),
    path('productos', include('productosApp.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('', include('pwa.urls')),
    path('sitemap.xml',sitemap, {'sitemaps': sitemaps}),
 
    
    
]
handler500 = 'proyectoApp.views.error404'
handler404 = 'proyectoApp.views.error'



urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
