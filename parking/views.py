# Create your views here.
from django.shortcuts import render
from .parking_logic import depositar_vehiculo
from datetime import datetime
from .models import Ticket, Cobro


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
            return render(request, 'mensaje.html', {'mensaje': 'Ticket no válido'})
        # calcular coste
        importe = (datetime.now() - ticket.fecha_entrada).seconds / 60 * ticket.plaza.tarifa_minuto
        cobro = Cobro(ticket=ticket, importe=importe, fecha_pago=datetime.now())
        cobro.save()
        # actualizar plaza
        plaza = ticket.plaza
        plaza.estado = 'Libre'
        plaza.save()
        # eliminar ticket
        ticket.delete()
        return render(request, 'ticket.html', {'cobro': cobro})
    else:
        return render(request, 'retirar_vehiculo.html')


