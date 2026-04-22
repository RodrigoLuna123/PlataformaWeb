from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    path('admin_django/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Vistas de Administrador
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registro/', views.registrar_estudiante, name='registrar_estudiante'),
    path('inscripcion/', views.inscribir_curso, name='inscribir_curso'),
    path('graficas/', views.graficas_gestion, name='graficas'),
    path('auditoria/', views.ver_auditoria, name='auditoria'),
    path('registro_admin/', views.registrar_admin, name='registrar_admin'),
    path('reporte_cursos_pdf/', views.descargar_reporte_cursos_pdf, name='pdf_reporte_cursos'),

    # Vistas de Profesor
    path('profesor/', views.vista_profesor, name='vista_profesor'),
    path('curso/<int:curso_id>/', views.detalle_curso, name='detalle_curso'),

    # Vistas de Alumno
    path('alumno/', views.vista_alumno, name='vista_alumno'),
    path('mi_curso/<int:curso_id>/', views.detalle_curso_alumno, name='detalle_curso_alumno'),
    path('pdf_boleta/', views.descargar_boleta_pdf, name='descargar_pdf'),
    path('eliminar_estudiante/<int:estudiante_id>/', views.eliminar_estudiante, name='eliminar_estudiante'),
]