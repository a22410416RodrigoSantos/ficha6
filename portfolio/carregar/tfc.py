# portfolio/management/commands/carregar_tfc.py
import json
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests

from portfolio.models import TFC, Docente, Licenciatura, Tecnologia, Competencia


class Command(BaseCommand):
    help = "Carrega os TFCs do JSON (adaptado ao modelo atual)"

    def handle(self, *args, **options):
        caminho_json = "data/tfcs.json"   # altera se necessário
        
        self.stdout.write("📂 A ler o ficheiro tfcs.json...")

        with open(caminho_json, "r", encoding="utf-8") as f:
            dados = json.load(f)

        if isinstance(dados, dict):
            dados = [dados]

        criados = 0
        atualizados = 0

        for item in dados:
            try:
                titulo = item.get("titulo")
                if not titulo:
                    continue

                # === Ano (extraído da licenciatura) ===
                lic_str = item.get("licenciaturas") or ""
                ano = 2025  # default
                if "." in lic_str:
                    try:
                        ano = int(lic_str.split(".")[-1].strip())
                    except:
                        pass

                # === Orientador (Docente) ===
                orientador_nome = item.get("orientador") or "Desconhecido"
                orientador, _ = Docente.objects.get_or_create(nome=orientador_nome)

                # === Licenciatura ===
                nome_lic = lic_str.split(".")[0].strip() if "." in lic_str else lic_str
                if not nome_lic:
                    nome_lic = "Mestrado em Engenharia Informática e Sistemas de Informação"
                
                licenciatura, _ = Licenciatura.objects.get_or_create(nome=nome_lic)

                # === Tecnologias ===
                tech_nomes = item.get("tecnologias usadas") or []
                tecnologias = []
                for nome in tech_nomes:
                    if nome:
                        tech, _ = Tecnologia.objects.get_or_create(
                            nome=nome.strip(),
                            defaults={"tipo": "Ferramenta", "interesseNivel": 7}
                        )
                        tecnologias.append(tech)

                # === Áreas ===
                area_nomes = item.get("áreas") or []
                areas = []
                for nome in area_nomes:
                    if nome:
                        area, _ = Competencia.objects.get_or_create(
                            nome=nome.strip(),
                            defaults={"tipo": "Área Temática", "nivel": 8}
                        )
                        areas.append(area)

                # === Download da imagem (opcional mas recomendado) ===
                imagem_url = item.get("imagem")
                imagem_file = None
                if imagem_url:
                    try:
                        response = requests.get(imagem_url, timeout=10)
                        if response.status_code == 200:
                            temp_file = NamedTemporaryFile(delete=True)
                            temp_file.write(response.content)
                            temp_file.seek(0)
                            imagem_file = File(temp_file, name=f"{titulo[:50]}.png")
                    except Exception as img_err:
                        self.stdout.write(self.style.WARNING(f"⚠️ Não foi possível descarregar imagem: {img_err}"))

                # === Criar / Atualizar TFC ===
                tfc, criado = TFC.objects.update_or_create(
                    titulo=titulo,
                    aluno=item.get("nome") or "Autor Desconhecido",
                    defaults={
                        "resumo": (item.get("resumo") or "")[:200],
                        "orientador": orientador,
                        "ano": ano,
                        "destaque": False,
                        "licenciatura": licenciatura,
                        "link": item.get("link para PDF") or "",
                    }
                )

                # ManyToMany fields
                tfc.tecnologia.set(tecnologias)
                tfc.area.set(areas)

                # Imagem (se foi descarregada)
                if imagem_file:
                    tfc.imagem.save(imagem_file.name, imagem_file, save=True)

                if criado:
                    criados += 1
                    self.stdout.write(self.style.SUCCESS(f"✅ Criado: {titulo}"))
                else:
                    atualizados += 1
                    self.stdout.write(self.style.SUCCESS(f"🔄 Atualizado: {titulo}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"❌ Erro em '{item.get('titulo', 'sem título')}': {e}"
                ))

        self.stdout.write(self.style.SUCCESS(
            f"\n🎉 Concluído! Criados: {criados} | Atualizados: {atualizados}"
        ))