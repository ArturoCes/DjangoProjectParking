from django.db import models

from django.db.models import Sum

class Plaza(models.Model):
    ESTADO_OCUPADO = 'Ocupado'
    ESTADO_LIBRE = 'Libre'
    ESTADO_RESERVADO = 'Reservada'
    ESTADOS_CHOICES = (
        (ESTADO_OCUPADO, 'Ocupado'),
        (ESTADO_LIBRE, 'Libre'),
        (ESTADO_RESERVADO, 'Reservada'),
    )

    id = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    tipo = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default=ESTADO_LIBRE)
    tarifa_minuto = models.DecimalField(max_digits=5, decimal_places=2)


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=20)
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=20)
    num_tarjeta = models.CharField(max_length=20)

    TIPOS_ABONO = (
        ('Turismo', 'Turismo'),
        ('Moto', 'Moto'),
        ('PMR', 'PMR')
    )
    tipo_abono = models.CharField(max_length=20, choices=TIPOS_ABONO, default='Turismo')

    TIPOS_SUSCRIPCION = (
        ('Mensual', 'Mensual'),
        ('Trimestral', 'Trimestral'),
        ('Semestral', 'Semestral'),
        ('Anual', 'Anual'),
    )
    tipo_suscripcion = models.CharField(max_length=20, choices=TIPOS_SUSCRIPCION, default='Mensual')
    fecha_inicio_suscripcion = models.DateField()
    email = models.EmailField()


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    matricula = models.CharField(max_length=20)
    fecha_entrada = models.DateTimeField()
    plaza = models.ForeignKey(Plaza, on_delete=models.CASCADE)
    pin = models.CharField(max_length=6)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)


class Cobro(models.Model):
    id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    importe = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_pago = models.DateTimeField()


class Abono(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    plaza = models.ForeignKey(Plaza, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    pin = models.CharField(max_length=6)
