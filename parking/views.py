# Create your views here.

from .parking_logic import depositar_vehiculo
from .models import Ticket, Cobro, Abono, Cliente
from django.shortcuts import render
from django.utils import timezone
import decimal
import pytz
from datetime import datetime


def depositar_vehiculo_view(request):
    if request.method == 'POST':
        matricula = request.POST['matricula']
        tipo = request.POST['tipo']
        ticket = depositar_vehiculo(matricula, tipo)
        if ticket:
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
        plaza.estado = 'Libre'
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
            if plaza.estado == 'Libre':
                plaza.estado = 'Ocupado'
                plaza.save()
                ticket = Ticket(matricula=matricula, plaza=plaza, pin=abono.pin, fecha_entrada=datetime.now())
                ticket.save()
                return render(request, 'mensaje.html', {'mensaje': 'Vehículo depositado'})
            else:
                return render(request, 'mensaje2.html', {'mensaje': 'La plaza no está libre'})
        except Abono.DoesNotExist:
            return render(request, 'mensaje2.html', {'mensaje': 'DNI no válido'})
    else:
        return render(request, 'depositar_abonado.html')
