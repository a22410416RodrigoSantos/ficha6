from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artigo, Comentario, Like
from .forms import ArtigoForm


def artigos_list(request):
    artigos = Artigo.objects.all().order_by('-data_criacao')
    return render(request, 'artigos/list.html', {'artigos': artigos})


def artigo_detail(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    comentarios = artigo.comentarios.all().order_by('-data')
    
    # Verificar se o utilizador já deu like
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(artigo=artigo, utilizador=request.user).exists()
    
    return render(request, 'artigos/detail.html', {
        'artigo': artigo,
        'comentarios': comentarios,
        'user_liked': user_liked
    })


@login_required
def artigo_create(request):
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES)
        if form.is_valid():
            artigo = form.save(commit=False)
            artigo.autor = request.user
            artigo.save()
            messages.success(request, 'Artigo publicado com sucesso!')
            return redirect('artigo_detail', pk=artigo.pk)
    else:
        form = ArtigoForm()
    return render(request, 'artigos/form.html', {'form': form})


@login_required
def artigo_update(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    
    # Só o autor pode editar
    if artigo.autor != request.user:
        messages.error(request, 'Não tens permissão para editar este artigo.')
        return redirect('artigo_detail', pk=pk)
    
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES, instance=artigo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artigo atualizado!')
            return redirect('artigo_detail', pk=pk)
    else:
        form = ArtigoForm(instance=artigo)
    
    return render(request, 'artigos/form.html', {'form': form, 'editar': True})


@login_required
def artigo_delete(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if artigo.autor != request.user:
        messages.error(request, 'Não tens permissão para apagar este artigo.')
        return redirect('artigo_detail', pk=pk)
    
    if request.method == 'POST':
        artigo.delete()
        messages.success(request, 'Artigo apagado com sucesso.')
        return redirect('artigos')
    return render(request, 'artigos/confirm_delete.html', {'artigo': artigo})

@login_required
def add_comentario(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    
    if request.method == 'POST':
        texto = request.POST.get('texto')
        if texto:
            Comentario.objects.create(
                artigo=artigo,
                autor=request.user,
                texto=texto
            )
            messages.success(request, 'Comentário publicado!')
    
    return redirect('artigo_detail', pk=pk)