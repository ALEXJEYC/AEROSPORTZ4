from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    descripcion = models.CharField(max_length=200, null=False)

    def __str__(self) -> str:
        return f"Id: {self.pk} | Descripcion: {self.descripcion}"


class Producto(models.Model):
    titulo = models.CharField(max_length=50, null=False)
    imagen = models.ImageField(upload_to='image', null=True)
    descripcion = models.CharField(max_length=200, null=False)
    precio = models.DecimalField(null=False, max_digits=10, decimal_places=3)
    # Relación con el modelo Categoria
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='productos')

    def __str__(self) -> str:
        return f"Id: {self.pk} | Titulo: {self.titulo} | Imagen: {self.imagen} | Descripcion: {self.descripcion} | Precio: {self.precio} || Categoria_id: {self.categoria.id} "
    
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carrito")
    total = models.DecimalField(null=False, max_digits=10, decimal_places=3)

    def __str__(self) -> str:
        return f"Id: {self.pk} | Usuario_id: {self.usuario.id} | Usuario: {self.usuario.username} | Total: {self.total}"
    
    def calcular_total(self):
        items = self.items.all()  # Obtener todos los items del carrito
        total = sum(item.producto.precio for item in items)  # Sumar los precios de los productos
        self.total = total
        self.save()

class Carrito_item(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Id: {self.pk} | Producto: {self.producto.titulo} | Cantidad: {self.cantidad}"


class Boleta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boletas')
    total = models.DecimalField(max_digits=10, decimal_places=3)
    fecha_de_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Id: {self.pk} | Usuario: {self.usuario.username} | Total: {self.total}"


class DetalleBoleta(models.Model):
    boleta = models.ForeignKey('Boleta', on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, related_name='detalles')
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Id: {self.pk} | Boleta: {self.boleta.pk} | Producto: {self.producto.titulo} | Cantidad: {self.cantidad} | Fecha: {self.fecha}"