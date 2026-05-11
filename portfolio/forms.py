from django import forms
from .models import Projeto, Tecnologia, Competencia, Formacao

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

class TecnologiaForm(forms.ModelForm):
    class Meta:
        model = Tecnologia
        fields = '__all__'
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

class CompetenciaForm(forms.ModelForm):
    class Meta:
        model = Competencia
        fields = '__all__'

class FormacaoForm(forms.ModelForm):
    class Meta:
        model = Formacao
        fields = '__all__'
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }