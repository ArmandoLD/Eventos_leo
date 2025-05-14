from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from .forms import LoginForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .forms import PerfilProveedorForm
from .forms import PerfilClienteForm
from .forms import ProductoForm
from .models import Producto
from .models import Reserva
from .models import Mensaje
from .models import Usuario, Mensaje






def inicio(request):
    return render(request, 'usuarios/inicio.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.tipo_usuario = form.cleaned_data['tipo_usuario'] 
            user.save() 

            subject = 'Registro exitoso'
            message = f'Te has registrado correctamente como {user.tipo_usuario.upper()} en nuestra plataforma.'
            send_mail(subject, message, None, [user.email], fail_silently=False)

            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})


def iniciar_sesion(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if username and password:
            usuario = authenticate(username=username, password=password)
            if usuario:
                login(request, usuario)

                if usuario.tipo_usuario == 'proveedor':
                    return redirect('panel_proveedor')
                else:  
                    return redirect('exploracion_productos')

            else:
                error = "Usuario o contraseña incorrectos"

    return render(request, 'usuarios/login.html', {'error': error})

@login_required
def bienvenida(request):
    return render(request, 'usuarios/bienvenida.html')

@login_required
def panel_proveedor(request):
    return render(request, 'usuarios/panel_proveedor.html')

@login_required
def mis_productos(request):
    productos = request.user.productos.all()  
    return render(request, 'usuarios/mis_productos.html', {'productos': productos})

@login_required
def reservas(request):
    reservas_pendientes = request.user.reservas.filter(estado='pendiente')  
    return render(request, 'usuarios/reservas.html', {'reservas': reservas_pendientes})

@login_required
def perfil_proveedor(request):
    usuario = request.user
    
    if request.method == 'POST':
        form = PerfilProveedorForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil_proveedor')

    else:
        form = PerfilProveedorForm(instance=usuario)

    return render(request, 'usuarios/perfil_proveedor.html', {'form': form})

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.proveedor = request.user  
            producto.save()
            return redirect('mis_productos') 
    else:
        form = ProductoForm()

    return render(request, 'usuarios/agregar_producto.html', {'form': form})

@login_required
def mis_productos(request):
    productos = Producto.objects.filter(proveedor=request.user)
    return render(request, 'usuarios/mis_productos.html', {'productos': productos})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, proveedor=request.user)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('mis_productos') 
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'usuarios/editar_producto.html', {'form': form, 'producto': producto})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, proveedor=request.user)

    if request.method == "POST":
        producto.delete()  
        return redirect('mis_productos')

    return render(request, 'usuarios/confirmar_eliminar.html', {'producto': producto})


@login_required
def exploracion_productos(request):
    productos = Producto.objects.all()

 
    categoria = request.GET.get('categoria')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    capacidad = request.GET.get('capacidad')


    if categoria and categoria != "todos":
        productos = productos.filter(categoria=categoria)
    
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    
    if capacidad:
        productos = productos.filter(capacidad__gte=capacidad)

    return render(request, 'usuarios/exploracion.html', {'productos': productos})

@login_required
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    proveedor = producto.proveedor  
    return render(request, 'usuarios/detalle_producto.html', {'producto': producto, 'proveedor': proveedor})

@login_required
def reservar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        reserva = Reserva.objects.create(producto=producto, cliente=request.user)
        return redirect('mis_reservas')

    return render(request, 'usuarios/detalle_producto.html', {'producto': producto})

@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(cliente=request.user)
    return render(request, 'usuarios/mis_reservas.html', {'reservas': reservas})

from .models import Reserva

@login_required
def reservar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        fecha = request.POST.get('fecha', None) 
        if fecha:
            Reserva.objects.create(producto=producto, cliente=request.user, fecha=fecha)
            return redirect('mis_reservas')

    return render(request, 'usuarios/detalle_producto.html', {'producto': producto})

@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(cliente=request.user)
    return render(request, 'usuarios/mis_reservas.html', {'reservas': reservas})

from django.core.mail import send_mail

@login_required
def gestionar_reservas(request):
    reservas_pendientes = Reserva.objects.filter(producto__proveedor=request.user, estado='pendiente')

    if request.method == 'POST':
        reserva_id = request.POST.get('reserva_id')
        accion = request.POST.get('accion')

        reserva = Reserva.objects.get(id=reserva_id)

        if accion == "aceptar":
            reserva.estado = "aceptada"  
            mensaje = f"Hola {reserva.cliente.username}, tu reserva para {reserva.producto.nombre} ha sido **ACEPTADA**."

        elif accion == "rechazar":
            mensaje = f"Hola {reserva.cliente.username}, lamentablemente tu reserva para {reserva.producto.nombre} ha sido **RECHAZADA**."
            reserva.delete()  

        else:
            return redirect('gestionar_reservas')

        reserva.save() 

        send_mail(
            subject="Estado de tu reserva",
            message=mensaje,
            from_email=None,  
            recipient_list=[reserva.cliente.email],
            fail_silently=False,
        )

        return redirect('gestionar_reservas')

    return render(request, 'usuarios/gestionar_reservas.html', {'reservas': reservas_pendientes})

@login_required
def perfil_cliente(request):
    usuario = request.user  

    if request.method == 'POST':
        form = PerfilClienteForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario.username = form.cleaned_data['username']
            usuario.email = form.cleaned_data['email']
            usuario.telefono = form.cleaned_data['telefono']
            usuario.save()
            return redirect('perfil_cliente')

    else:
        form = PerfilClienteForm(instance=usuario)

    return render(request, 'usuarios/perfil_cliente.html', {'form': form, 'usuario': usuario})

@login_required
def pago_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user)

    if request.method == "POST":
        
        reserva.estado = "pagado"
        reserva.save()
        return redirect('mis_reservas')

    return render(request, 'usuarios/pago_reserva.html', {'reserva': reserva})

@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user)

    
    mensaje = f"Hola {reserva.producto.proveedor.username}, el cliente {reserva.cliente.username} ha cancelado su reserva para {reserva.producto.nombre}."
    send_mail(
        subject="Reserva Cancelada",
        message=mensaje,
        from_email=None,  
        recipient_list=[reserva.producto.proveedor.email],
        fail_silently=False,
    )

    reserva.delete()  

    return redirect('mis_reservas')

@login_required
def chat(request, producto_id, cliente_id):
    producto = Producto.objects.filter(id=producto_id).first()
    cliente = Usuario.objects.filter(id=cliente_id).first()
    proveedor = producto.proveedor if producto else None

    if not producto or not cliente or not proveedor:
        return render(request, 'usuarios/error.html', {'mensaje': 'El producto o el cliente no existen.'})

    
    if request.user == proveedor:
        destinatario = cliente 
    elif request.user == cliente:
        destinatario = proveedor  
    else:
        return render(request, 'usuarios/error.html', {'mensaje': 'No tienes acceso a este chat.'})

    mensajes = Mensaje.objects.filter(producto=producto, remitente__in=[request.user, destinatario], destinatario__in=[request.user, destinatario]).order_by('fecha_envio')

    if request.method == "POST":
        contenido = request.POST.get("contenido")
        if contenido:
            Mensaje.objects.create(remitente=request.user, destinatario=destinatario, producto=producto, contenido=contenido)
            return redirect('chat', producto_id=producto.id, cliente_id=cliente.id)

    return render(request, 'usuarios/chat.html', {'producto': producto, 'mensajes': mensajes, 'proveedor': proveedor, 'cliente': cliente, 'usuario_actual': request.user})


@login_required
def mensajes_producto(request, producto_id):
    producto = Producto.objects.filter(id=producto_id, proveedor=request.user).first()

    if not producto:
        return render(request, 'usuarios/error.html', {'mensaje': 'El producto no existe o no te pertenece.'})

    chats = Mensaje.objects.filter(producto=producto).values_list('remitente', flat=True).distinct()
    clientes_chat = Usuario.objects.filter(id__in=list(chats))

    return render(request, 'usuarios/mensajes_producto.html', {'producto': producto, 'clientes_chat': clientes_chat})


@login_required
def mensajes(request):
    chats = Mensaje.objects.filter(destinatario=request.user).values_list('remitente', flat=True).distinct()
    usuarios_chat = Usuario.objects.filter(id__in=list(chats))

    return render(request, 'usuarios/mensajes.html', {'usuarios_chat': usuarios_chat})



