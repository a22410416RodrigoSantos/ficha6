from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Licenciatura(models.Model):
    nome = models.CharField(max_length=100)
    instituicao = models.CharField(max_length=150)
    semestres = models.IntegerField()
    descricao = models.CharField(max_length=250)
    ects = models.IntegerField()

    def __str__(self):
        return self.nome


class Docente(models.Model):
    nome = models.CharField(max_length=100)
    disciplina = models.ManyToManyField('UnidadeCurricular', blank=True)

    def __str__(self):
        return self.nome


class Tecnologia(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=150)
    logo = models.ImageField(null=True, blank=True)
    website_ofc = models.URLField()
    descricao = models.CharField(max_length=200)
    classificacao = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=200)
    conceitos_aplicados = models.CharField(max_length=250)
    imagem = models.ImageField(null=True, blank=True)
    video_demo = models.URLField()
    github_repo = models.URLField()
    data = models.DateField()
    classificacao = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )

    def __str__(self):
        return self.titulo


class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=100)
    semestre = models.CharField(max_length=100)
    descricao = models.CharField(max_length=200)
    ects = models.IntegerField()
    imagem = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.nome


class TFC(models.Model):
    titulo = models.CharField(max_length=100)
    resumo = models.CharField(max_length=200)
    aluno = models.CharField(max_length=100)
    orientador = models.ForeignKey(Docente, on_delete=models.CASCADE)
    ano = models.IntegerField()
    destaque = models.BooleanField()

    def __str__(self):
        return self.titulo


class Competencia(models.Model):
    nome = models.CharField(max_length=100)
    nivel = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Formacao(models.Model):
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    instituicao = models.CharField(max_length=150)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo


class MakingOFF(models.Model):
    descricao_decisoes = models.CharField(max_length=200)
    justificacao = models.CharField(max_length=250)
    correcoes = models.CharField(max_length=150)
    uso_ia = models.BooleanField()
    foto_caderno = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.tipo