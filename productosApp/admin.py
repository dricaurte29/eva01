from django.contrib import admin

from .models import categoria, producto, tienda, pedido, comentario

class productadmin(admin.ModelAdmin):
    readonly_fields=('created','updated')


admin.site.register(producto, productadmin)
admin.site.register(categoria, productadmin)
admin.site.register(tienda, productadmin)
admin.site.register(pedido, productadmin)
admin.site.register(comentario, productadmin)
