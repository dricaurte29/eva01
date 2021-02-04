from django.contrib import admin

from .models import categoria, producto, tienda, pedido, comentario, favorito

class productadmin(admin.ModelAdmin):
    readonly_fields=('created',)


admin.site.register(producto, productadmin)
admin.site.register(categoria, productadmin)
admin.site.register(tienda, productadmin)
admin.site.register(pedido, productadmin)
admin.site.register(comentario, productadmin)
admin.site.register(favorito, productadmin)
