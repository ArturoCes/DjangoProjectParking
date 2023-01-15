from django.contrib import admin
from .models import Cliente, Plaza,Abono,Ticket, Cobro;

# Register your models here.
admin.site.register(Cliente);
admin.site.register(Cobro);
admin.site.register(Ticket);
admin.site.register(Abono);
admin.site.register(Plaza);
