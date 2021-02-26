from django.contrib.sitemaps import Sitemap
from productosApp.models import tienda
from django.urls import reverse

class tiendaSitemap(Sitemap):
    protocol = 'https'
    def items(self):
        return tienda.objects.all()

class staticSitemap(Sitemap):
    protocol = 'https'
    def items(self):
        return ['inicio','tiendas','terminos','galleta','privacidad','contacto','unete','productos']

    def location(self, item):
        return reverse(item)
