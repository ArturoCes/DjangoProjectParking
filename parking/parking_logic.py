import datetime

import uuid


def generar_pin():
    return str(uuid.uuid4().int)[:6]


from datetime import datetime
from .models import Plaza, Ticket, Cobro


def depositar_vehiculo(matricula, tipo):
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


def crear_plazas_turismo():
    tipos = ['Turismo']
    for i in range(1, 101):
        for tipo in tipos:
            plaza = Plaza(numero=i, tipo=tipo, estado='Libre', tarifa_minuto=0.12)
            plaza.save()
    print("Plazas creadas correctamente.")


crear_plazas_turismo()



def crear_plazas_moto():
    tipos = ['Moto']
    for i in range(1, 101):
        for tipo in tipos:
            plaza = Plaza(numero=i, tipo=tipo, estado='Libre', tarifa_minuto=0.10)
            plaza.save()
    print("Plazas creadas correctamente.")


crear_plazas_moto()

def crear_plazas_pmr():
    tipos = ['PMR']
    for i in range(1, 101):
        for tipo in tipos:
            plaza = Plaza(numero=i, tipo=tipo, estado='Libre', tarifa_minuto=0.10)
            plaza.save()
    print("Plazas creadas correctamente.")


crear_plazas_pmr()


def retirar_vehiculo(matricula, id, pin):
    try:
        ticket = Ticket.objects.get(matricula=matricula, plaza_id=id, pin=pin)
    except Ticket.DoesNotExist:
        raise ValueError("Ticket no válido")
    # calcular coste
    diferencia = datetime.now() - ticket.fecha_entrada
    importe = diferencia.seconds / 60 * ticket.plaza.tarifa_minuto
    cobro = Cobro(ticket=ticket, importe=importe, fecha_pago=datetime.now())
    cobro.save()
    # actualizar plaza
    plaza = ticket.plaza
    plaza.estado = 'Libre'
    plaza.save()
    # eliminar ticket
    ticket.delete()
    return cobro
