# Create your views here.

from .parking_logic import *
from .models import *
from django.shortcuts import render
from django.utils import timezone
import decimal
import pytz
from datetime import datetime
from .forms import CrearAbonoForm


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

def mostrar_cobros_view(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        cobros = Cobro.objects.filter(fecha_pago__range=(fecha_inicio, fecha_fin))
        return render(request, 'mostrar_cobros.html', {'cobros': cobros})
    else:
        return render(request, 'buscar_cobros.html')

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
        result, mensaje = retirar_vehiculo(matricula, plaza_id, pin)

        if result:
            return render(request, 'ticket1.html', {'cobro': mensaje})
        else:
            return render(request, 'mensaje.html', {'mensaje': mensaje})
    else:
        return render(request, 'retirar_vehiculo.html')


def depositar_abonado_view(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        matricula = request.POST.get('matricula')
        try:
            cliente = Cliente.objects.get(dni=dni)
            plaza = Plaza.objects.get(ticket__matricula=matricula)
            if plaza.ticket_set.filter(matricula=matricula, cliente=cliente).exists():
                if plaza.estado == Plaza.ESTADO_LIBRE or Plaza.ESTADO_RESERVADO:
                    plaza.estado = Plaza.ESTADO_OCUPADO
                    plaza.save()
                    ticket = Ticket(matricula=matricula, plaza=plaza, pin=generar_pin(), fecha_entrada=datetime.now())
                    ticket.save()
                    context = {'ticket': ticket}
                    return render(request, 'ticket.html', context)
                else:
                    return render(request, 'mensaje.html', {'mensaje': 'La plaza no está libre'})
            else:
                return render(request, 'mensaje.html', {'mensaje': 'La plaza no esta asignada a este cliente'})
        except Cliente.DoesNotExist:
            return render(request, 'mensaje.html', {'mensaje': 'DNI no válido'})
        except Plaza.DoesNotExist:
            return render(request, 'mensaje.html', {'mensaje': 'Matricula no válida'})
    else:
        return render(request, 'depositar_abonado.html')


def plazas_view(request):
    plazas = Plaza.objects.all()
    return render(request, 'plazas.html', {'plazas': plazas})


def retirar_abonado_view(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        matricula = request.POST.get('matricula')
        pin = request.POST.get('pin')
        try:
            cliente = Cliente.objects.get(dni=dni)
            plaza = Plaza.objects.get(ticket__matricula=matricula, ticket__cliente=cliente)
            if plaza.ticket_set.filter(matricula=matricula, cliente=cliente).exists():
                if plaza.estado == Plaza.ESTADO_OCUPADO:
                    plaza.estado = Plaza.ESTADO_LIBRE
                    plaza.save()
                    return render(request, 'mensajeExitoso.html', {'mensaje': 'Vehículo depositado'})
                else:
                    return render(request, 'mensaje.html', {'mensaje': 'La plaza no está libre'})
            else:
                return render(request, 'mensaje.html', {'mensaje': 'La plaza no esta asignada a este cliente'})
        except Cliente.DoesNotExist:
            return render(request, 'mensaje.html', {'mensaje': 'DNI no válido'})
        except Plaza.DoesNotExist:
            return render(request, 'mensaje.html', {'mensaje': 'Matricula no válida'})
    else:
        return render(request, 'retirar_abonado.html')


def crear_abono_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        dni = request.POST.get('dni')
        email = request.POST.get('email')
        matricula = request.POST.get('matricula')
        tipo_suscripcion = request.POST.get('tipo_suscripcion')
        tipo_abono = request.POST.get('tipo_abono')
        cliente = Cliente(nombre=nombre, apellidos=apellidos, dni=dni, email=email)
        cliente.save()
        plaza = Plaza.objects.filter(estado=Plaza.ESTADO_LIBRE).first()
        plaza.estado = Plaza.ESTADO_RESERVADO
        plaza.save()
        pin = generar_pin()
        abono = Abono(cliente=cliente, plaza=plaza, pin=pin)
        abono.save()
        ticket = Ticket(cliente=cliente, matricula=matricula, plaza=plaza, pin=abono.pin, fecha_entrada=datetime.now())
        ticket.save()
        return render(request, 'mensajeExitoso.html', {'mensaje': 'Abono creado exitosamente'})
    else:
        return render(request, 'crear_abono.html')
