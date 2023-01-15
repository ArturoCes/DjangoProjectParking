import datetime
from .models import Cliente, Plaza,Abono,Ticket,Cobro
import uuid


def generate_pin():
         return str(uuid.uuid4().int)[:6]

def generar_ticket(cls, matricula, plaza_id):
        plaza = Plaza.objects.get(pk=plaza_id)
        ticket = cls(matricula=matricula, fecha_entrada=datetime.timezone.now(), plaza=plaza, pin=generate_pin())
        ticket.save()
        return ticket
