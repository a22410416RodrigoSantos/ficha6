from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_portfolio, name='home_portfolio'),
    
    # Listagens
    path('tecnologias/', views.tecnologias_view, name='tecnologias'),
    path('projetos/', views.projetos_view, name='projetos'),
    path('unidades-curriculares/', views.unidades_view, name='unidades'),
    path('tfc/', views.tfc_view, name='tfc'),
    path('competencias/', views.competencias_view, name='competencias'),
    path('formacoes/', views.formacoes_view, name='formacoes'),
    path('licenciaturas/', views.licenciaturas_view, name='licenciaturas'),
    
    # CRUD Projetos
    path('projetos/novo/', views.projeto_create, name='projeto_create'),
    path('projetos/<int:pk>/editar/', views.projeto_update, name='projeto_update'),
    path('projetos/<int:pk>/apagar/', views.projeto_delete, name='projeto_delete'),
    
    # CRUD Tecnologia
    path('tecnologias/novo/', views.tecnologia_create, name='tecnologia_create'),
    path('tecnologias/<int:pk>/editar/', views.tecnologia_update, name='tecnologia_update'),
    path('tecnologias/<int:pk>/apagar/', views.tecnologia_delete, name='tecnologia_delete'),
    
    # CRUD Competencia
    path('competencias/novo/', views.competencia_create, name='competencia_create'),
    path('competencias/<int:pk>/editar/', views.competencia_update, name='competencia_update'),
    path('competencias/<int:pk>/apagar/', views.competencia_delete, name='competencia_delete'),
    
    # CRUD Formacao
    path('formacoes/novo/', views.formacao_create, name='formacao_create'),
    path('formacoes/<int:pk>/editar/', views.formacao_update, name='formacao_update'),
    path('formacoes/<int:pk>/apagar/', views.formacao_delete, name='formacao_delete'),
]