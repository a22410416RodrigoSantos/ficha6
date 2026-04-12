from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'semestres', 'ects')
    search_fields = ('nome',)
    list_filter = ('semestres',)

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    filter_horizontal = ('disciplina',)

@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'classificacao')
    search_fields = ('nome', 'tipo')
    list_filter = ('tipo',)

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data')
    search_fields = ('titulo',)
    list_filter = ('data',)

@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ects')
    search_fields = ('nome',)

@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'aluno', 'orientador')
    search_fields = ('titulo',)

@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nivel')
    search_fields = ('nome', 'tipo')
    list_filter = ('nivel',)

@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'instituicao')
    search_fields = ('titulo', 'instituicao')
    list_filter = ('tipo',)

@admin.register(MakingOFF)
class MakingOFFAdmin(admin.ModelAdmin):
    list_display = ('uso_ia',)
    list_filter = ('uso_ia',)