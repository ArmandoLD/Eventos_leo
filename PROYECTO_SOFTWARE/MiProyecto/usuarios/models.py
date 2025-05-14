from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    tipo_usuario = models.CharField(max_length=20, choices=[
        ('cliente', 'Cliente'),
        ('proveedor', 'Proveedor'),
    ], default='cliente')

    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
    
class Producto(models.Model):
    CATEGORIAS = [
        ('local', 'Local'),
        ('entretenimiento', 'Entretenimiento'),
        ('comida', 'Comida'),
    ]

    proveedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    descripcion = models.TextField()
    capacidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} ({self.proveedor.username})"
    

class Reserva(models.Model):
    ESTADOS_RESERVA = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS_RESERVA, default='pendiente')

    def __str__(self):
        return f"Reserva de {self.producto.nombre} por {self.cliente.username} ({self.estado})"
    

class Mensaje(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="mensajes_enviados")
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="mensajes_recibidos")
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.remitente.username} a {self.destinatario.username} sobre {self.producto.nombre}"






