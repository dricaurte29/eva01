from django.shortcuts import render, HttpResponse, redirect
from productosApp.models import producto, categoria, tienda, pedido, comentario
from django.contrib.auth.models import User
from django.db.models import Q
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib import messages
import os

def send_email(pe):
    template = get_template('correo.html')
    mail = pe.local.autor.email
    product = pe.item
    cl = User()
    cl = pe.cliente
    content = template.render({"producto":product,"pedido":pe,"cliente":cl})
    email = EmailMultiAlternatives(
        'Nuevo Pedido',
        'Proyecto Eva-01',
        'muestrastore@gmail.com',
        [mail]
    )
    
    email.attach_alternative(content, 'text/html')
    email.send()
    





def productos(request):
    
    
    dis = request.GET.get('dis')
    if dis:
        if dis == "a":
            request.session['distro'] = 0
        if dis == "b":
            request.session['distro'] = 1
    distro = request.session.get('distro',0)
    categorias=categoria.objects.all()
    page = request.GET.get('page',1)
    busqueda = request.GET.get('bus')
    mini = request.GET.get('min')
    maxi = request.GET.get('max')
    orden = request.GET.get('ord')
    nbn = 0

    if busqueda:
        productos = producto.objects.filter(estatus=True)
        productos = productos.filter(
            Q(titulo__icontains=busqueda) |
            Q(contenido__icontains=busqueda) |
            Q(categorian__icontains=busqueda)
            ).distinct()

        
    else:
        productos = producto.objects.filter(estatus=True)
    if mini:
        mi = int(mini)
        productos = productos.filter(precio__gt = mi-1)

    if maxi:
        ma = int(maxi)
        productos = productos.filter(precio__lt = ma+1)    
    nbn = productos.count()
    if orden:
        if orden == "reciente":
            productos = productos.order_by('-created')
        elif orden == "menor":
            productos = productos.order_by('precio')
        elif orden == "mayor":
            productos = productos.order_by('-precio')    
            
    try:
            paginator = Paginator(productos, 6)
            productos = paginator.page(page)
    except:
        raise Http404      
    return render(request, "productos.html", {"mi":mini,"ma":maxi,"distro":distro,"ord":orden,"nbn":nbn,"nb":busqueda,"entity": productos, "categorias": categorias,"paginator":paginator})

def categorias(request, cate):
    
    busqueda=categoria.objects.get(nombre= cate)
    productos=producto.objects.filter(categoria=busqueda)
    categorias=categoria.objects.all()
    return render(request, "buspro.html", {"productos": productos, "categorias": categorias, "categoria": busqueda})

def solo(request, producto_id):

    product=producto.objects.get(id= producto_id)
    comentarios = comentario.objects.filter(item_id= producto_id)
    comentarios = comentarios.order_by('-created')
    print(product.tienda_id)
    ids= product.tienda_id
    tien=tienda.objects.get(id=ids)
    page = request.GET.get('page',1)
    try:
            paginator = Paginator(comentarios, 3)
            comentarios = paginator.page(page)
    except:
        raise Http404 
    if request.method == 'POST':
        
        cm = comentario()
        cm.contenido = request.POST.get('comentario')
        use = User()
        use  = User()
        use.id = int(request.POST.get('usid'))
        cm.autor = use
        
        ite = producto.objects.get(id= int(request.POST.get('pid')))
        cm.item = ite
        ite.nr = ite.nr + 1
        ite.tr = ite.tr + int(request.POST.get('puntua'))
        ite.pr = ite.tr/ite.nr
        ite.save()
        cm.puntuacion = int(request.POST.get('puntua'))
        cm.save()
        comentarios = comentario.objects.filter(item_id= producto_id)
        comentarios = comentarios.order_by('-created')
        try:
            paginator = Paginator(comentarios, 3)
            comentarios = paginator.page(page)
        except:
            raise Http404 
        messages.success(request, "Gracias por tu comentario")
        return render(request, "solo.html",{"producto":product, "tienda":tien ,"entity":comentarios})
    return render(request, "solo.html",{"producto":product, "tienda":tien ,"entity":comentarios})

def pedidos(request, tienda_id, producto_id):
    tien = tienda.objects.get(id = tienda_id)
    product=producto.objects.get(id= producto_id)
    if request.method == 'POST':
        print('printing POST::: ', request.POST)
        pe = pedido()
        pe.item = product
        pe.cantidad = int(request.POST.get('cantidad'))
        pe.contacto = int(request.POST.get('contacto'))
        pe.direccion = request.POST.get('direccion')
        pe.detalle = request.POST.get('detalle')
        pe.precio = int(request.POST.get('total'))
        us = User()
        us.id = int(request.POST.get('usid'))
        pe.cliente = us
        pe.local = tien
        pe.save()
        send_email(pe)
        return render(request, "confirma.html",{ "tienda":tien })



    return render(request, "pedido.html",{"producto":product})

def tiend(request, tienda_id):

    tien=tienda.objects.get(id= tienda_id)
    categorias=categoria.objects.all()
    productos=producto.objects.filter(tienda_id= tienda_id)
    return render(request, "tienda.html",{"tienda":tien, "categorias": categorias, "productos":productos})

def archivar(request, tienda_id, producto_id):

    prd = producto.objects.get(id = producto_id)
    prd.estatus = False
    prd.save()
    messages.success(request, f"Anuncio archivado")
    return redirect('dashboard', tienda_id= tienda_id)

def desarchivar(request, tienda_id, producto_id):

    prd = producto.objects.get(id = producto_id)
    prd.estatus = True
    prd.save()
    messages.success(request, f"Anuncio activado")
    return redirect('dashboard', tienda_id= tienda_id)

def envia(request, tienda_id, pedido_id):
    ped = pedido.objects.get(id= pedido_id)
    ped.enviado = True
    ped.save()
    return redirect('pedidos', tienda_id= tienda_id)

def elimi(request, tienda_id, producto_id):

    prd = producto.objects.get(id= producto_id)

    prd.delete()
    messages.success(request, f"Producto eliminado")
    return redirect('dashboard', tienda_id= tienda_id)

def edit(request, tienda_id, producto_id):
    prd = producto.objects.get(id= producto_id)
    productos=producto.objects.filter(tienda_id= tienda_id, estatus= True)
    mac = productos.count()
    produ = producto.objects.filter(tienda_id= tienda_id, estatus= False)
    arc = produ.count()
    ped = pedido.objects.filter(local_id=tienda_id, enviado=False)
    pc = ped.count()

    categorias=categoria.objects.all()
    tien=tienda.objects.get(id= tienda_id)
    if request.method == 'POST':
        
        prd.titulo = request.POST.get('nombre')
        prd.contenido = request.POST.get('contenido')
        prd.precio = int(request.POST.get('precio'))
        if request.POST.get('imagen') == "":
            print("NO IMAGEN :(")
        else:
            print(request.FILES.get('imagen'))
            prd.imagen = request.FILES.get('imagen')
        if request.FILES.get('imagen2'):
            prd.imagen2 = request.FILES.get('imagen2')
        if request.FILES.get('imagen3'):
            prd.imagen2 = request.FILES.get('imagen3')

        prd.categorian = request.POST.get('categoria') 
        prd.save()
        messages.success(request, f"Anuncio actualizado")

        #print('printing POST::: ', request.POST)
        return redirect('dashboard', tienda_id= tienda_id)
    return render(request, "edit.html", {"pc":pc, "tienda": tien, "categorias":categorias, "producto":prd, "mac":mac, "arc":arc})

def form(request, tienda_id):
    categorias=categoria.objects.all()
    prod=producto.objects.filter(tienda_id= tienda_id, estatus= True)
    mac = prod.count()
    productos=producto.objects.filter(tienda_id= tienda_id, estatus= False)
    arc = productos.count()
    ped = pedido.objects.filter(local_id=tienda_id)
    pc = ped.count()
    tien=tienda.objects.get(id= tienda_id)
    if request.method == 'POST':
        pr = producto()
        pr.titulo = request.POST.get('nombre')
        pr.contenido = request.POST.get('contenido')
        pr.precio = int(request.POST.get('precio'))
        pr.imagen = request.FILES.get('imagen')
        pr.imagen2 = request.FILES.get('imagen2')
        pr.imagen3 = request.FILES.get('imagen3')
        tn = tienda()
        tn.id = tienda_id
        pr.tienda = tn
        cat = categoria()
        
        
        pr.categorian = request.POST.get('categoria')
        
        pr.save()
        messages.success(request, f"Producto creado")
        print('printing POST::: ', request.POST)
        return redirect('dashboard', tienda_id= tienda_id)
    return render(request, "formpro.html", {"tienda": tien, "categorias":categorias, "pc":pc, "mac":mac, "arc":arc})