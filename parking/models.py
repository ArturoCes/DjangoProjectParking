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

    def __str__(self):
        txt = "{0}- Número de plaza: {1} / Tipo de plaza: {2} / Estado de la plaza: {3} / Tarifa por minuto: {4}"
        return txt.format(self.id, self.numero, self.tipo, self.estado, self.tarifa_minuto)


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=20, null=True, blank=True)
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=20, null=True, blank=True)
    num_tarjeta = models.CharField(max_length=20)
    TIPO_TURISMO = 'Turismo'
    TIPO_MOTO = 'Moto'
    TIPO_PMR = 'PMR'
    TIPOS_ABONO = (
        (TIPO_TURISMO, 'Turismo'),
        (TIPO_MOTO, 'Moto'),
        (TIPO_PMR, 'PMR')
    )
    tipo_abono = models.CharField(max_length=20, choices=TIPOS_ABONO, null= True)

    TIPOS_SUSCRIPCION = (
        ('Mensual', 'Mensual'),
        ('Trimestral', 'Trimestral'),
        ('Semestral', 'Semestral'),
        ('Anual', 'Anual'),
    )
    tipo_suscripcion = models.CharField(max_length=20, choices=TIPOS_SUSCRIPCION, default='Mensual')
    fecha_inicio_suscripcion = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        txt = "{0} Dni:  {1}, Nombre:  {2}, Apellidos:  {3}"
        return txt.format(self.id, self.dni, self.nombre, self.apellidos)


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    matricula = models.CharField(max_length=20)
    fecha_entrada = models.DateTimeField()
    fecha_salida = models.DateTimeField(null=True)
    plaza = models.ForeignKey(Plaza, on_delete=models.CASCADE)
    pin = models.CharField(max_length=6)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        txt = "{0} - Matricula :{1}/ Fecha de entrada: {2} / Plaza: {3}"
        return txt.format(self.id, self.matricula, self.fecha_entrada, self.plaza)


class Cobro(models.Model):
    id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    importe = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_pago = models.DateTimeField()

    def __str__(self):
        txt = "{0} / Ticket:  {1}  / Importe: {2} / Fecha de Pago: {3}"
        return txt.format(self.id, self.ticket, self.importe, self.fecha_pago)


class Abono(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
    plaza = models.ForeignKey(Plaza, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    pin = models.CharField(max_length=6)

    def __str__(self):
        txt = "{0} / Cliente: {1} / Ticket: {2}/Plaza:{3} /Fecha de inicio: {4} / Fecha de vencimiento: {5} / Pin: {6}"
        return txt.format(self.id, self.cliente, self.ticket, self.plaza, self.fecha_inicio, self.fecha_vencimiento,
                          self.pin)
