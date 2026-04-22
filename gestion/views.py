from datetime import datetime
import json
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.http import HttpResponse

# ==========================================
# 🛡️ VISTAS DE ACCESO Y SESIÓN
# ==========================================
def login_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT estudiante_id, nombre_completo FROM Estudiantes")
        alumnos = [{'id': r[0], 'nombre': r[1]} for r in cursor.fetchall()]
        
        cursor.execute("SELECT admin_id, nombre_completo FROM Administradores")
        admins = [{'id': r[0], 'nombre': r[1]} for r in cursor.fetchall()]

        cursor.execute("SELECT instructor_id, nombre_completo FROM Instructores WHERE estado = 'Activo'")
        profesores = [{'id': r[0], 'nombre': r[1]} for r in cursor.fetchall()]

    if request.method == 'POST':
        tipo = request.POST.get('tipo_usuario')
        id_selec = request.POST.get('usuario_id')
        nombre_selec = request.POST.get('nombre_oculto')

        request.session['rol'] = tipo
        request.session['nombre'] = nombre_selec
        request.session['usuario_id'] = id_selec

        if tipo == 'alumno':
            return redirect('vista_alumno')
        elif tipo == 'instructor':
            return redirect('vista_profesor')
        else:
            return redirect('dashboard')

    return render(request, 'gestion/login.html', {
        'alumnos': alumnos, 
        'admins': admins, 
        'profesores': profesores
    })

def logout_view(request):
    request.session.flush()
    return redirect('login')

# ==========================================
# 👔 VISTAS DEL ADMINISTRADOR
# ==========================================
def dashboard(request):
    if request.session.get('rol') != 'admin':
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute("EXEC ReporteGeneralSistema")
        columnas = [col[0] for col in cursor.description]
        reporte = [dict(zip(columnas, row)) for row in cursor.fetchall()]
    
    return render(request, 'gestion/dashboard.html', {'reporte': reporte})

def registrar_estudiante(request):
    if request.session.get('rol') != 'admin':
        return redirect('login')

    with connection.cursor() as cursor:
        # --- PARTE 1: PROCESAR EL REGISTRO (POST) ---
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            email = request.POST.get('email')
            telefono = request.POST.get('telefono')
            direccion = request.POST.get('direccion')
            tipo_doc = request.POST.get('tipo_doc')
            num_doc = request.POST.get('num_doc')

            try:
                # Usamos tu Procedure original para mantener el cifrado AES_256
                cursor.execute(
                    "EXEC RegistrarEstudiante %s, %s, %s, %s, %s, %s",
                    [nombre, email, telefono, direccion, tipo_doc, num_doc]
                )
                connection.commit()
                messages.success(request, f"¡Estudiante {nombre} registrado con éxito!")
                return redirect('registrar_estudiante')
            except Exception as e:
                messages.error(request, f"Error al registrar: {str(e)}")

        # --- PARTE 2: TRAER LA LISTA PARA LA TABLA (GET) ---
        # Esto es lo que permite que se llene la tabla de abajo en tu HTML
        cursor.execute("SELECT estudiante_id, nombre_completo, email FROM Estudiantes ORDER BY estudiante_id DESC")
        alumnos = [dict(zip(['id', 'nombre', 'email'], r)) for r in cursor.fetchall()]

    # El return render debe estar AL FINAL y fuera de cualquier IF
    return render(request, 'gestion/registro.html', {'lista_estudiantes': alumnos})

def registrar_admin(request):
    if request.session.get('rol') != 'admin':
        messages.error(request, "Acceso denegado.")
        return redirect('login')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Administradores (nombre_completo, email) VALUES (%s, %s)", [nombre, email])
        return redirect('login')
    return render(request, 'gestion/registro_admin.html')

def inscribir_curso(request):
    if request.session.get('rol') != 'admin': 
        return redirect('login')

    with connection.cursor() as cursor:
        if request.method == 'POST':
            accion = request.POST.get('accion')
            
            if accion == 'inscribir':
                est_id = request.POST.get('estudiante_id')
                cur_id = request.POST.get('curso_id')
                inst_id = request.POST.get('instructor_id')
                monto = request.POST.get('monto')
                metodo = request.POST.get('metodo_pago')
                ref = request.POST.get('referencia')
                try:
                    cursor.execute(
                        "EXEC ProcesoCompletoInscripcion %s, %s, %s, %s, %s, %s, %s, %s, %s",
                        [est_id, cur_id, inst_id, monto, 0, 'Inscripción desde Web', metodo, ref, monto]
                    )
                    connection.commit()
                    messages.success(request, "¡Inscripción registrada con éxito!")
                except Exception as e:
                    messages.error(request, f"Error: {str(e)}")
                    
            elif accion == 'eliminar':
                insc_id = request.POST.get('inscripcion_id')
                try:
                    cursor.execute("DELETE FROM Inscripciones WHERE inscripcion_id = %s", [insc_id])
                    connection.commit()
                    messages.warning(request, "Alumno dado de baja del curso exitosamente.")
                except Exception as e:
                    messages.error(request, f"No se pudo eliminar: {str(e)}")
                    
            return redirect('inscribir_curso')

        cursor.execute("SELECT estudiante_id, nombre_completo FROM Estudiantes WHERE estado = 'Activo'")
        estudiantes = [{'id': r[0], 'nombre': r[1]} for r in cursor.fetchall()]
        
        cursor.execute("SELECT curso_id, nombre_curso, costo FROM Cursos WHERE estado = 'Activo'")
        cursos = [{'id': r[0], 'nombre': r[1], 'costo': r[2]} for r in cursor.fetchall()]
        
        cursor.execute("SELECT instructor_id, nombre_completo FROM Instructores WHERE estado = 'Activo'")
        instructores = [{'id': r[0], 'nombre': r[1]} for r in cursor.fetchall()]

        cursor.execute("""
            SELECT i.inscripcion_id, e.nombre_completo, c.nombre_curso, i.fecha_inscripcion 
            FROM Inscripciones i
            JOIN Estudiantes e ON i.estudiante_id = e.estudiante_id
            JOIN Cursos c ON i.curso_id = c.curso_id
            ORDER BY i.fecha_inscripcion DESC
        """)
        inscripciones = [dict(zip(['id', 'alumno', 'curso', 'fecha'], r)) for r in cursor.fetchall()]

    return render(request, 'gestion/inscripcion.html', {
        'estudiantes': estudiantes, 'cursos': cursos, 'instructores': instructores, 'inscripciones_activas': inscripciones
    })

def graficas_gestion(request):
    if request.session.get('rol') != 'admin':
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute("EXEC RankingCursosMasPopulares")
        ranking = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        
        cursor.execute("EXEC ReporteInscripcionesPorMes")
        inscripciones_mes = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

    context = {
        'nombres_cursos': json.dumps([r['nombre_curso'] for r in ranking]),
        'totales_cursos': json.dumps([r['total_inscripciones'] for r in ranking]),
        'meses_data': json.dumps(list(inscripciones_mes[0].values())[1:] if inscripciones_mes else [0]*12)
    }
    return render(request, 'gestion/graficas.html', context)

def ver_auditoria(request):
    if request.session.get('rol') != 'admin':
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute("SELECT TOP 50 * FROM Auditoria_Inscripciones ORDER BY fecha_auditoria DESC")
        logs = [dict(zip([c[0] for c in cursor.description], r)) for r in cursor.fetchall()]
        
        cursor.execute("SELECT TOP 20 * FROM LogErrores ORDER BY fecha_error DESC")
        errores = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

    return render(request, 'gestion/auditoria.html', {'auditoria': logs, 'errores': errores})

# ==========================================
# 👨‍🏫 VISTAS DEL PROFESOR
# ==========================================
def vista_profesor(request):
    if request.session.get('rol') not in ['instructor', 'admin']:
        return redirect('login')

    profesor_id = request.session.get('usuario_id')

    with connection.cursor() as cursor:
        cursor.execute("SELECT curso_id, nombre_curso FROM Cursos WHERE instructor_titular_id = %s", [profesor_id])
        mis_cursos = [dict(zip([c[0] for c in cursor.description], r)) for r in cursor.fetchall()]
        
        cursor.execute("""
            SELECT DISTINCT e.estudiante_id, e.nombre_completo, e.email 
            FROM Estudiantes e
            JOIN Inscripciones i ON e.estudiante_id = i.estudiante_id
            JOIN Cursos c ON i.curso_id = c.curso_id
            WHERE c.instructor_titular_id = %s
        """, [profesor_id])
        mis_alumnos = [dict(zip([c[0] for c in cursor.description], r)) for r in cursor.fetchall()]

        cursor.execute("SELECT remitente, mensaje, fecha FROM Notificaciones WHERE receptor_id = %s AND rol_receptor = 'instructor' ORDER BY fecha DESC", [profesor_id])
        notificaciones = [dict(zip([c[0] for c in cursor.description], r)) for r in cursor.fetchall()]

    if request.method == 'POST':
        accion = request.POST.get('accion')
        with connection.cursor() as cursor:
            if accion == 'subir_actividad':
                try:
                    cursor.execute(
                        "INSERT INTO Actividades (titulo, descripcion, fecha_entrega, curso_id) VALUES (%s, %s, %s, %s)",
                        [request.POST.get('titulo'), request.POST.get('desc'), request.POST.get('fecha'), request.POST.get('curso_id')]
                    )
                    connection.commit() 
                    messages.success(request, "¡Tarea guardada! Entra al curso para verla.")
                except Exception as e:
                    messages.error(request, f"Error al guardar en BD: {str(e)}")

        return redirect('vista_profesor')

    return render(request, 'gestion/profesor.html', {
        'cursos': mis_cursos, 
        'alumnos': mis_alumnos, 
        'notificaciones': notificaciones
    })


def detalle_curso(request, curso_id):
    if request.session.get('rol') not in ['instructor', 'admin']:
        return redirect('login')

    profesor_id = request.session.get('usuario_id')

    with connection.cursor() as cursor:
        # 1. Info del curso
        cursor.execute("""
            SELECT curso_id, nombre_curso, costo, estado 
            FROM Cursos 
            WHERE curso_id = %s AND instructor_titular_id = %s
        """, [curso_id, profesor_id])
        row = cursor.fetchone()
        
        if not row:
            messages.error(request, "No tienes permiso para ver este curso.")
            return redirect('vista_profesor')
            
        curso_info = {'curso_id': row[0], 'nombre_curso': row[1], 'costo': row[2], 'estado': row[3]}

        # 2. Actividades de la materia
        cursor.execute("SELECT titulo, descripcion, fecha_entrega FROM Actividades WHERE curso_id = %s ORDER BY fecha_entrega ASC", [curso_id])
        actividades = [dict(zip([col[0] for col in cursor.description], r)) for r in cursor.fetchall()]

        # 3. Alumnos inscritos EN ESTA MATERIA específicamente
        cursor.execute("""
            SELECT e.estudiante_id, e.nombre_completo, e.email 
            FROM Estudiantes e
            JOIN Inscripciones i ON e.estudiante_id = i.estudiante_id
            WHERE i.curso_id = %s
        """, [curso_id])
        alumnos_curso = [dict(zip([col[0] for col in cursor.description], r)) for r in cursor.fetchall()]

        # 4. Procesar Formularios (Subir tarea, Configuración, y CALIFICACIONES)
        if request.method == 'POST':
            accion = request.POST.get('accion')
            
            if accion == 'subir_actividad':
                try:
                    fecha_cruda = request.POST.get('fecha')
                    fecha_sql = fecha_cruda.replace('T', ' ') if fecha_cruda else None
                    
                    cursor.execute(
                        "INSERT INTO Actividades (titulo, descripcion, fecha_entrega, curso_id) VALUES (%s, %s, %s, %s)",
                        [request.POST.get('titulo'), request.POST.get('desc'), fecha_sql, curso_id]
                    )
                    connection.commit() 
                    messages.success(request, "Actividad publicada exitosamente.")
                except Exception as e:
                    messages.error(request, f"Error al guardar la actividad: {str(e)}")
                
            elif accion == 'actualizar_config':
                try:
                    cursor.execute(
                        "UPDATE Cursos SET nombre_curso = %s, estado = %s WHERE curso_id = %s",
                        [request.POST.get('nombre_curso'), request.POST.get('estado'), curso_id]
                    )
                    connection.commit()
                    messages.success(request, "Configuración del curso guardada.")
                except Exception as e:
                    messages.error(request, f"Error al actualizar: {str(e)}")

            # --- NUEVA LÓGICA DE FASE 2: CALIFICAR Y NOTIFICAR ---
            elif accion == 'guardar_calificaciones':
                try:
                    cursor.execute("SELECT inscripcion_id, estudiante_id FROM Inscripciones WHERE curso_id = %s", [curso_id])
                    inscripciones = cursor.fetchall()
                    
                    for insc in inscripciones:
                        insc_id = insc[0]
                        est_id = insc[1]
                        nota = request.POST.get(f'nota_{est_id}')
                        
                        if nota: # Si el profesor escribió una calificación para este alumno
                            cursor.execute("""
                                IF EXISTS (SELECT 1 FROM Evaluaciones WHERE inscripcion_id = %s)
                                    UPDATE Evaluaciones SET calificacion = %s WHERE inscripcion_id = %s
                                ELSE
                                    INSERT INTO Evaluaciones (inscripcion_id, calificacion) VALUES (%s, %s)
                            """, [insc_id, nota, insc_id, insc_id, nota])
                            
                            mensaje = f"Tu profesor ha registrado una calificación de {nota} en el curso {curso_info['nombre_curso']}."
                            cursor.execute("""
                                INSERT INTO Notificaciones (remitente, receptor_id, rol_receptor, mensaje, fecha)
                                VALUES ('Sistema Académico', %s, 'alumno', %s, GETDATE())
                            """, [est_id, mensaje])
                            
                    connection.commit()
                    messages.success(request, "¡Calificaciones guardadas y alumnos notificados!")
                except Exception as e:
                    messages.error(request, f"Error al guardar notas: {str(e)}")
                
            return redirect('detalle_curso', curso_id=curso_id)

    return render(request, 'gestion/detalle_curso.html', {
        'curso': curso_info,
        'actividades': actividades,
        'alumnos_curso': alumnos_curso
    })

def editar_calificacion(request, evaluacion_id):
    if request.session.get('rol') not in ['instructor', 'admin']:
        return redirect('login')

    if request.method == 'POST':
        nueva_nota = request.POST.get('nota')
        with connection.cursor() as cursor:
            cursor.execute("UPDATE Evaluaciones SET calificacion = %s WHERE evaluacion_id = %s", [nueva_nota, evaluacion_id])
            messages.success(request, "Calificación actualizada.")
        return redirect('dashboard')

# ==========================================
# 🎓 VISTAS DEL ALUMNO Y PDFs
# ==========================================
def vista_alumno(request):
    if request.session.get('rol') != 'alumno':
        return redirect('login')

    usuario_id = request.session.get('usuario_id')
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.curso_id, c.nombre_curso, c.estado
            FROM Inscripciones i
            JOIN Cursos c ON i.curso_id = c.curso_id
            WHERE i.estudiante_id = %s
        """, [usuario_id])
        mis_cursos = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

    return render(request, 'gestion/alumno.html', {'cursos': mis_cursos})

def detalle_curso_alumno(request, curso_id):
    if request.session.get('rol') != 'alumno':
        return redirect('login')
        
    usuario_id = request.session.get('usuario_id')
    
    with connection.cursor() as cursor:
        # 1. Validar acceso y obtener el ID de Inscripción
        cursor.execute("SELECT inscripcion_id FROM Inscripciones WHERE estudiante_id = %s AND curso_id = %s", [usuario_id, curso_id])
        insc = cursor.fetchone()
        if not insc:
            messages.error(request, "No tienes acceso a este curso.")
            return redirect('vista_alumno')
            
        inscripcion_id = insc[0]

        # 2. PROCESAR LA SUBIDA DE TAREA (POST)
        if request.method == 'POST':
            accion = request.POST.get('accion')
            if accion == 'subir_entrega':
                titulo_tarea = request.POST.get('titulo_tarea')
                # Aquí guardarías el archivo en tu servidor o BD. 
                # Por ahora, simulamos el éxito de la recepción:
                messages.success(request, f"¡Tu entrega para '{titulo_tarea}' se envió correctamente al profesor!")
                return redirect('detalle_curso_alumno', curso_id=curso_id)

        # 3. GET: Info del curso
        cursor.execute("""
            SELECT c.curso_id, c.nombre_curso, i.nombre_completo 
            FROM Cursos c
            JOIN Instructores i ON c.instructor_titular_id = i.instructor_id
            WHERE c.curso_id = %s
        """, [curso_id])
        row = cursor.fetchone()
        curso_info = {'curso_id': row[0], 'nombre_curso': row[1], 'instructor': row[2]}
        
        # 4. GET: Actividades
        cursor.execute("SELECT titulo, descripcion, fecha_entrega FROM Actividades WHERE curso_id = %s ORDER BY fecha_entrega ASC", [curso_id])
        actividades = [dict(zip(['titulo', 'descripcion', 'fecha_entrega'], r)) for r in cursor.fetchall()]

        # 5. GET: Libro de Calificaciones
        cursor.execute("SELECT calificacion FROM Evaluaciones WHERE inscripcion_id = %s", [inscripcion_id])
        nota = cursor.fetchone()
        mi_calificacion = nota[0] if nota else "Aún no calificado"

        # 6. GET: Anuncios (Notificaciones)
        cursor.execute("SELECT remitente, mensaje, fecha FROM Notificaciones WHERE receptor_id = %s AND rol_receptor = 'alumno' ORDER BY fecha DESC", [usuario_id])
        anuncios = [dict(zip(['remitente', 'mensaje', 'fecha'], r)) for r in cursor.fetchall()]
        
    return render(request, 'gestion/detalle_curso_alumno.html', {
        'curso': curso_info, 
        'actividades': actividades,
        'mi_calificacion': mi_calificacion,
        'anuncios': anuncios
    })

def descargar_boleta_pdf(request):
    usuario_id = request.session.get('usuario_id')
    with connection.cursor() as cursor:
        cursor.execute("OPEN SYMMETRIC KEY ClavePlataforma DECRYPTION BY CERTIFICATE CertificadoPlataforma")
        cursor.execute("""
            SELECT c.nombre_curso, ev.calificacion, 
                ISNULL(CONVERT(VARCHAR(MAX), DecryptByKey(ev.comentarios)), 'Sin observaciones') as comentarios
            FROM Inscripciones i
            JOIN Cursos c ON i.curso_id = c.curso_id
            JOIN Evaluaciones ev ON i.inscripcion_id = ev.inscripcion_id
            WHERE i.estudiante_id = %s
        """, [usuario_id])
        
        notas = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        cursor.execute("CLOSE SYMMETRIC KEY ClavePlataforma")

    context = {'notas': notas, 'nombre': request.session.get('nombre'), 'fecha': datetime.now()}
    return render(request, 'gestion/pdf_boleta.html', context)

def descargar_reporte_cursos_pdf(request):
    if request.session.get('rol') != 'admin':
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute("EXEC RankingCursosMasPopulares")
        ranking = [dict(zip([c[0] for c in cursor.description], row)) for row in cursor.fetchall()]

    context = {'ranking': ranking, 'fecha': datetime.now(), 'admin_nombre': request.session.get('nombre')}
    return render(request, 'gestion/pdf_reporte_cursos.html', context)

def eliminar_estudiante(request, estudiante_id):
    if request.session.get('rol') != 'admin':
        return redirect('login')
        
    with connection.cursor() as cursor:
        try:
            # Gracias a la CASCADA que activamos en SQL Server, esto borra todo el rastro
            cursor.execute("DELETE FROM Estudiantes WHERE estudiante_id = %s", [estudiante_id])
            connection.commit()
            messages.success(request, "Perfil del estudiante y todo su historial eliminados permanentemente.")
        except Exception as e:
            messages.error(request, f"No se pudo eliminar al estudiante: {str(e)}")
            
    return redirect('registrar_estudiante')