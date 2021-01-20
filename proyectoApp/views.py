from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import usuariof
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from productosApp.models import producto, categoria, tienda, pedido
from django.core.paginator import Paginator
from django.http import Http404
from django.core.mail import send_mail

def estrella(request):
    
    return render(request, "proyectoApp/estrella.html")

def home(request):
    categorias=categoria.objects.all()
    productos=producto.objects.all()
    productos=productos.order_by('?')
    tiendas=tienda.objects.all()
    tiendas=tiendas.order_by('?')
    return render(request, "proyectoApp/inicio.html", {"productos": productos, "categorias": categorias, "tiendas": tiendas})



def tiendas(request):
    tien=tienda.objects.all()
    page = request.GET.get('page',1)
    busqueda = request.GET.get('bus')
    if busqueda:
        
        tien = tienda.objects.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(categoria__icontains=busqueda) 
            ).distinct()
    try:
            paginator = Paginator(tien, 3)
            tien = paginator.page(page)
    except:
        raise Http404
    return render(request, "proyectoApp/tiendas.html", {"entity":tien,"paginator":paginator})

def local(request, tienda_url):

    tien=tienda.objects.get(url= tienda_url)
    categorias=categoria.objects.all()
    productos=producto.objects.filter(tienda_id= tien.id)
    return render(request, "proyectoApp/tienda.html",{"tienda":tien, "categorias": categorias, "productos":productos})

def creatienda(request):

    if request.method == 'POST':
        ti = tienda()
        ti.nombre = request.POST.get('nombre')
        ti.descripcion = request.POST.get('descripcion')
        ti.ubicacion = request.POST.get('ubicacion')
        ti.instagram_link = request.POST.get('insta')
        ti.whatsapp_link = request.POST.get('num')
        ti.facebook_link = request.POST.get('face')
        ti.foto_perfil = request.FILES.get('imagen')
        ti.foto_fondo = request.FILES.get('imagen2')
        us = User()
        us.id = int(request.POST.get('usid'))
        ti.autor = us
        ti.save()
        messages.success(request, "Tienda Creada")
        return redirect('inicio')
    return render(request, "proyectoApp/tform.html")

def tiendash(request, us_id):
    tien=tienda.objects.filter(autor_id= us_id)
    return render(request, "proyectoApp/tiendash.html", {"tiendas":tien})


     
def dashboard(request, tienda_id):
    tien=tienda.objects.get(id= tienda_id)
    productos=producto.objects.filter(tienda_id= tienda_id, estatus= True)
    mac = productos.count()
    produ = producto.objects.filter(tienda_id= tienda_id, estatus= False)
    arc = produ.count()
    ped = pedido.objects.filter(local_id=tienda_id, enviado=False)
    pc = ped.count()
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(productos, 5)
        productos = paginator.page(page)
    except:
        raise Http404
    return render(request, "proyectoApp/dashboard.html", {"tienda":tien, "entity":productos, "pc":pc, "mac":mac, "arc":arc, "paginator":paginator})

def archivados(request, tienda_id):
    tien=tienda.objects.get(id= tienda_id)
    prod=producto.objects.filter(tienda_id= tienda_id, estatus= True)
    mac = prod.count()
    productos=producto.objects.filter(tienda_id= tienda_id, estatus= False)
    arc = productos.count()
    ped = pedido.objects.filter(local_id=tienda_id)
    pc = ped.count()
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(productos, 5)
        productos = paginator.page(page)
    except:
        raise Http404
    return render(request, "proyectoApp/archivados.html", {"tienda":tien, "entity":productos, "pc":pc, "mac":mac, "arc":arc, "paginator":paginator})



def pedi(request, tienda_id):
    tien=tienda.objects.get(id= tienda_id)
    prod=producto.objects.filter(tienda_id= tienda_id, estatus= True)
    mac = prod.count()
    productos=producto.objects.filter(tienda_id= tienda_id, estatus= False)
    arc = productos.count()
    busqueda = request.GET.get('bus')
    if busqueda:
        pedidos = pedido.objects.filter(enviado=False)
        pedidos = pedidos.filter(id=int(busqueda))
    else:
        pedidos=pedido.objects.filter(local_id =tienda_id, enviado= False)         
   
    page = request.GET.get('page',1)
    pc = pedidos.count()

    try:
        paginator = Paginator(pedidos, 5)
        pedidos = paginator.page(page)
    except:
        raise Http404
    
    return render(request, "proyectoApp/pedidos.html", {"tienda":tien, "entity":pedidos, "paginator":paginator,"pc":pc, "mac":mac, "arc":arc})


    
    
def contacto(request):
    if request.method == 'POST':
        subject = "mensaje" + " " + request.POST.get('nombre')
        message = request.POST.get('email') + "\n" + request.POST.get('mensaje')
        email_from = "muestrastore@gmail.com"
        recipient=["muestrastore@gmail.com"]
        send_mail(subject, message, email_from, recipient)

        return render(request, "proyectoApp/gracias.html") 

    return render(request, "proyectoApp/contacto.html")

def editienda(request, tienda_id):
    tie = tienda.objects.get(id= tienda_id)

    if request.method == 'POST':
        tie.nombre = request.POST.get('nombre')
        tie.ubicacion = request.POST.get('ubicacion')
        tie.descripcion = request.POST.get('descripcion')
        tie.instagram_link = request.POST.get('insta')
        tie.facebook_link = request.POST.get('face')
        tie.whatsapp_link = request.POST.get('num')
        if request.FILES.get('perfil'):
            tie.foto_perfil = request.FILES.get('perfil')
        if request.FILES.get('fondo'):
            tie.foto_fondo = request.FILES.get('fondo')
        tie.save()
        return redirect('dashboard', tienda_id= tienda_id)    
    return render(request, "proyectoApp/editienda.html", {"tienda":tie})

def solicitud(request):
    if request.method == 'POST':
        subject = "Solicitud de:" + " " + request.POST.get('nombre')
        message = "Nombre tienda:  "+request.POST.get('nombret') + "\n" + "Email:  " +request.POST.get('email')+"\n"+"Instagram:  "+request.POST.get('insta')+"\n"+("Facebook:  ")+request.POST.get('face')+"\n"+("Categoria:  ")+request.POST.get('categoria')+"\n"+"\n"+request.POST.get('mensaje')
        email_from = "muestrastore@gmail.com"
        recipient=["muestrastore@gmail.com"]
        send_mail(subject, message, email_from, recipient)

        return render(request, "proyectoApp/graciast.html")
    return render(request, "proyectoApp/solicitud.html")

def modalel(request, producto_id):
    pro = producto.objects.get(id=producto_id)

    return render(request, "proyectoApp/modalel.html", {"producto":pro})

def modalpe(request, pedido_id):
    ped = pedido.objects.get(id=pedido_id)

    return render(request, "proyectoApp/modalpe.html", {"pedido":ped})

def registro(request):
    form = usuariof(data=request.POST)
    
    if request.method == 'POST':
        try:
            form.save()
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Bien hecho")  
            return redirect('/')
        except:
            messages.info(request, "Datos erroneos")
            return redirect('/registro')
    return render(request, "proyectoApp/registro.html",{"form":usuariof()})

def salir(request):

    logout(request)
    messages.success(request, "Saliste")

    return redirect('/entra')

def entra(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            clave = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=clave)
            if user is not None:
                login(request, user)
                messages.success(request, f"estas adentro {user.username}")
                return redirect('/')
            else:
                messages.info(request, "Datos incorrectos")
        else:
            messages.info(request, "Datos incorrectos")
    form = AuthenticationForm()
    return render(request, "proyectoApp/entra.html", {"form": form})