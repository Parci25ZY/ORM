from django.db import models

class Cargo(models.Model):
    nombre_cargo = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_cargo

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='empleados')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Prestamo(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_prestamo = models.DateField()
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='prestamos')
    numero_cuotas = models.IntegerField()
    cuota = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Préstamo ID {self.id} - {self.monto}"

class Pago(models.Model):
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name='pagos')

    def __str__(self):
        return f"Pago ID {self.id} - {self.monto_pago}"
