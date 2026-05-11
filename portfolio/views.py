from django.shortcuts import render
from .models import (
    Tecnologia, Projeto, UnidadeCurricular, 
    TFC, Competencia, Formacao, Licenciatura, Docente
)

def home_portfolio(request):
    return render(request, 'portfolio/home.html')

def tecnologias_view(request):
    tecnologias = Tecnologia.objects.all().order_by('-classificacao')
    return render(request, 'portfolio/tecnologias.html', {'tecnologias': tecnologias})

def projetos_view(request):
    projetos = Projeto.objects.all().order_by('-data')
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})

def unidades_view(request):
    unidades = UnidadeCurricular.objects.all().order_by('semestre', 'ano')
    return render(request, 'portfolio/unidades.html', {'unidades': unidades})

def tfc_view(request):
    tfcs = TFC.objects.select_related('orientador', 'licenciatura').prefetch_related('tecnologia', 'area').all()
    return render(request, 'portfolio/tfc.html', {'tfcs': tfcs})

def competencias_view(request):
    competencias = Competencia.objects.all().order_by('-nivel')
    return render(request, 'portfolio/competencias.html', {'competencias': competencias})

def formacoes_view(request):
    formacoes = Formacao.objects.all().order_by('-data_fim')
    return render(request, 'portfolio/formacoes.html', {'formacoes': formacoes})

def licenciaturas_view(request):
    licenciaturas = Licenciatura.objects.all().order_by('nome')
    return render(request, 'portfolio/licenciaturas.html', {'licenciaturas': licenciaturas})
