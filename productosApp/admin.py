from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin 
from .models import categoria, producto, tienda, pedido, comentario, favorito



class pedRes(resources.ModelResource):
    class Meta:
        model = pedido
class tnRes(resources.ModelResource):
    class Meta:
        model = tienda

class usRes(resources.ModelResource):
    class Meta:
        model = User

class UserAdmin(ImportExportModelAdmin, UserAdmin):
    resource_class = usRes

class productadmin(admin.ModelAdmin):
    readonly_fields=('created',)
class pedidoadmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=["item","local","cliente","created","precio"]
    readonly_fields=('created',)
    search_fields=["cliente",]
    list_filter=["local","enviado","created"]
    date_hierarchy="created"
    resource_class = pedRes
class prod(admin.ModelAdmin):
    readonly_fields=('created',)
    list_display=("titulo","tienda","categorian","precio")
    search_fields=("titulo","tienda")
    list_filter=("tienda","estatus")
class tn(ImportExportModelAdmin,admin.ModelAdmin):
    readonly_fields=('created',)
    list_display=("nombre","autor","categoria")
    search_fields=("nombre",)
    list_filter=("categoria",)
    resource_class = tnRes

admin.site.register(producto, prod)
admin.site.register(categoria, productadmin)
admin.site.register(tienda, tn)
admin.site.register(pedido, pedidoadmin)
admin.site.register(comentario, productadmin)
admin.site.register(favorito, productadmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

