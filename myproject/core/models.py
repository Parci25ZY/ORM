from django.db import models
from django.contrib.auth.models import User
from myproject.utils import valida_cedula

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state=True)

class GeneralDelete(models.Model):
    state   = models.BooleanField(default = True)
    user    = models.ForeignKey(User, on_delete  =models.CASCADE)
    created = models.DateField(auto_now_add = True)
    updated = models.DateField(auto_now = True)
    objects = models.Manager()
    active_objects = ActiveManager()

    def delete(self):
        self.state = False
        self.save()

    class Meta:
        abstract = True

class Period(GeneralDelete):
    description = models.CharField(max_length=50)
    start_date  = models.DateField()
    end_date    = models.DateField()
    
    def __str__(self):
        return self.description

class Asignature(GeneralDelete):
    description = models.CharField(max_length=150)

    class Meta:
        ordering = ['description']
        verbose_name = 'Asignature'
        verbose_name_plural = 'Asignatures'

    def __str__(self):
        return self.description

class Teacher(GeneralDelete):
    cedula     = models.CharField(max_length=10, unique=True, validators=[valida_cedula])
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)

    objects = models.Manager()
    active_teachers = ActiveManager()

    class Meta:
        ordering = ["first_name"]
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()

class Student(GeneralDelete):
    cedula     = models.CharField(max_length=10, unique=True, validators=[valida_cedula])
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)

    class Meta:
        ordering = ["first_name"]
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()

class Note(GeneralDelete):
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name="notes")
    #Cuando se elimine un profesor on_delete=models.CASCADE hace que seelimines todas las notas 
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="notes")
    asignature = models.ForeignKey(Asignature, on_delete=models.CASCADE, related_name="notes")

    class Meta:
        ordering = ['period', 'teacher', 'asignature']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    def __str__(self):
        return f"Period: {self.period}, Teacher: {self.teacher}, Asignature: {self.asignature}"

class DetailNote(GeneralDelete):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="Notas", null=True)
    estudiante_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_detail", null=True)
    note1 = models.DecimalField(max_digits=5, decimal_places=2)
    note2 = models.DecimalField(max_digits=5, decimal_places=2)
    recovery = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    observations = models.TextField()

    class Meta:
        ordering = ['recovery']
        verbose_name = 'DetailNote'
        verbose_name_plural = 'DetailNotes'

    def __str__(self):
        return f"note: {self.note}, student: {self.estudiante_id},Note 1: {self.note1}, Note 2: {self.note2}, Recovery: {self.recovery}, Observations: {self.observations}"



