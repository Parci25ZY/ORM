from datetime import date, time, timedelta, datetime
from core.models import Period, Note, DetailNote, Student, Teacher, Asignature, ActiveManager, GeneralDelete
from django.contrib.auth.models import User
import random
from create import periods, asignatures, students, teachers, students_data
from django.db.models import Q, F, Sum, Max, Min, Count, Avg, ExpressionWrapper, FloatField
from django.db.models.functions import Length
from django.utils import timezone

"""
                *********************************
                            ORM TAREA 
      ESTUDIANTES  | MAESTROS  | ASIGNATURAS | NOTAS | PERIODO     
                **********************************
"""

def create_bulks(state):
    if state:
        #----> INSERT Periodos
        periodos = []
        for key, value in periods.items():
            periodo = Period(description = value["description"], start_date = value["start_date"], end_date = value["end_date"], user = User.objects.get(username=value["user"]))
            periodos.append(periodo)

        Period.objects.bulk_create(periodos)

        #----> INSERT Asignaturas
        asignaturas = []
        for key, value in asignatures.items():
            asignatura = Asignature(description = value["description"], user = User.objects.get(username = value["user"]))
            asignaturas.append(asignatura)

        Asignature.objects.bulk_create(asignaturas)

        #----> INSERT Profesores
        profesores = []
        for key, value in teachers.items():
            profesor = Teacher(cedula = value["cedula"], first_name = value["first_name"], last_name = value["last_name"], user = User.objects.get(username = value["user"]))
            profesores.append(profesor)

        Teacher.objects.bulk_create(profesores)

        #----> INSERT Estudiantes
        estudiantes = []
        for key, value in students.items():
            estudiante = Student(cedula = value["cedula"], first_name = value["first_name"], last_name = value["last_name"], user = User.objects.get(username = value["user"]))
            estudiantes.append(estudiante)

        Student.objects.bulk_create(estudiantes)
    else:
        print("No se puede crear la base de datos")
create_bulks(False)

# ++ RELACIONES UNO A MUCHOS PARA NOTAS, CREAR OBJETO PARA NOTAS ++
def note_create(state):
    user = User.objects.get(username = "davdev")
    if state:
        for i in range(1,11):
            periodo    = Period.objects.get(id=i)
            profesor   = Teacher.objects.get(id=i)
            asignatura = Asignature.objects.get(id=i)
            note = Note.objects.create(
                period     = periodo,
                teacher    = profesor,
                asignature = asignatura,
                user = user
            )
    else:
        print("No se puede crear la base de datos")
note_create(False)

## +++  RELACION UNO PARA MUCHOS DETALLES_NOTA (SENTENCIA: CREAR) +++
def create_detail(state):
    user = User.objects.get(username = "davdev")
    if state:
        for data_detail in students_data.values():
            detail_note = DetailNote(
                note = data_detail["note"],
                estudiante_id = data_detail["student"],
                note1 = data_detail["note1"],
                note2 = data_detail["note2"],
                recovery = data_detail["recovery"],
                observations = data_detail["observations"],
                user = user
            )
            detail_note.save()
            print("REGISTROS GUARDADOS CON EXITO")
    else:
        print("NO SE GUARDARON LOS REGISTROS")
create_detail(False)

# +++ FUNCIÓN UNIRSE PARA CONSULTAS GENERALES +++
def joiners(listers):
    return print(f"\n".join([f" ==> {context}" for i, context in enumerate(listers)]))

# +++ CONSULTA BÁSICA GENERAL +++
def consult_basic():
    # ---> CONSULTAR ESTUDIANTES CUYO NOMBRE COMIENZA CON "EST" <---
    def consult_student(state):
        if state:
            students = Student.objects.filter(first_name__istartswith="est")
            if students.exists():
                print("Estudiantes cuyos nombres comienzan con 'Est':")
                for student in students:
                    print(f'{student.full_name()} y su cédula es {student.cedula}')
            else:
                print("No se encontraron estudiantes cuyos nombres comiencen con 'Est'.")
    consult_student(False)

    # ---> CONSULTAR MAESTROS CUYO NOMBRE COMIENZA CON "OR" <---
    def consult_teacher(state):
        if state:
            teachers = Teacher.objects.filter(first_name__icontains="or")
            joiners(teachers)
    consult_teacher(False)

    # ---> CONSULTAR ASIGNATURAS CUYA DESCRIPCIÓN TERMINA EN "10" <---
    def consult_asignatures_end10(state):
        if state:
            asignatures = Asignature.objects.filter(description__endswith="10")
            joiners(asignatures)
    consult_asignatures_end10(False)

    # ---> VER NOTAS QUE SON MAYORES A 8.0 <---
    def consult_notes_elderly(states):
        if states:
            note1  = DetailNote.objects.filter(note1__gt=8.0) 
            lister = [[note.estudiante_id.full_name(), note.note1] for note in note1]
            print("Listado de Estudiantes y Notas:\n" + "-"*77)
            joiners([f"Nombre del Estudiante: {estudiante:<30} | Nota1 ->: {nota}" for estudiante, nota in lister])
            print("-"*77)
    consult_notes_elderly(False)

    # ---> VER NOTAS QUE SON MENORES A 9.0 <---
    def consult_notes_minor(states):
        if states:
            note2  = DetailNote.objects.filter(note2__lt=9.0)
            lister = [[note.estudiante_id.full_name(), note.note2] for note in note2]
            print("Listado de Estudiantes y Notas:\n" + "-"*77)
            joiners([f"Nombre del Estudiante: {estudiante:<30} | Nota2 ->: {nota}" for estudiante, nota in lister])
            print("-"*77)
    consult_notes_minor(False)

# ---> LLAMAR A LA FUNCIÓN PARA VER SU FUNCIONALIDAD <---
consult_basic()

# ---> CONSULTAS UTILIZANDO CONDICIONES LÓGICAS (AND, OR, NOT) <---
def consult_logical_conditions():
    #--> Seleccionar todos los estudiantes cuyo nombre comienza con 'Est' y su ID termina en '1': <--
    def consult_students(states):
        if states:
            students = Student.objects.filter(Q(first_name__istartswith='Est') & Q(cedula__endswith='1'))
            for student in students:
                print(f'\n {student} | Cédula: {student.cedula}')
    consult_students(False)

    #--> Seleccionar todas las asignaturas cuya descripción contiene 'Asig' o termina en '5': <--
    def consult_asignatures(states):
        if states:
            asignatures = Asignature.objects.filter(
            Q(description__icontains="Asig") | Q(description__endswith="5"))
            for asignature in asignatures:
                print(asignature)
    consult_asignatures(False)

    #--> Seleccionar todos los maestros cuyo nombre no contiene 'or': <--
    def consult_teachers(states):
        if states:
            teachers = Teacher.objects.filter(~Q(first_name__icontains="or"))
            for teacher in teachers:
                print(teacher)
    consult_teachers(False)

    #--> Seleccionar todas las notas con nota1 mayor a 7.0 y nota2 menor a 8.0: <--
    def consult_notes(states):
        if states:
            notes = DetailNote.objects.filter(
            Q(note1__gt=7.0) & Q(note2__lt=8.0))
            for note in notes:
                print(f"Nombre del Estudiante: {note.student.full_name()} | Nota1 ->: {note.note1} | Nota2 ->: {note.note2}")
    consult_notes(False)

    #--> Seleccionar todas las notas con recuperación igual a Ninguna o nota2 mayor a 9.0: <--
    def consult_notes_with_recovery(states):
        if states:
            notes = DetailNote.objects.filter(
            Q(recovery__isnull = True) | Q(note2__gt = 9.0))
            for note in notes:
                print(f"Nombre del Estudiante: {note.student.full_name()} | Recuperación ->: {note.recovery} | Nota2 ->: {note.note2}")
    consult_notes_with_recovery(False)

# ---> LLAMAR A LA FUNCIÓN PARA VER SU FUNCIONALIDAD <---
consult_logical_conditions()

# ---> CONSULTAS NUMÉRICAS <---
def consult_funcion_numer():
    # ---> Seleccionar todas las notas con nota1 entre 7.0 y 9.0 <---
    def consult_notes7_9(states):
        if states:
            notes = DetailNote.objects.filter(note1__gte=7.0, note1__lte=9.0)
            print("Notas con nota1 entre 7.0 y 9.0:")
            for note in notes:
                print(f"ID: {note.id} | Estudiante: {note.estudiante_id.full_name()} | Nota1: {note.note1}")
    consult_notes7_9(False)

    # ---> Seleccionar todas las notas con nota2 fuera del rango 6.0 a 8.0 <---
    def consult_notes_range_6_8(states):
        if states:
            notes = DetailNote.objects.filter(~Q(note2__gte=6.0) | ~Q(note2__lte=8.0))
            print("Notas con nota2 fuera del rango 6.0 a 8.0:")
            for note in notes:
                print(f"ID: {note.id} | Estudiante: {note.estudiante_id.full_name()} | Nota2: {note.note2}")
    consult_notes_range_6_8(False)

#    ---> Todas las notas cuya recuperacion no sea None: <---
    def consult_notes_none(states):
        if states:
            notes = DetailNote.objects.filter(recovery__isnull=False)
            print("Notas con recuperación no nula:")
            for note in notes:
                print(f"ID: {note.id} | Estudiante: {note.estudiante_id.full_name()} | Recuperación: {note.recovery}")
    consult_notes_none(False)

# ---> LLAMAR A LA FUNCIÓN PARA VER SU FUNCIONALIDAD <---
consult_funcion_numer()

# ---> CONSULTAS DE FECHA <---
def consult_funcion_fech():
#  ---> Seleccionar todas las notas creadas en el último año <---
    def consult_notes_ultimo_año(states):
        if states:
            fecha_actual = timezone.now()
            fecha_hace_un_anio = fecha_actual - timedelta(days=365)
            notas_ultimo_anio = DetailNote.objects.filter(created__gte=fecha_hace_un_anio)
            if notas_ultimo_anio.exists():
                print("Notas creadas en el último año:")
                for nota in notas_ultimo_anio:
                    print(f"ID: {nota.id} | Estudiante: {nota.estudiante_id.full_name()} | Fecha de Creación: {nota.created}")
            else:
                print("No se encontraron notas creadas en el último año.")
    consult_notes_ultimo_año(False)

# ---> Seleccionar todas las notas creadas en el último mes <---
    def consult_notes_ultimo_mes(states):
        if states:
            fecha_actual = timezone.now()
            fecha_hace_un_mes = fecha_actual - timedelta(days=30)
            notas_ultimo_mes = DetailNote.objects.filter(created__gte=fecha_hace_un_mes)
            if notas_ultimo_mes.exists():
                print("Notas creadas en el último mes:")
                for nota in notas_ultimo_mes:
                    print(f"ID: {nota.id} | Estudiante: {nota.estudiante_id.full_name()} | Fecha de Creación: {nota.created}")
            else:
                print("No se encontraron notas creadas en el último mes.")
    consult_notes_ultimo_mes(False)

# --->  Seleccionar todas las notas creadas en el último día <---
    def consult_notes_ultimo_dia(states):
        if states:
            fecha_actual = datetime.now()
            fecha_hace_un_dia = fecha_actual - timedelta(days=1)
            notas_ultimo_dia = DetailNote.objects.filter(created__gte=fecha_hace_un_dia)
            if notas_ultimo_dia.exists():
                print("Notas creadas en el último día:")
                for nota in notas_ultimo_dia:
                    print(f"ID: {nota.id} | Estudiante: {nota.estudiante_id.full_name()} | Fecha de Creación: {nota.created}")
            else:
                print("No se encontraron notas creadas en el último día.")
    consult_notes_ultimo_dia(False)

# ---> Seleccionar todas las notas creadas antes del año 2023 <---
    def consult_notes_antes_2023(states):
        if states:
            fecha_limite = datetime(2023, 1, 1)

            notas_antes_2023 = DetailNote.objects.filter(created__lt=fecha_limite)

            if notas_antes_2023.exists():
                print("Notas creadas antes del año 2023:")
                for nota in notas_antes_2023:
                    print(f"ID: {nota.id} | Estudiante: {nota.student.full_name()} | Fecha de Creación: {nota.created}")
            else:
                print("No se encontraron notas creadas antes del año 2023.")
    consult_notes_antes_2023(False)

# ---> Seleccionar todas las notas creadas en marzo de cualquier año <---
    def consult_notes_in_marzo(states):
        if states:
            fecha_inicio = datetime(datetime.now().year, 3, 1)
            fecha_fin = datetime(datetime.now().year, 3, 31, 23, 59, 59)
            notas_en_marzo = DetailNote.objects.filter(created__gte=fecha_inicio, created__lte=fecha_fin)
            if notas_en_marzo.exists():
                print("Notas creadas en marzo de cualquier año:")
                for nota in notas_en_marzo:
                    print(f"ID: {nota.id} | Estudiante: {nota.student.full_name()} | Fecha de Creación: {nota.created}")
            else:
                print("No se encontraron notas creadas en marzo de ningún año.")
    consult_notes_in_marzo(False)

# ---> LLAMAR A LA FUNCIÓN PARA VER SU FUNCIONALIDAD <---
consult_funcion_fech()


# ---> CONSULTAS COMBINADAS FUNCION AVANZADA <---
def consult_avazand():
#  ---> Seleccionar todos los estudiantes cuyo nombre tiene exactamente 10 caracteres: <---
    def consult_estudiantes_caracter_10(states):
        if states:
            students = Student.objects.annotate(first_name_length=Length('first_name')).filter(first_name_length=10)
            # Imprimir los resultados
            if students.exists():
                print("Estudiantes con nombre de exactamente 10 caracteres:")
                for student in students:
                    print(f"{student.first_name} {student.last_name}")
            else:
                print("No se encontraron estudiantes con nombre de exactamente 10 caracteres.")
    consult_estudiantes_caracter_10(False)

#   --> Seleccionar todas las notas con nota1 y nota2 mayores a 7.5: <--
    def consult_notes_mayor_7_5(states):
        if states:
            notes = DetailNote.objects.filter(note1__gt=7.5, note2__gt=7.5)
            print("Notas con nota1 y nota2 mayores a 7.5:")
            for note in notes:
                print(f"ID: {note.id} | Estudiante: {note.estudiante_id.full_name()} | Nota1: {note.note1} | Nota2: {note.note2}")
    consult_notes_mayor_7_5(False)

# ---> Seleccionar todas las notas con recuperacion no nula y nota1 mayor a nota2: <---
    def consult_notes_mayor_nota2(states):
        if states:
            notes = DetailNote.objects.filter(recovery__isnull=False, note1__gt=F('note2'))
            print("Notas con recuperación no nula y nota1 mayor a nota2:")
            for note in notes:
                print(f"ID: {note.id} | Estudiante: {note.estudiante_id.full_name()} | Recuperación: {note.recovery} | Nota1: {note.note1} | Nota2: {note.note2}")
    consult_notes_mayor_nota2(False)

# ---> Seleccionar todas las notas con nota1 mayor a 8.0 o nota2 igual a 7.5 <---
    def consult_notes_8_7(states):
        if states:
            notes = DetailNote.objects.filter(Q(note1__gt=8.0) | Q(note2=7.5))
            print("Notas con nota1 mayor a 8.0 o nota2 igual a 7.5:")
            for note in notes:
                print(f"ID: {note.id} | Estudiante: {note.estudiante_id.full_name()} | Nota1: {note.note1} | Nota2: {note.note2}")
    consult_notes_8_7(False)

# ---> Seleccionar todas las notas con recuperacion mayor a nota1 y nota2 <---
    def consult_recuperacion_note1_note2(states):
       if states:
            notes = DetailNote.objects.filter(Q(recovery__gt=F('note1')) & Q(recovery__gt=F('note2')))
            print("Notas con recuperación mayor a nota1 y nota2:")
            for note in notes:
                print(f"ID: {note.id} | Estudiante: {note.estudiante_id.full_name()} | Nota1: {note.note1} | Nota2: {note.note2} | Recuperación: {note.recovery}")
    consult_recuperacion_note1_note2(False)

# ---> LLAMAR A LA FUNCIÓN PARA VER SU FUNCIONALIDAD <---
consult_avazand()

# ---> CONSULTAS DE SUVCOSULTAS <---
def consult_subcosult():
# ---> Seleccionar todos los estudiantes con al menos una nota de recuperación <---
    def student_menor_recuperacion(states):
        if states:
            students = Student.objects.filter(student_detail__recovery__isnull=False).distinct()
            print("Estudiantes con al menos una nota de recuperación:")
            for student in students:
                print(f"{student.first_name} {student.last_name}")
    student_menor_recuperacion(False)
    
# -->  Seleccionar todos los profesores que han dado una asignatura específica <---
    def consult_teacher_asignature_distinct(states):
        if states:
            asignatura_id = 1 
            teachers = Teacher.objects.filter(notes__asignature_id=asignatura_id).distinct()
            if teachers.exists():
                print(f"Profesores que han dado la asignatura con ID {asignatura_id}:")
                for teacher in teachers:
                    print(f"{teacher.first_name} {teacher.last_name}")
    consult_teacher_asignature_distinct(False)

# --> Seleccionar todas las asignaturas que tienen al menos una nota registrada <---
    def consult_asignaturas_con_notas(states):
        if states:
            asignaturas = Asignature.objects.filter(notes__isnull=False).distinct()
            if asignaturas.exists():
                print("Asignaturas con al menos una nota registrada:")
                for asignatura in asignaturas:
                    print(asignatura)
    consult_asignaturas_con_notas(False)

# -->  Seleccionar todas las asignaturas que no tienen notas registradas <---
    def consult_asignatura_sin_notas(states):
        if states:
            asignaturas = Asignature.objects.filter(notes__isnull=True).distinct()
            if asignaturas.exists():
                print("Asignaturas sin notas registradas:")
                for asignatura in asignaturas:
                    print(asignatura)
    consult_asignatura_sin_notas(False)

# -->  Seleccionar todos los estudiantes que no tienen notas de recuperación <---
    def consult_notas_no_recuperacion(states):
        if states:
            students = Student.objects.filter(student_detail__recovery__isnull=True).distinct()
            if students.exists():
                print("Estudiantes que no tienen notas de recuperación:")
                for student in students:
                    print(f"{student.first_name} {student.last_name}")
    consult_notas_no_recuperacion(False)

# --> Seleccionar todas las notas cuyo promedio de nota1 y nota2 es mayor a 8.0 <---
    def consult_promedio_mayor_8_0(states):
        if states:
            notes = DetailNote.objects.annotate(promedio=(F('note1')+F('note2'))/2).filter(promedio__gt=8.0)
            print("Notas cuyo promedio de nota1 y nota2 es mayor a 8.0:")
            for note in notes:
                print(f"ID: {note.id} | Estudiante: {note.estudiante_id.full_name()} | Nota1: {note.note1} | Nota2: {note.note2} | Promedio: {note.promedio}")
    consult_promedio_mayor_8_0(False)

#  --> Seleccionar todas las notas con nota1 menor que 6.0 y nota2 mayor que 7.0 <---
    def consult_nota1_menor_6_nota2_mayor_7(states):
        if states:
            notes = DetailNote.objects.filter(note1__lt=6.0, note2__gt=7.0)
            if notes.exists():
                print("Notas con nota1 menor que 6.0 y nota2 mayor que 7.0:")
                for note in notes:
                    print(f"ID: {note.id} | Estudiante: {note.student.full_name()} | Nota1: {note.note1} | Nota2: {note.note2}")
            else:
                print("No se encontraron notas con nota1 menor que 6.0 y nota2 mayor que 7.0.")
    consult_nota1_menor_6_nota2_mayor_7(False)

#  ---> Seleccionar todas las notas con nota1 en la lista <---
    def consultar_notas_con_nota1_en_lista(states):
        if states:
            lista_notas = [7.0, 8.0, 9.0]
            notas = DetailNote.objects.filter(note1__in=lista_notas)
            if notas.exists():
                print("Notas con note1 en la lista [7.0, 8.0, 9.0]:")
                for nota in notas:
                    print(f"ID: {nota.id} | Estudiante: {nota.estudiante_id.full_name()} | Nota1: {nota.note1} | Nota2: {nota.note2}")
            else:
                print("No se encontraron notas con note1 en la lista [7.0, 8.0, 9.0].")
    consultar_notas_con_nota1_en_lista(False)

# ---> Seleccionar todas las notas cuyo id está en un rango del 1 al 5 <---
    def consultar_notas_en_rango(states):
        if states:
            notas = DetailNote.objects.filter(id__range=(1,5))
            if notas.exists():
                print("Notas cuyo id está en un rango del 1 al 5:")
                for nota in notas:
                    print(f"ID: {nota.id} | Estudiante: {nota.estudiante_id.full_name()} | Nota1: {nota.note1} | Nota2: {nota.note2}")
            else:
                print("No se encontraron notas cuyo id está en un rango del 1 al 5.")
    consultar_notas_en_rango(False)

# ---> Seleccionar todas las notas cuyo recuperacion no está en la lista [8.0, 9.0, 10.0] <---
    def consultar_notas_con_recuperacion_no_en_lista(states):
        if states:
            lista_recuperacion = [8.0, 9.0, 10.0]
            notas = DetailNote.objects.exclude(recovery__in=lista_recuperacion)
            if notas.exists():
                print("Notas cuyo recuperacion no está en la lista [8.0, 9.0, 10.0]")
                for nota in notas:
                    print(f"ID: {nota.id} | Estudiante: {nota.estudiante_id.full_name()} | Recuperación: {nota.recovery}")
    consultar_notas_con_recuperacion_no_en_lista(False)

#  ---> Suma de todas las notas de un estudiante <---
    def suma_notas_estudiante(states):
        if states:
            estudiante_id = 1 
            estudiante = Student.objects.get(pk=estudiante_id)

            suma_notas = DetailNote.objects.filter(estudiante_id=estudiante_id).annotate(
                suma=ExpressionWrapper(F('note1') + F('note2'), output_field=FloatField())
            ).aggregate(suma_total=Sum('suma'))

            suma = suma_notas['suma_total'] or 0

            print(f"La suma de todas las notas del estudiante {estudiante.full_name()} con ID {estudiante_id} es: {suma:.2f}")
    suma_notas_estudiante(False)

# --->  Nota máxima obtenida por un estudiante <---
    def nota_maxima_estudiante(states):
        if states:
            estudiante_id = 1  
            estudiante = Student.objects.get(pk=estudiante_id)
            maxima_nota = DetailNote.objects.filter(estudiante_id=estudiante_id).aggregate(max_nota=Max('note1'), max_nota2=Max('note2'))
            max_nota1 = maxima_nota['max_nota']
            max_nota2 = maxima_nota['max_nota2']

            if max_nota1 is None and max_nota2 is None:
                maxima = 0
            elif max_nota1 is None:
                maxima = max_nota2
            elif max_nota2 is None:
                maxima = max_nota1
            else:
                maxima = max(max_nota1, max_nota2)
            print(f"La nota máxima obtenida por el estudiante {estudiante.full_name()} con ID {estudiante_id} es: {maxima}")
    nota_maxima_estudiante(False)

# ---> Nota mínima obtenida por un estudiante <---
    def nota_minima_estudiante(states):
        if states:
            estudiante_id = 1  
            estudiante = Student.objects.get(pk=estudiante_id)
            minima_nota = DetailNote.objects.filter(estudiante_id=estudiante_id).aggregate(min_nota=Min('note1'), min_nota2=Min('note2'))
            min_nota1 = minima_nota['min_nota']
            min_nota2 = minima_nota['min_nota2']

            if min_nota1 is None and min_nota2 is None:
                minima = 0
            elif min_nota1 is None:
                minima = min_nota2
            elif min_nota2 is None:
                minima = min_nota1
            else:
                minima = min(min_nota1, min_nota2)
            print(f"La nota mínima obtenida por el estudiante {estudiante.full_name()} con ID {estudiante_id} es: {minima}")
    nota_minima_estudiante(False)

# ---> Contar el número total de notas de un estudiante <---
    def contar_notas_estudiante(states):
        if states:
            estudiante_id = 1 
            estudiante = Student.objects.get(pk=estudiante_id)
            notas_estudiante = DetailNote.objects.filter(estudiante_id=estudiante_id)
            total_notas_individuales = sum(1 for nota in notas_estudiante for _ in (nota.note1, nota.note2) if nota.note1 is not None and nota.note2 is not None)
            print(f"El número total de notas individuales del estudiante {estudiante.full_name()} con ID {estudiante_id} es: {total_notas_individuales}")
    contar_notas_estudiante(False)

# ---> Promedio de todas las notas de un estudiante sin incluir recuperación <---
    def promedio_notas_sin_recuperacion(states):
        if states:
            estudiante_id = 1 
            estudiante = Student.objects.get(pk=estudiante_id)
            notas_estudiante = DetailNote.objects.filter(estudiante_id=estudiante_id).annotate(
                promedio=ExpressionWrapper((F('note1') + F('note2')) / 2.0, output_field=FloatField())
            ).aggregate(promedio_total=Avg('promedio'))

            promedio = notas_estudiante['promedio_total'] or 0

            print(f"El promedio de todas las notas (sin recuperación) del estudiante {estudiante.full_name()} con ID {estudiante_id} es: {promedio:.2f}")
    promedio_notas_sin_recuperacion(False)

# ---> LLAMAR A LA FUNCIÓN PARA VER SU FUNCIONALIDAD <---
consult_subcosult()


# ---> CONSULTAS CON SUBCONSULTAS CON LOS MODELOS RELACIONADO. APLICAR 
# RELACIONES INVERSAS DONDE SEA NECESARIO <---
def consult_notes():
    def get_student_notes(state, student_id):
        if state:
            notes = DetailNote.objects.filter(estudiante_id=student_id).select_related('note__period', 'note__teacher', 'note__asignature')     # utilizan el doble subrayado (__) para seguir la relación desde DetailNote hasta los modelos relacionados (Note, Period, Teacher, Asignature).
            print("Todas sus notas con el detalle de todos sus datos de un estudiante:")
            for note in notes:
                print(f"Estudiante: {note.estudiante_id.full_name} | Nota 1:{note.note1} | Note 2: {note.note2} | Recovery: {note.recovery} | Observations: {note.observations}")
                print(f"Periodo: {note.note.period.description} | Teacher: {note.note.teacher.first_name} {note.note.teacher.last_name} | Asignatura: {note.note.asignature.description}")
    get_student_notes(False,1)   

    def get_notes_by_period(state, period_id):
        if state:
            notes = DetailNote.objects.filter(note__id=period_id)
            print("Todas las notas de un periodo en especifico:")
            for note in notes:
                print(f"Estudiante: {note.estudiante_id.full_name} | Nota 1: {note.note1} | Nota 2: {note.note2} | Recuperación: {note.recovery} | Observaciones: {note.observations}")
    get_notes_by_period(False,10) 

    def consult_notes_asignature_period(state, asignature_id, period_id):
        if state:
            notes = DetailNote.objects.filter(note__asignature_id=asignature_id, note__period_id= period_id)
            print("Todas las notas de una asignatura dada en un período:")
            for note in notes:
                print(f"Estudiante: {note.estudiante_id.full_name} | Nota 1: {note.note1} | {note.note2} | Recuperación: {note.recovery} | {note.observations}")
                print(f"Periodo: {note.note.period.description} | Asignatura: {note.note.asignature.description}")

    consult_notes_asignature_period(False, 1, 1)
    
    def get_notes_teacher(state, teacher_id):
        if state:
            teacher = Teacher.objects.get(id= teacher_id)
            notes = DetailNote.objects.filter(note__teacher= teacher)

            print(f"Todas las notas del profesor {teacher.full_name}:")
            for note in notes:
                print(f"Nota 1: {note.note1} | Nota 2: {note.note2} | Recuperación: {note.recovery} | Observaciones: {note.observations}")

    get_notes_teacher(False, 1)  

    def consult_notes_above_value(state, student_id, value):
        if state:
            notes = DetailNote.objects.filter(estudiante_id=student_id, note1__gt=value)
            print(f"Todas las notas de un estudiante con notas superiores a {value}:")
            for note in notes:
                print(f"Periodo: {note.note.period.description} | Asignature: {note.note.asignature.description} | Nota 1: {note.note1} | Nota 2: {note.note2} | Recuperacion: {note.recovery} | Observacion: {note.observations}" )

    consult_notes_above_value(False, 2, 5)        

    def get_student_notes_ordered_byperiod(state, student_id):
        if state:
            notes = DetailNote.objects.filter(estudiante_id= student_id).order_by('note__period__id')
            print(f"Todas las notas del estudiante ordenadas por período:")
            for note in notes:
                print(f"Período: {note.note.period.description} | Asignatura: {note.note.asignature.description} | Nota 1: {note.note1} | Nota 2: {note.note2} | Recuperación: {note.recovery} | Observacion: {note.observations}")
    get_student_notes_ordered_byperiod(False, 3)

    def count_student_notes(state, student_id):
        if state:
            try:
                notes = DetailNote.objects.filter(estudiante_id=student_id)
                
                # Verificar qué notas se están recuperando (para propósitos de depuración)
                print(f"Notas encontradas para el estudiante con ID {student_id}: {notes}")

                # Contar las notas encontradas
                count = notes.count()
                print(f"Total de notas del estudiante {student_id}: {count}")

            except DetailNote.DoesNotExist:
                print(f"No se encontraron notas para el estudiante con ID {student_id}")

    count_student_notes(False, 1)

    def calculate_average_notes(state, student_id, period_id):
        if state:
            try:
                notes = DetailNote.objects.filter(estudiante_id=student_id, note__period_id=period_id)

                # Verificar si se encontraron notas
                if notes.exists():
                    total_notes = 0
                    notes_count = 0

                    # Sumar todas las notas
                    for note in notes:
                        total_notes += note.note1
                        total_notes += note.note2
                        if note.recovery:
                            total_notes += note.recovery
                            notes_count += 3  # contando note1, note2 y recovery
                        else:
                            notes_count += 2  # contando solo note1 y note2

                    # Calcular el promedio
                    average = total_notes / notes_count

                    # Imprimir el promedio de las notas del estudiante
                    print(f"Promedio de las notas del estudiante {student_id} en el período {period_id}: {average:.2f}")
                else:
                    print(f"No se encontraron notas para el estudiante {student_id} en el período {period_id}")

            except DetailNote.DoesNotExist:
                print(f"No se encontraron notas para el estudiante {student_id} en el período {period_id}")

    calculate_average_notes(False, 1, 1)

    def get_notes_with_specific_observation(state, observation):    #48.	Consultar todas las notas con una observación específica: 
        if state:
            notes = DetailNote.objects.filter(observations__icontains=observation)

            # Verificar si se encontraron notas
            if notes.exists():
                print(f"Notas encontradas con la observación '{observation}':")
                for note in notes:
                    print(f"Estudiante: {note.estudiante_id.full_name} | Nota 1: {note.note1} | Nota 2: {note.note2} | Recuperación: {note.recovery} | Observaciones: {note.observations}")
                    print(f"Periodo: {note.note.period.description} | Asignatura: {note.note.asignature.description} | Profesor: {note.note.teacher.first_name} {note.note.teacher.last_name}")
            else:
                print(f"No se encontraron notas con la observación '{observation}'")

    get_notes_with_specific_observation(False, 'Sigue mejorando')

    def get_student_notes_ordered_by_asignature(state, student_id):
        if state:
            # Filtrar todas las notas del estudiante por su ID y ordenarlas por asignatura
            notes = DetailNote.objects.filter(estudiante_id=student_id).order_by('note__asignature__description')

            # Verificar si se encontraron notas
            if notes.exists():
                print(f"Notas del estudiante {student_id} ordenadas por asignatura:")
                for note in notes:
                    print(f"Asignatura: {note.note.asignature.description} | Nota 1: {note.note1} | Nota 2: {note.note2} | Recuperación: {note.recovery} | Observaciones: {note.observations}")
                    print(f"Periodo: {note.note.period.description} | Profesor: {note.note.teacher.first_name} {note.note.teacher.last_name}")
            else:
                print(f"No se encontraron notas para el estudiante {student_id}")

# Ejecutar la función para obtener las notas del estudiante ordenadas por asignatura
    get_student_notes_ordered_by_asignature(False, 1)

# ---> LLAMAR A LA FUNCIÓN PARA VER SU FUNCIONALIDAD <---
consult_notes()

# SENTENCIAS UPDATE
def sentencia_update():
# ---> Actualizar nota1 para alumnos con nota1 < 20 <---
    def update_note1_student(states):
        if states:
            notas_por_actualizar = DetailNote.objects.filter(note1__lt=20)
            for detalle in notas_por_actualizar:
                detalle.note1 = 20 
                detalle.save() 
            print(f'Se actualizaron {notas_por_actualizar.count()} registros.')
    update_note1_student(False)

# ---> Actualizar nota2 para alumnos con nota2 < 15 <---
    def update_note2_student(states):
        if states:
            notas_por_actualizar = DetailNote.objects.filter(note2__lt=15)
            for detalle in notas_por_actualizar:
                detalle.note2 = 15 
                detalle.save() 
            print(f'Se actualizaron {notas_por_actualizar.count()} registros.')
    update_note2_student(False)

# --->  Actualizar recuperación para alumnos con recuperación < 10 <---
    def update_recuperacion_student(states):
        if states:
            notas_por_actualizar = DetailNote.objects.filter(recovery__lt=10)
            for detalle in notas_por_actualizar:
                detalle.recovery = 10 
                detalle.save() 
            print(f'Se actualizaron {notas_por_actualizar.count()} registros.')
    update_recuperacion_student(False)

    def update_observations_student(states):
    # Actualizar observación para alumnos que hayan aprobado:
        if states:
            notas_por_actualizar = DetailNote.objects.filter(note1__gte=20, note2__gte=15)
            # Iterar sobre cada detalle de nota y actualizar observación
            for detalle in notas_por_actualizar:
                detalle.observations = 'Aprobado'  # Actualizar observación a 'Aprobado'
                detalle.save()  # Guardar el cambio en la base de datos
            print(f'Se actualizaron {notas_por_actualizar.count()} registros.')
    update_observations_student(False)

    # Obtener todos los detalles de notas de un período específico
    def update_notes_period(states):
        if states:
            notas_por_actualizar = DetailNote.objects.filter(note__period_id=1)
            # Iterar sobre cada detalle de nota y eliminarlo
            for detalle in notas_por_actualizar:
                detalle.delete()  # Eliminar el detalle de nota
            print(f'Se eliminaron {notas_por_actualizar.count()} registros.')
    update_notes_period(False)    

# ---> LLAMAR A LA FUNCIÓN PARA VER SU FUNCIONALIDAD <---
sentencia_update()

# SENTENCIAS UPDATE
def sentencia_delete():
    # Eliminar físicamente todas las notas de un estudiante:
    def delete_notes_physics_student(states):
        if states:
            notas_por_eliminar = DetailNote.objects.filter(estudiante_id=1)
            # Iterar sobre cada detalle de nota y eliminarlo
            for detalle in notas_por_eliminar:
                detalle.delete()  # Eliminar el detalle de nota
            print(f'Se eliminaron {notas_por_eliminar.count()} registros.')
            
    delete_notes_physics_student(False)
    
    # Eliminar lógicamente todas las notas de un estudiante (en el campo state que indica si el registro está activo o no):
    def delete_notes_logic_student(states):
        if states:
            notas_por_eliminar = DetailNote.objects.filter(estudiante_id=1, state=True)
            # Iterar sobre cada detalle de nota y eliminarlo
            for detalle in notas_por_eliminar:
                detalle.delete()  # Eliminar el detalle de nota
            print(f'Se eliminaron {notas_por_eliminar.count()} registros.')
    
    delete_notes_logic_student(False)
    
    # Eliminar físicamente todas las notas de un período específico
    def delete_notes_period_physics_student(states):
        if states:
            notas_por_eliminar = DetailNote.objects.filter(note__period_id=1)
            # Iterar sobre cada detalle de nota y eliminarlo
            for detalle in notas_por_eliminar:
                detalle.delete()  # Eliminar el detalle de nota
            print(f'Se eliminaron {notas_por_eliminar.count()} registros.')
    
    delete_notes_period_physics_student(False)    
    
    # Eliminar lógicamente todas las notas de un período específico:
    def delete_notes_period_logic_student(states):
        if states:
            notas_por_eliminar = DetailNote.objects.filter(note__period_id=1, state=True)
            # Iterar sobre cada detalle de nota y eliminarlo
            for detalle in notas_por_eliminar:
                detalle.delete()  # Eliminar el detalle de nota
            print(f'Se eliminaron {notas_por_eliminar.count()} registros.')
    delete_notes_period_logic_student(False)
        
    # Eliminar físicamente todas las notas que tengan una nota1 menor a 10:
    def delete_notes_logic(states):
        if states:
            notas_por_eliminar = DetailNote.objects.filter(note1__lt=10)
            # Iterar sobre cada detalle de nota y eliminarlo
            for detalle in notas_por_eliminar:
                detalle.delete()  # Eliminar el detalle de nota
            print(f'Se eliminaron {notas_por_eliminar.count()} registros.')
    delete_notes_logic(False)

# ---> LLAMAR A LA FUNCIÓN PARA VER SU FUNCIONALIDAD <---
sentencia_delete()

# Crea un registro de notas de un estudiante, simulando una inserción de los 
# datos tal como se explicó en el ejercicio de la creación de una factura con su 
# detalle de productos en el archivo orm.py de la clase impartida.

# Llamar a la función para crear el registro de notas para un estudiante específico
# 60. Crear un registro de notas de un estudiante:
def modificar_notas_estudiante(estudiante_id, nota1, nota2, recuperacion, observacion):
    try:
        # Obtener el estudiante
        estudiante = Student.objects.get(pk=estudiante_id)
        
        # Obtener la nota existente del estudiante (suponemos que solo hay una nota por estudiante)
        detalle_nota = DetailNote.objects.filter(estudiante_id=estudiante).first()

        if not detalle_nota:
            print(f"No se encontraron detalles de nota para el estudiante {estudiante.full_name()}")
            return
        # Actualizar los valores de la nota existente
        detalle_nota.note1 = nota1
        detalle_nota.note2 = nota2
        detalle_nota.recovery = recuperacion
        detalle_nota.observations = observacion
        detalle_nota.updated = timezone.now()
        detalle_nota.save()

        print(f'Notas actualizadas para el estudiante {estudiante.full_name()}')

    except Student.DoesNotExist:
        print(f"No se encontró el estudiante con id {estudiante_id}")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")

# # Ejemplo de cómo llamar a la función para modificar las notas de un estudiante
modificar_notas_estudiante(2, 10, 8.0, 10, "Mejoró en la recuperación")

# def cambiar_nombre_apellido_estudiante(estudiante_id, nuevo_nombre, nuevo_apellido):
#     try:
#         # Obtener el estudiante por su ID
#         estudiante = Student.objects.get(pk=estudiante_id)
        
#         # Actualizar nombre y apellido
#         estudiante.first_name = nuevo_nombre
#         estudiante.last_name = nuevo_apellido
    
#         # Guardar los cambios en la base de datos
#         estudiante.save()
#         print(f'Nombre y apellido actualizados para el estudiante {estudiante.full_name()}')

#     except Student.DoesNotExist:
#         print(f"No se encontró el estudiante con ID {estudiante_id}")
#     except Exception as e:
#         print(f"Ha ocurrido un error: {e}")

# # Ejemplo de cómo llamar a la función para cambiar nombre y apellido
# cambiar_nombre_apellido_estudiante(10, "Estefania", "Zuñiga")