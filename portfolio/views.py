from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Tecnologia, Projeto, UnidadeCurricular, TFC,
    Competencia, Formacao, Licenciatura
)
from .forms import (    
    ProjetoForm, 
    TecnologiaForm, 
    CompetenciaForm, 
    FormacaoForm,
    LicenciaturaForm        
)

# ====================== PÁGINAS DE LISTAGEM ======================

def home_portfolio(request):
    return render(request, 'portfolio/home.html')

def tecnologias_view(request):
    tecnologias = Tecnologia.objects.all().order_by('-classificacao')
    return render(request, 'portfolio/tecnologias.html', {'tecnologias': tecnologias})

def projetos_view(request):
    projetos = Projeto.objects.all().order_by('-data')
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})

def unidades_view(request):
    unidades = UnidadeCurricular.objects.all().order_by('ano', 'semestre')
    return render(request, 'portfolio/unidades.html', {'unidades': unidades})

def tfc_view(request):
    tfcs = TFC.objects.select_related('orientador', 'licenciatura').all()
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
    
def makingoff_view(request):
    md_path = os.path.join(settings.BASE_DIR, 'portfolio', 'static', 'portfolio', 'makingoff.md')
    
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            conteudo_md = f.read()
    except FileNotFoundError:
        conteudo_md = "# Making Off\n\nFicheiro makingoff.md não encontrado."
    
    return render(request, 'portfolio/makingoff.html', {'conteudo_md': conteudo_md})


# ====================== CRUD PROJETOS ======================

def projeto_create(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projetos')
    else:
        form = ProjetoForm()
    return render(request, 'portfolio/projeto_form.html', {'form': form})


def projeto_update(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    if request.method == 'POST':
        form = ProjetoForm(request.POST, request.FILES, instance=projeto)
        if form.is_valid():
            form.save()
            return redirect('projetos')
    else:
        form = ProjetoForm(instance=projeto)
    return render(request, 'portfolio/projeto_form.html', {
        'form': form,
        'editar': True
    })


def projeto_delete(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    if request.method == 'POST':
        projeto.delete()
        return redirect('projetos')
    return render(request, 'portfolio/projeto_confirm_delete.html', {'projeto': projeto})

    # ====================== CRUD TECNOLOGIA ======================
def tecnologia_create(request):
    if request.method == 'POST':
        form = TecnologiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tecnologias')
    else:
        form = TecnologiaForm()
    return render(request, 'portfolio/tecnologia_form.html', {'form': form})

def tecnologia_update(request, pk):
    obj = get_object_or_404(Tecnologia, pk=pk)
    if request.method == 'POST':
        form = TecnologiaForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('tecnologias')
    else:
        form = TecnologiaForm(instance=obj)
    return render(request, 'portfolio/tecnologia_form.html', {'form': form, 'editar': True})

def tecnologia_delete(request, pk):
    obj = get_object_or_404(Tecnologia, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('tecnologias')
    return render(request, 'portfolio/tecnologia_confirm_delete.html', {'object': obj})


# ====================== CRUD COMPETENCIA ======================
def competencia_create(request):
    if request.method == 'POST':
        form = CompetenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('competencias')
    else:
        form = CompetenciaForm()
    return render(request, 'portfolio/competencia_form.html', {'form': form})

def competencia_update(request, pk):
    obj = get_object_or_404(Competencia, pk=pk)
    if request.method == 'POST':
        form = CompetenciaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('competencias')
    else:
        form = CompetenciaForm(instance=obj)
    return render(request, 'portfolio/competencia_form.html', {'form': form, 'editar': True})

def competencia_delete(request, pk):
    obj = get_object_or_404(Competencia, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('competencias')
    return render(request, 'portfolio/competencia_confirm_delete.html', {'object': obj})


# ====================== CRUD FORMACAO ======================
def formacao_create(request):
    if request.method == 'POST':
        form = FormacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formacoes')
    else:
        form = FormacaoForm()
    return render(request, 'portfolio/formacao_form.html', {'form': form})

def formacao_update(request, pk):
    obj = get_object_or_404(Formacao, pk=pk)
    if request.method == 'POST':
        form = FormacaoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('formacoes')
    else:
        form = FormacaoForm(instance=obj)
    return render(request, 'portfolio/formacao_form.html', {'form': form, 'editar': True})

def formacao_delete(request, pk):
    obj = get_object_or_404(Formacao, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('formacoes')
    return render(request, 'portfolio/formacao_confirm_delete.html', {'object': obj})

# ====================== CRUD LICENCIATURAS ======================

def licenciatura_create(request):
    if request.method == 'POST':
        form = LicenciaturaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('licenciaturas')
    else:
        form = LicenciaturaForm()
    return render(request, 'portfolio/licenciatura_form.html', {'form': form})


def licenciatura_update(request, pk):
    obj = get_object_or_404(Licenciatura, pk=pk)
    if request.method == 'POST':
        form = LicenciaturaForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('licenciaturas')
    else:
        form = LicenciaturaForm(instance=obj)
    return render(request, 'portfolio/licenciatura_form.html', {'form': form, 'editar': True})


def licenciatura_delete(request, pk):
    obj = get_object_or_404(Licenciatura, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('licenciaturas')
    return render(request, 'portfolio/licenciatura_confirm_delete.html', {'object': obj})