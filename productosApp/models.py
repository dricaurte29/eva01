from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import os


class tienda(models.Model):
    nombre=models.CharField(max_length=50)
    created=models.DateField(auto_now_add=True)
    
    descripcion=models.CharField(max_length=100)
    autor=models.ForeignKey(User, related_name='tiendas', on_delete=models.CASCADE)
    instagram_link=models.CharField(max_length=255, blank=True)
    whatsapp_link=models.CharField(max_length=255, blank=True)
    facebook_link=models.CharField(max_length=255, blank=True)
    instagram_post=models.CharField(max_length=255, blank=True)
    facebook_post=models.CharField(max_length=255, blank=True)
    foto_perfil=models.ImageField(upload_to='fototd')
    foto_fondo=models.ImageField(upload_to='fototd')
    ubicacion =models.CharField(max_length=30)
    categoria = models.CharField(max_length=30)
    url = models.CharField(max_length=30)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.foto_perfil.path):
            os.remove(self.foto_perfil.path)
        super(tienda, self).delete(*args, **kwargs)
    class meta:
        verbose_name='tienda'
        verbose_name_plural='tiendas'
    def __str__(self):
        return self.nombre
    def get_absolute_url(self):
        
        return reverse("local", args=[str(self.url)])
    
    
class categoria(models.Model):
    nombre=models.CharField(max_length=50)


    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)
    
    class meta:
        verbose_name='categoria'
        verbose_name_plural='categorias'

    def __str__(self):
        return self.nombre

class producto(models.Model):
    titulo=models.CharField(max_length=50)
    contenido=models.TextField(max_length=1000)
    imagen=models.ImageField(upload_to='fotopr')
    imagen2=models.ImageField(upload_to='fotopr',blank=True)
    imagen3=models.ImageField(upload_to='fotopr',blank=True)
    tienda=models.ForeignKey(tienda, related_name='productos', on_delete=models.CASCADE)
    estatus = models.BooleanField(default=True)
    categorian=models.CharField(max_length=25)
    created=models.DateField(auto_now_add=True)
    
    precio=models.IntegerField()
    nr=models.IntegerField(default=0)
    tr=models.IntegerField(default=0)
    pr=models.FloatField(default=0)
    def delete(self, *args, **kwargs):
        if os.path.isfile(self.imagen.path):
            os.remove(self.imagen.path)
        try:    
            if os.path.isfile(self.imagen2.path):
                os.remove(self.imagen2.path)

        except:
            b=1
        try:
            if os.path.isfile(self.imagen3.path):
                os.remove(self.imagen3.path)
        except:
            a=0
        super(producto, self).delete(*args, **kwargs)
    class meta:
        verbose_name='post'
        verbose_name_plural='postes'

    def __str__(self):
        return self.titulo




class pedido(models.Model):
    item = models.ForeignKey(producto, related_name='producto', on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, related_name='pedidos', on_delete=models.CASCADE)
    local = models.ForeignKey(tienda, related_name='pedidos', on_delete=models.CASCADE)
    created=models.DateField(auto_now_add=True)
    
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    detalle = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    enviado = models.BooleanField(default=False)

    class meta:
        verbose_name='pedido'
        verbose_name_plural='pedidos'

    def __str__(self):
        return self.item.titulo
class comentario(models.Model):
    item = models.ForeignKey(producto, related_name='product', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, related_name='comentarios', on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    created=models.DateField(auto_now_add=True)
    
    contenido=models.CharField(max_length=140, null=True)
    class meta:
        verbose_name='comentario'
        verbose_name_plural='comentarios'

    def __str__(self):
        return self.item.titulo

class favorito(models.Model):
    item = models.ForeignKey(producto, related_name='produ', on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, related_name='favoritos', on_delete=models.CASCADE)
    created=models.DateField(auto_now_add=True)
    

    class meta:
        verbose_name='favorito'
        verbose_name_plural='favoritos'

    def __str__(self):
        return self.item.titulo






