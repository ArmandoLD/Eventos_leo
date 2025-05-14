from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    inicio, registro, iniciar_sesion, bienvenida, panel_proveedor, mis_productos, reservas, perfil_proveedor,
    agregar_producto, editar_producto, eliminar_producto, exploracion_productos, detalle_producto, reservar_producto,
    mis_reservas, gestionar_reservas, perfil_cliente, pago_reserva, cancelar_reserva, chat, mensajes_producto
)

urlpatterns = [
    # Autenticación
    path('', inicio, name='inicio'),
    path('registro/', registro, name='registro'),
    path('login/', iniciar_sesion, name='login'),
    path('bienvenida/', bienvenida, name='bienvenida'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),

    # Proveedor
    path('panel-proveedor/', panel_proveedor, name='panel_proveedor'),
    path('productos/mis/', mis_productos, name='mis_productos'),
    path('productos/agregar/', agregar_producto, name='agregar_producto'),
    path('productos/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),

    # Exploración y detalles de productos
    path('productos/explorar/', exploracion_productos, name='exploracion_productos'),
    path('productos/detalle/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('productos/reservar/<int:producto_id>/', reservar_producto, name='reservar_producto'),

    # Reservas
    path('reservas/', reservas, name='reservas'),
    path('reservas/mis/', mis_reservas, name='mis_reservas'),
    path('reservas/gestionar/', gestionar_reservas, name='gestionar_reservas'),
    path('reservas/pago/<int:reserva_id>/', pago_reserva, name='pago_reserva'),
    path('reservas/cancelar/<int:reserva_id>/', cancelar_reserva, name='cancelar_reserva'),

    # Perfiles
    path('perfil/proveedor/', perfil_proveedor, name='perfil_proveedor'),
    path('perfil/cliente/', perfil_cliente, name='perfil_cliente'),

    # Mensajes y chat
    path('mensajes/producto/<int:producto_id>/', mensajes_producto, name='mensajes_producto'),
    path('chat/<int:producto_id>/<int:cliente_id>/', chat, name='chat'),
]