# Proyecto_Parking
## Entorno de desarrollo y ejecución:

Para ejecutar el proyecto abre el terminal y ejecuta el comando --> - python manage.py runserver

## Organización del proyecto:
En este proyecto hemos llamado Parking, ya que se trata de gestionar un Parking en el cual hay dos áreas que el usuario puede acceder, tanto al sistema de Administrador como al sistema de Usuario, en la que en cada uno contará con sus propias funcionalidades y características.

Se ha utilizado en este proyecto:

-**Django**: Hemos utilizado Django ya que se ha querido implementar un fronted para la aplicación y una manera diferente de hacer esta gestión, ya que he querido transformar este proyecto en una aplicación web y tiene mayor documentación, además de que contiene su propio ORM

-**Python**: Se ha utilizado el lenguaje de programación Python para el desarrollo de esta aplicación

## Zonas de la aplicación:
### Cliente:

En el área de Cliente, el usuario solamente dispondrá de las siguiente funcionalidades en la que tendrá su respectiva característica de si se trata de un abonado o de un cliente corriente:

- **Depositar_Vehiculo**: En este método, se deposita una plaza, un pin a un no abonado
- **Retirar_Vehiculo**: En este método, se retira de la plaza anteriormente asignada junto al pin, el vehículo estacionado de un no abonado
- **Depositar_Abonados**: En este método se deposita una plaza, un pin a un cliente que se trata de un abonado
- **Retirar_abonado**: Se retira el vehículo anteriormente dado del cliente abonado

### Administrador:

En el área de Administrador, el usuario solamente dispondrá de las siguientes funcionalidades en la que tendrá sus respectivas características al tratarse de los abonos realizados:

- **Estado_parking**: Se muestra las plazas libres, ocupadas y reservadas de abonados
- **Alta_abono**: Se crea un abono(mensual, trimestral, semanal o anual) dada a los abonados
- **faltan campos**
