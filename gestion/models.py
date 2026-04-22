# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuditoriaEvaluaciones(models.Model):
    auditoria_id = models.AutoField(primary_key=True)
    evaluacion_id = models.IntegerField(blank=True, null=True)
    accion = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    inscripcion_id = models.IntegerField(blank=True, null=True)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fecha_evaluacion = models.DateField(blank=True, null=True)
    fecha_auditoria = models.DateTimeField(blank=True, null=True)
    usuario_bd = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Auditoria_Evaluaciones'


class AuditoriaInscripciones(models.Model):
    auditoria_id = models.AutoField(primary_key=True)
    inscripcion_id = models.IntegerField(blank=True, null=True)
    accion = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    estudiante_id = models.IntegerField(blank=True, null=True)
    curso_id = models.IntegerField(blank=True, null=True)
    instructor_id = models.IntegerField(blank=True, null=True)
    fecha_inscripcion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    total_pago = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_auditoria = models.DateTimeField(blank=True, null=True)
    usuario_bd = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Auditoria_Inscripciones'


class AuditoriaPagos(models.Model):
    auditoria_id = models.AutoField(primary_key=True)
    pago_id = models.IntegerField(blank=True, null=True)
    accion = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    inscripcion_id = models.IntegerField(blank=True, null=True)
    fecha_pago = models.DateField(blank=True, null=True)
    metodo_pago = models.CharField(max_length=30, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado_pago = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    fecha_auditoria = models.DateTimeField(blank=True, null=True)
    usuario_bd = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Auditoria_Pagos'


class Cursos(models.Model):
    curso_id = models.IntegerField(primary_key=True)
    nombre_curso = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    categoria = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    duracion_horas = models.IntegerField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cupo_maximo = models.IntegerField(blank=True, null=True)
    cupo_disponible = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Cursos'


class DetallePagos(models.Model):
    detalle_id = models.IntegerField(primary_key=True)
    pago = models.ForeignKey('Pagos', models.DO_NOTHING, blank=True, null=True)
    concepto = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Detalle_Pagos'


class Estudiantes(models.Model):
    estudiante_id = models.IntegerField(primary_key=True)
    nombre_completo = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    telefono = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    direccion = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    tipo_documento = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    numero_documento = models.BinaryField(blank=True, null=True)
    fecha_registro = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Estudiantes'


class Evaluaciones(models.Model):
    evaluacion_id = models.IntegerField(primary_key=True)
    inscripcion = models.ForeignKey('Inscripciones', models.DO_NOTHING, blank=True, null=True)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    comentarios = models.BinaryField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Evaluaciones'


class Inscripciones(models.Model):
    inscripcion_id = models.IntegerField(primary_key=True)
    estudiante = models.ForeignKey(Estudiantes, models.DO_NOTHING, blank=True, null=True)
    curso = models.ForeignKey(Cursos, models.DO_NOTHING, blank=True, null=True)
    instructor = models.ForeignKey('Instructores', models.DO_NOTHING, blank=True, null=True)
    fecha_inscripcion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    total_pago = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Inscripciones'


class Instructores(models.Model):
    instructor_id = models.IntegerField(primary_key=True)
    nombre_completo = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    especialidad = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    cedula_profesional = models.BinaryField(blank=True, null=True)
    usuario = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    contrasena = models.BinaryField(blank=True, null=True)
    estado = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Instructores'


class Logerrores(models.Model):
    error_id = models.AutoField(primary_key=True)
    procedimiento = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    mensaje_error = models.CharField(max_length=4000, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    numero_error = models.IntegerField(blank=True, null=True)
    severidad = models.IntegerField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    linea = models.IntegerField(blank=True, null=True)
    fecha_error = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LogErrores'


class Pagos(models.Model):
    pago_id = models.IntegerField(primary_key=True)
    inscripcion = models.ForeignKey(Inscripciones, models.DO_NOTHING, blank=True, null=True)
    fecha_pago = models.DateField(blank=True, null=True)
    metodo_pago = models.CharField(max_length=30, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    referencia_pago = models.BinaryField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado_pago = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Pagos'
