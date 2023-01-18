# Create your views here.

from .parking_logic import *
from django.db.models import Sum

from .models import *
from django.shortcuts import render
from django.utils import timezone
import decimal
import pytz
from datetime import datetime

def administrar_plazas_view(request):
    plazas = Plaza.objects.all()
    context = {'plazas': plazas}
    return render(request, 'administrar_plazas.html', context)
class TicketList:
    def __init__(self):
        self.tickets = []

    def add_ticket(self, matricula, fecha_entrada, fecha_salida=None):
        ticket = {'matricula': matricula, 'fecha_entrada': fecha_entrada, 'fecha_salida': fecha_salida}
        self.tickets.append(ticket)

def main_view(request):
    return render(request, 'main.html')
def facturacion_view(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        tickets = facturacion(fecha_inicio, fecha_fin)
        context = {'tickets': tickets}
        return render(request, 'facturacion.html', context)
    else:
        return render(request, 'facturacion_form.html')


def depositar_vehiculo_view(request):
    ticket_list = TicketList()
    if request.method == 'POST':
        matricula = request.POST['matricula']
        tipo = request.POST['tipo']
        ticket = depositar_vehiculo(matricula, tipo)
        if ticket:
            ticket_list.add_ticket(matricula, ticket.fecha_entrada)
            context = {'ticket': ticket}
            return render(request, 'ticket.html', context)
        else:
            context = {'mensaje': 'Lo siento, no hay plazas libres disponibles para ese tipo de vehículo.'}
            return render(request, 'mensaje.html', context)
    else:
        return render(request, 'depositar_vehiculo.html')


def retirar_vehiculo_view(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        plaza_id = request.POST.get('id')
        pin = request.POST.get('pin')
        try:
            ticket = Ticket.objects.get(matricula=matricula, plaza_id=plaza_id, pin=pin)
        except Ticket.DoesNotExist:
            return render(request, 'mensaje2.html', {'mensaje': 'Ticket no válido'})
        # calcular coste
        fecha_entrada = ticket.fecha_entrada.replace(tzinfo=pytz.UTC)
        tiempo_estacionado = datetime.now(pytz.UTC) - fecha_entrada
        importe = decimal.Decimal(tiempo_estacionado.seconds) / 60 * ticket.plaza.tarifa_minuto
        importe = importe.quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_HALF_UP)

        cobro = Cobro(ticket=ticket, importe=importe, fecha_pago=datetime.now())
        cobro.save()

        # actualizar plaza
        plaza = ticket.plaza
        plaza.estado = plaza.ESTADO_LIBRE
        plaza.save()

        # eliminar ticket
        ticket.delete()
        return render(request, 'ticket1.html', {'cobro': cobro})
    else:
        return render(request, 'retirar_vehiculo.html')


def depositar_abonado_view(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        dni = request.POST.get('dni')
        try:
            abono = Abono.objects.get(cliente__dni=dni)
            plaza = abono.plaza
            if plaza.estado == Plaza.ESTADO_LIBRE:
                plaza.estado = Plaza.ESTADO_OCUPADO
                plaza.save()
                ticket = Ticket(matricula=matricula, plaza=plaza, pin=abono.pin, fecha_entrada=datetime.now())
                ticket.save()
                return render(request, 'mensaje.html', {'mensaje': 'Vehículo depositado'})
            else:
                return render(request, 'mensaje2.html', {'mensaje': 'La plaza no está libre'})
        except Abono.DoesNotExist:
            return render(request, 'mensaje4.html', {'mensaje': 'DNI no válido'})
    else:
        return render(request, 'depositar_abonado.html')


def retirar_abonado_view(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        plaza_id = request.POST.get('id')
        pin = request.POST.get('pin')
        try:
            ticket = Ticket.objects.get(matricula=matricula, plaza_id=plaza_id, pin=pin)
        except Ticket.DoesNotExist:
            return render(request, 'mensaje2.html', {'mensaje': 'Ticket no válido'})

        # actualizar plaza
        plaza = ticket.plaza
        plaza.estado = plaza.ESTADO_RESERVADO
        plaza.save()
        return render(request, 'mensaje.html', {'mensaje': 'Vehículo retirado'})
    else:
        return render(request, 'retirar_abonado.html')
