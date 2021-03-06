from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import usuariof
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from productosApp.models import producto, categoria, tienda, pedido, favorito
from django.core.paginator import Paginator
from django.http import Http404
from django.core.mail import send_mail
from django.contrib.auth.models import Group

def materiales(request):
    if request.method == 'POST':
       m1 = [77000,460,7.8,10000,"ASTM A913"]
       m2 = [75000,530,8,17000,"AISI 302"]
       m3 = [28000,510,2.81,28000,"7075 T6"]
       m4 = [78000,772,7.85,19000,"AISI 1095"]
       m = [m1,m2,m3,m4]
       a1=int(request.POST.get('a1'))
       t1=int(request.POST.get('t1'))
       a2=int(request.POST.get('a2'))
       t2=int(request.POST.get('t2'))
       a3=int(request.POST.get('a3'))
       t3=int(request.POST.get('t3'))
       d1=int(request.POST.get('d1'))
       g1=int(request.POST.get('g1'))
       d2=int(request.POST.get('d2'))
       g2=int(request.POST.get('g2'))
       d3=int(request.POST.get('d3'))
       g3=int(request.POST.get('g3'))
       n1=int(request.POST.get('m1'))
       n2=int(request.POST.get('m2'))
       n3=int(request.POST.get('m3'))
       mp1 = m[n1-1]
       l1=((a1*(pi/180))/t1)*(mp1[0]*(pi/32)*((d1**4)-(d1-(2*g1))**4))
       
       tl1=((a2-a1)*pi*mp1[0]*(pi/32)*((d1**4)-(d1-(2*g1))**4))/(180*l1)
       tl2=t2-tl1
       mp2 = m[n2-1] 
       l2=(((a2-a1)*(pi/180))/tl2)*(mp2[0]*(pi/32)*((d2**4)-(d2-(2*g2))**4))
       
       tl1=((a3-a2)*pi*mp1[0]*(pi/32)*((d1**4)-(d1-(2*g1))**4))/(180*l1)
       tl2=((a3-a2)*pi*mp2[0]*(pi/32)*((d2**4)-(d2-(2*g2))**4))/(180*l2)
       tl3=t3-(tl1+tl2)
       mp3 = m[n3-1]
       l3=(((a3-a2)*(pi/180))/tl3)*(mp3[0]*(pi/32)*((d3**4)-(d3-(2*g3))**4))
       
       ar1=(pi*((d1/2)**2))-(pi*(((d1/2)-g1)**2))
       vl1=(ar1*l1)/1000
       p1=((vl1*mp1[2])/1000)*mp1[3]
       ar2=(pi*((d2/2)**2))-(pi*(((d2/2)-g2)**2))
       vl2=(ar2*l2)/1000
       p2=((vl2*mp2[2])/1000)*mp2[3]
       ar3=(pi*((d3/2)**2))-(pi*(((d3/2)-g3)**2))
       vl3=(ar3*l3)/1000
       p3=((vl3*mp3[2])/1000)*mp3[3]
       l3="{0:.3f}".format(l3)
       l2="{0:.3f}".format(l2)
       l1="{0:.3f}".format(l1)
       pt="{0:.3f}".format(p1+p2+p3)
       
       fs1="{0:.3f}".format((0.577*mp1[1])/((16*tl1*d1)/(pi*((d1**4)-(d1-(2*g1))**4))))
       fs2="{0:.3f}".format((0.577*mp2[1])/((16*tl2*d2)/(pi*((d2**4)-(d2-(2*g2))**4))))
       fs3="{0:.3f}".format((0.577*mp3[1])/((16*tl3*d3)/(pi*((d3**4)-(d3-(2*g3))**4))))
       fst=max([fs1,fs2,fs3])

       return render(request, "proyectoApp/mreport.html", {"a1":a1,"a2":a2,"a3":a3,"t1":t1,"t2":t2,"t3":t3,"l1":l1,"l2":l2,"l3":l3,"d1":d1,"d2":d2,"d3":d3,"g1":g1,"g2":g2,"g3":g3,"pt":pt,"fs":fst,"m1":mp1[4],"m2":mp2[4],"m3":mp3[4]}) 
    return render(request, "proyectoApp/materiales.html")


def infor(request):
    
    return render(request, "proyectoApp/tuto.html")

def error404(request):
    return render(request, "proyectoApp/404.html")

def error(request, exception):
    return render(request, "proyectoApp/404.html")


def home(request):
    categorias=categoria.objects.all()
    productos=producto.objects.filter(estatus= True)
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
            paginator = Paginator(tien, 12)
            tien = paginator.page(page)
    except:
        raise Http404
    return render(request, "proyectoApp/tiendas.html", {"entity":tien,"paginator":paginator})

def local(request, tienda_url):
    dis = request.GET.get('dis')
    if dis:
        if dis == "a":
            request.session['distro'] = 0
        if dis == "b":
            request.session['distro'] = 1
    distro = request.session.get('distro',0)    
    tien=tienda.objects.get(url= tienda_url)
    categorias=categoria.objects.all()
    productos=producto.objects.filter(tienda_id= tien.id)
    orden = request.GET.get('ord')
    page = request.GET.get('page',1)
    if orden:
        if orden == "reciente":
            productos = productos.order_by('-created')
        elif orden == "menor":
            productos = productos.order_by('precio')
        elif orden == "mayor":
            productos = productos.order_by('-precio')  
    
    try:
            paginator = Paginator(productos, 12)
            productos = paginator.page(page)
    except:
        raise Http404 

    return render(request, "proyectoApp/tienda.html",{"distro":distro,"paginator":paginator,"tienda":tien, "categorias": categorias, "entity":productos,"ord":orden})

def creatienda(request):
    
        
    categorias = categoria.objects.all()
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
        ti.url = request.POST.get('url')
        if request.POST.get('otra'):
            ti.categoria = request.POST.get('otra')
        else:
            ti.categoria = request.POST.get('cate')
        us = User()
        us.id = int(request.POST.get('usid'))
        ti.autor = us
        ti.save()
        gru = Group.objects.get(name='Vendedor')
        gru.user_set.add(request.user)
        gru.save()
        messages.success(request, "Tienda Creada")
        return redirect('mistiendas', us_id=request.user.id)
    return render(request, "proyectoApp/tform.html",{"categorias":categorias})
def tiendash(request, us_id):
    tien=tienda.objects.filter(autor_id= us_id)
    mens = request.session.get('men2',0)
    men = 0
    if mens == 0:
       
       request.session['men2'] = 1
       men = 1
    return render(request, "proyectoApp/tiendash.html", {"men1":men,"tiendas":tien})


     
def dashboard(request, tienda_id):
    tien=tienda.objects.get(id= tienda_id)
    mens = request.session.get('men0',0)
    men = 0
    if mens == 0:
       
       request.session['men0'] = 1
       men = 1
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
    return render(request, "proyectoApp/dashboard.html", {"men0": men,"tienda":tien, "entity":productos, "pc":pc, "mac":mac, "arc":arc, "paginator":paginator})

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

def ipost(request, tienda_id):
    tien = tienda.objects.get(id=tienda_id)
    prod=producto.objects.filter(tienda_id= tienda_id, estatus= True)
    mac = prod.count()
    productos=producto.objects.filter(tienda_id= tienda_id, estatus= False)
    arc = productos.count()
    pedidos=pedido.objects.filter(local_id =tienda_id, enviado= False)         
    pc = pedidos.count()
    if request.method == 'POST':
        if request.POST.get('insta'):
            if request.POST.get('insta').find("?") == -1:
               tien.instagram_post = request.POST.get('insta')
            else:
                nu = request.POST.get('insta').find("?")
                ins = request.POST.get('insta')[0:nu]
                
                tien.instagram_post = ins
        if request.POST.get('insta2'):
            if request.POST.get('insta2').find("?") == -1:
               tien.facebook_post = request.POST.get('insta2')
            else:
                nu = request.POST.get('insta2').find("?")
                ins = request.POST.get('insta2')[0:nu]
                
                tien.facebook_post = ins
        tien.save()
        messages.success(request, "Post actualizado")
    return render(request, "proyectoApp/ipost.html",{"tienda":tien, "pc":pc, "mac":mac, "arc":arc})
    

def pedi(request, tienda_id):
    tien=tienda.objects.get(id= tienda_id)
    prod=producto.objects.filter(tienda_id= tienda_id, estatus= True)
    mac = prod.count()
    productos=producto.objects.filter(tienda_id= tienda_id, estatus= False)
    arc = productos.count()
    busqueda = request.GET.get('bus')
    if busqueda:
        pedidos = pedido.objects.filter(local_id =tienda_id,enviado=False)
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

def elpe(request, pedido_id, tienda_id):
    tie = tienda.objects.get(id=tienda_id)
    ped = pedido.objects.get(id=pedido_id)
    return render(request, "proyectoApp/elpe.html", {"pedido":ped,"tienda":tie})
def elimipe(request, pedido_id, tienda_id):

    ped = pedido.objects.get(id=pedido_id)
    ped.delete()
    messages.success(request, "Pedido eliminado")
    ted = tienda_id
    return redirect('pedidos', tienda_id=ted)

    
def contacto(request):
    if request.method == 'POST':
        subject = "Mensaje de" + " " + request.POST.get('nombre')
        message = request.POST.get('mensaje') + "\n" + "\n" + "@Email:  "+ request.POST.get('email')
        email_from = "pedidos@muestra.store"
        recipient=["gerencia@muestra.store"]
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
        tie.url = request.POST.get('url')
        if request.FILES.get('perfil'):
            tie.foto_perfil = request.FILES.get('perfil')
        if request.FILES.get('fondo'):
            tie.foto_fondo = request.FILES.get('fondo')
        tie.save()
        messages.success(request, "Información actualizada")
        return redirect('dashboard', tienda_id= tienda_id)    
    return render(request, "proyectoApp/editienda.html", {"tienda":tie})

def solicitud(request):
    if request.method == 'POST':
        subject = "Solicitud de:" + " " + request.POST.get('nombre')
        message = "Nombre tienda:  "+request.POST.get('nombret') + "\n" + "Email:  " +request.POST.get('email')+"\n"+"Instagram:  "+request.POST.get('insta')+"\n"+("Facebook:  ")+request.POST.get('face')+"\n"+("Categoria:  ")+request.POST.get('categoria')+"\n"+"\n"+request.POST.get('mensaje')
        email_from = "pedidos@muestra.store"
        recipient=["gerencia@muestra.store"]
        send_mail(subject, message, email_from, recipient)

        return render(request, "proyectoApp/graciast.html")
    return render(request, "proyectoApp/solicitud.html")

def modalel(request, producto_id):
    pro = producto.objects.get(id=producto_id)

    return render(request, "proyectoApp/modalel.html", {"producto":pro})

def modalme(request, producto_id, tienda_id):
    return render(request, "proyectoApp/modalme.html",{"pro":producto_id,"tie":tienda_id})

def modalfa(request, producto_id):
    return render(request, "proyectoApp/modalfa.html",{"pro":producto_id})

def modalpe(request, pedido_id):
    ped = pedido.objects.get(id=pedido_id)

    return render(request, "proyectoApp/modalpe.html", {"pedido":ped})

def terminos(request):
    return render(request, "proyectoApp/terminos.html")

def galleta(request):
    return render(request, "proyectoApp/galleta.html")

def privacidad(request):
    return render(request, "proyectoApp/privacidad.html")



def dashcliente(request):
    page = request.GET.get('page',1)
    pedidos = pedido.objects.filter(cliente_id=request.user.id)
    pc = pedidos.count()
    favoritos = favorito.objects.filter(cliente_id=request.user.id)
    pf = favoritos.count()
    try:
        paginator = Paginator(pedidos, 7)
        pedidos = paginator.page(page)
    except:
        raise Http404
    return render(request, "proyectoApp/dashcliente.html",{"pc":pc,"pf":pf,"entity":pedidos,"paginator":paginator})

def favoritos(request):
    page = request.GET.get('page',1)
    favoritos = favorito.objects.filter(cliente_id=request.user.id)
    pf = favoritos.count()
    pedidos = pedido.objects.filter(cliente_id=request.user.id)
    pc = pedidos.count()
    try:
        paginator = Paginator(favoritos, 7)
        favoritos = paginator.page(page)
    except:
        raise Http404
    return render(request, "proyectoApp/favoritos.html",{"pc":pc,"pf":pf,"entity":favoritos,"paginator":paginator})

def registro(request):
    form = usuariof(data=request.POST)
    
    if request.method == 'POST':
        try:
            form.save()
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Bien hecho")
            if request.GET.get('sig'):
                return redirect('/nuevatienda')
            else:
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
                if request.GET.get('pr'):
                    if request.GET.get('sig'):
                        return redirect('pedido', tienda_id=request.GET.get('sig'), producto_id=request.GET.get('pr') )
                    elif request.GET.get('fav'):
                        return redirect('favorit', producto_id=request.GET.get('pr'))
                    else:
                        return redirect('solo', producto_id=request.GET.get('pr'))               
                else:
                    return redirect('/')
            else:
                messages.info(request, "Datos incorrectos")
        else:
            messages.info(request, "Datos incorrectos")
    form = AuthenticationForm()
    return render(request, "proyectoApp/entra.html", {"form": form})
