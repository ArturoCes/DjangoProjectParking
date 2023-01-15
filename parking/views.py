from django.shortcuts import render

# Create your views here.
from .models import Ticket


def generar_ticket_view(request):
    if request.method == 'POST':
        matricula = request.POST['matricula']
        tipo_vehiculo = request.POST['tipo_vehiculo']
        plaza_id = request.POST['plaza_id']
        ticket = Ticket.generar_ticket(matricula, tipo_vehiculo, plaza_id)
        return render(request, 'ticket.html', {'ticket': ticket})
    return render(request, 'generar_ticket.html')
