from datetime import date, timedelta, datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, F, Sum, Max, Min, Count, Avg
from django.db.models.functions import Length
from django.utils import timezone
from text.models import Cargo, Empleado, Prestamo, Pago

# Funciones de creación masiva para la nueva aplicación

def create_bulk_cargos(cargos_data):
    cargos = []
    for data in cargos_data:
        cargo = Cargo(nombre_cargo=data["nombre_cargo"], descripcion=data["descripcion"])
        cargos.append(cargo)
    Cargo.objects.bulk_create(cargos)
    print(f"{len(cargos)} cargos creados con éxito.")

def create_bulk_empleados(empleados_data):
    empleados = []
    for data in empleados_data:
        cargo = Cargo.objects.get(id=data["cargo_id"])
        empleado = Empleado(
            nombre=data["nombre"],
            apellido=data["apellido"],
            direccion=data["direccion"],
            telefono=data["telefono"],
            email=data["email"],
            cargo=cargo
        )
        empleados.append(empleado)
    Empleado.objects.bulk_create(empleados)
    print(f"{len(empleados)} empleados creados con éxito.")

def create_bulk_prestamos(prestamos_data):
    prestamos = []
    for data in prestamos_data:
        empleado = Empleado.objects.get(id=data["empleado_id"])
        prestamo = Prestamo(
            monto=data["monto"],
            fecha_prestamo=data["fecha_prestamo"],
            empleado=empleado,
            numero_cuotas=data["numero_cuotas"],
            cuota=data["cuota"]
        )
        prestamos.append(prestamo)
    Prestamo.objects.bulk_create(prestamos)
    print(f"{len(prestamos)} préstamos creados con éxito.")

def create_bulk_pagos(pagos_data):
    pagos = []
    for data in pagos_data:
        prestamo = Prestamo.objects.get(id=data["prestamo_id"])
        pago = Pago(
            monto_pago=data["monto_pago"],
            fecha_pago=data["fecha_pago"],
            prestamo=prestamo
        )
        pagos.append(pago)
    Pago.objects.bulk_create(pagos)
    print(f"{len(pagos)} pagos creados con éxito.")

# Ejemplo de uso de las nuevas funciones
def run_bulk_creation_functions():
    cargos_data = [
        {"nombre_cargo": "Gerente", "descripcion": "Responsable de la gestión del equipo."},
        {"nombre_cargo": "Desarrollador", "descripcion": "Desarrollo de aplicaciones y mantenimiento de software."}
        
    ]
    empleados_data = [
        {"nombre": "Juan", "apellido": "Pérez", "direccion": "Calle Falsa 123", "telefono": "123456789", "email": "juan.perez@example.com", "cargo_id": 1},
        {"nombre": "Ana", "apellido": "Gómez", "direccion": "Avenida Siempre Viva 742", "telefono": "987654321", "email": "ana.gomez@example.com", "cargo_id": 2},
        {"nombre": "Luis", "apellido": "Ramos", "direccion": "Avenida Siempre Viva 742", "telefono": "987654321", "email": "luis.ramos@example.com", "cargo_id": 2},
    ]
    prestamos_data = [
        {"monto": 1000.00, "fecha_prestamo": date(2023, 5, 17), "empleado_id": 1, "numero_cuotas": 12, "cuota": 83.33},
        {"monto": 2000.00, "fecha_prestamo": date(2023, 6, 17), "empleado_id": 2, "numero_cuotas": 24, "cuota": 83.33},
        {"monto": 3000.00, "fecha_prestamo": date(2023, 7, 17), "empleado_id": 3, "numero_cuotas": 36, "cuota": 83.33},
        {"monto": 4000.00, "fecha_prestamo": date(2023, 8, 17), "empleado_id": 3, "numero_cuotas": 48, "cuota": 83.33},
        {"monto": 5000.00, "fecha_prestamo": date(2023, 9, 17), "empleado_id": 3, "numero_cuotas": 60, "cuota": 83.33},
    ]
    pagos_data = [
    {"monto_pago": 80.33, "fecha_pago": date(2023, 6, 17), "prestamo_id": 1},
    {"monto_pago": 90.33, "fecha_pago": date(2023, 7, 17), "prestamo_id": 2},
    {"monto_pago": 100.50, "fecha_pago": date(2023, 8, 17), "prestamo_id": 3},
    {"monto_pago": 110.75, "fecha_pago": date(2023, 9, 17), "prestamo_id": 4},
    {"monto_pago": 120.00, "fecha_pago": date(2023, 10, 17), "prestamo_id": 5},
    {"monto_pago": 130.25, "fecha_pago": date(2023, 11, 17), "prestamo_id": 6},
    {"monto_pago": 140.50, "fecha_pago": date(2023, 12, 17), "prestamo_id": 7},
    {"monto_pago": 150.75, "fecha_pago": date(2023, 1, 17), "prestamo_id": 8},
    {"monto_pago": 160.00, "fecha_pago": date(2023, 2, 17), "prestamo_id": 9},
    {"monto_pago": 170.25, "fecha_pago": date(2023, 3, 17), "prestamo_id": 10},
    {"monto_pago": 180.50, "fecha_pago": date(2023, 4, 17), "prestamo_id": 11},
    {"monto_pago": 190.75, "fecha_pago": date(2023, 5, 17), "prestamo_id": 12},
    {"monto_pago": 200.00, "fecha_pago": date(2023, 6, 17), "prestamo_id": 13},
    {"monto_pago": 210.25, "fecha_pago": date(2023, 7, 17), "prestamo_id": 14},
    {"monto_pago": 220.50, "fecha_pago": date(2023, 8, 17), "prestamo_id": 15},
    {"monto_pago": 230.75, "fecha_pago": date(2023, 9, 17), "prestamo_id": 1},
    {"monto_pago": 240.00, "fecha_pago": date(2023, 10, 17), "prestamo_id": 2},
    {"monto_pago": 250.25, "fecha_pago": date(2023, 11, 17), "prestamo_id": 3},
    {"monto_pago": 260.50, "fecha_pago": date(2023, 12, 17), "prestamo_id": 4},
    {"monto_pago": 270.75, "fecha_pago": date(2023, 1, 17), "prestamo_id": 5},
    {"monto_pago": 280.00, "fecha_pago": date(2023, 2, 17), "prestamo_id": 6},
    {"monto_pago": 290.25, "fecha_pago": date(2023, 3, 17), "prestamo_id": 7},
    {"monto_pago": 300.50, "fecha_pago": date(2023, 4, 17), "prestamo_id": 8},
    {"monto_pago": 310.75, "fecha_pago": date(2023, 5, 17), "prestamo_id": 9},
    {"monto_pago": 320.00, "fecha_pago": date(2023, 6, 17), "prestamo_id": 10},
    {"monto_pago": 330.25, "fecha_pago": date(2023, 7, 17), "prestamo_id": 11},
    {"monto_pago": 340.50, "fecha_pago": date(2023, 8, 17), "prestamo_id": 12},
    {"monto_pago": 350.75, "fecha_pago": date(2023, 9, 17), "prestamo_id": 13},
    {"monto_pago": 360.00, "fecha_pago": date(2023, 10, 17), "prestamo_id": 14},
    {"monto_pago": 370.25, "fecha_pago": date(2023, 11, 17), "prestamo_id": 15}
]
    create_bulk_cargos(cargos_data)
    create_bulk_empleados(empleados_data)
    create_bulk_prestamos(prestamos_data)
    create_bulk_pagos(pagos_data)

def obtener_empleados_por_apellido_y_email():
            empleados = Empleado.objects.filter(
                apellido__istartswith='G',
                email__iendswith='gmail.com'
            )

            for empleado in empleados:
                print(f"{empleado.nombre} {empleado.apellido} - {empleado.email}")

obtener_empleados_por_apellido_y_email()
# run_bulk_creation_functions()

