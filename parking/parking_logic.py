import datetime

import uuid
from datetime import datetime
from .models import *
from .forms import CrearAbonoForm
import pytz
from django.utils.timezone import make_aware


def generar_pin():
    return str(uuid.uuid4().int)[:6]


def depositar_vehiculo(matricula, tipo):
    # Verifica si la matrícula ingresada ya está en uso
    if Ticket.objects.filter(matricula=matricula).exists():
        print("La matrícula ingresada ya está en uso.")
        return None

    plaza_asignada = None
    plazas_libres = Plaza.objects.filter(estado='Libre', tipo=tipo)

    if plazas_libres.exists():
        plaza_asignada = plazas_libres.first()
        plaza_asignada.estado = 'Ocupada'
        plaza_asignada.save()
    else:
        print("Lo siento, no hay plazas libres disponibles para ese tipo de vehículo.")
        return None

    pin = generar_pin()  # Genera un número aleatorio de 6 dígitos
    ticket = Ticket.objects.create(matricula=matricula, fecha_entrada=datetime.now(), plaza=plaza_asignada, pin=pin)
    print(
        "Ticket generado: Matrícula - {}; Fecha de entrada - {}; Plaza asignada - {}; Pin - {}".format(ticket.matricula,
                                                                                                       ticket.fecha_entrada,
                                                                                                       ticket.plaza.numero,
                                                                                                       ticket.pin))
    return ticket


# def crear_plazas_turismo():
#     tipos = ['Turismo']
#     for i in range(1, 71):
#         for tipo in tipos:
#             plaza = Plaza(numero=i, tipo=tipo, estado='Libre', tarifa_minuto=0.12)
#             plaza.save()
#     print("Plazas creadas correctamente.")
#
#
# crear_plazas_turismo()
#
#
# def crear_plazas_moto():
#     tipos = ['Moto']
#     for i in range(71, 85):
#         for tipo in tipos:
#             plaza = Plaza(numero=i, tipo=tipo, estado='Libre', tarifa_minuto=0.10)
#             plaza.save()
#     print("Plazas creadas correctamente.")
#
#
# crear_plazas_moto()
#
#
# def crear_plazas_pmr():
#     tipos = ['PMR']
#     for i in range(86, 100):
#         for tipo in tipos:
#             plaza = Plaza(numero=i, tipo=tipo, estado='Libre', tarifa_minuto=0.08)
#             plaza.save()
#     print("Plazas creadas correctamente.")
#
#
# crear_plazas_pmr()

def cobros_entre_fechas(request):
    return render(request, 'mostrar_cobros.html')


def retirar_vehiculo(matricula, plaza_id, pin):
    try:
        ticket = Ticket.objects.get(matricula=matricula, plaza_id=plaza_id, pin=pin)
    except Ticket.DoesNotExist:
        return False, "Ticket no válido"
    fecha_entrada = ticket.fecha_entrada.replace(tzinfo=None)
    diferencia = datetime.now() - fecha_entrada
    minutos_estacionado = int(diferencia.total_seconds() / 60)
    tarifa = ticket.plaza.tarifa_minuto
    importe = minutos_estacionado * tarifa
    fecha_guardar = datetime.now()
    cobro = Cobro(ticket=ticket, importe=importe, fecha_pago=fecha_guardar)
    cobro.save()
    plaza = ticket.plaza
    plaza.estado = plaza.ESTADO_LIBRE
    plaza.save()

    return True, cobro


def depositar_abonado(dni, matricula):
    try:
        abono = Abono.objects.get(cliente__dni=dni, matricula=matricula)
        plaza = abono.plaza
        if plaza.estado == Plaza.ESTADO_LIBRE:
            plaza.estado = Plaza.ESTADO_OCUPADO
            plaza.save()
            ticket = Ticket(matricula=matricula, plaza=plaza, pin=abono.pin, fecha_entrada=datetime.now())
            ticket.save()
            return True, "Vehículo depositado"
        else:
            return False, "La plaza no está libre"
    except Abono.DoesNotExist:
        return False, "DNI o matrícula no válido"


def facturacion(fecha_inicio, fecha_fin):
    tickets = Ticket.objects.filter(fecha_entrada__range=(fecha_inicio, fecha_fin))
    return tickets


def cobros_rango(fecha_inicio, fecha_fin):
    return Cobro.objects.filter(fecha_pago__range=(fecha_inicio, fecha_fin))


def depositar_abonado(dni, matricula):
    try:
        cliente = Cliente.objects.get(dni=dni)
        abono = Abono.objects.get(cliente=cliente, ticket__matricula=matricula)
        if abono.fecha_vencimiento > datetime.now():
            plaza = abono.plaza
            if plaza.estado == Plaza.ESTADO_RESERVADO:
                plaza.estado = Plaza.ESTADO_OCUPADO
                plaza.save()
                ticket = Ticket(matricula=matricula, plaza=plaza, pin=abono.pin, fecha_entrada=datetime.now())
                ticket.save()
                return "Vehículo depositado"
            else:
                return "La plaza no está libre"
        else:
            return "Suscripción vencida"
    except Cliente.DoesNotExist:
        return "Cliente no encontrado"
    except Abono.DoesNotExist:
        return "Abono no encontrado"


def retirar_abonado(dni, id_plaza, pin):
    cliente = Cliente.objects.get(dni=dni)
    abono = Abono.objects.get(cliente=cliente)
    if abono.plaza.id != id_plaza or abono.pin != pin:
        return 'La información ingresada es incorrecta'
    abono.plaza.estado = Plaza.ESTADO_LIBRE
    abono.plaza.save()
    abono.delete()
    return 'Abono retirado exitosamente'


def crear_abono(nombre, apellidos, dni, telefono, email, matricula, tipo_suscripcion, monto_pagar):
    cliente = Cliente.objects.create(nombre=nombre, apellidos=apellidos, dni=dni, telefono=telefono, email=email)
    pin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    plaza = Plaza.objects.filter(estado=Plaza.ESTADO_LIBRE).first()
    if not plaza:
        raise Exception("No hay plazas libres disponibles")
    plaza.estado = Plaza.ESTADO_OCUPADO
    plaza.save()
    abono = Abono.objects.create(cliente=cliente, pin=pin, plaza=plaza, fecha_inicio=datetime.now())
    Ticket.objects.create(cliente=cliente, matricula=matricula, plaza=plaza, pin=pin, fecha_entrada=datetime.now(),
                          cobro=abono)
