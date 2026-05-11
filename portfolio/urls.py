from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_portfolio, name='home_portfolio'),
    path('tecnologias/', views.tecnologias_view, name='tecnologias'),
    path('projetos/', views.projetos_view, name='projetos'),
    path('unidades-curriculares/', views.unidades_view, name='unidades'),
    path('tfc/', views.tfc_view, name='tfc'),
    path('competencias/', views.competencias_view, name='competencias'),
    path('formacoes/', views.formacoes_view, name='formacoes'),
    path('licenciaturas/', views.licenciaturas_view, name='licenciaturas'),
]