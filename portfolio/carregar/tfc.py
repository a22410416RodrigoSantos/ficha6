# portfolio/management/commands/carregar_tfc.py

import json
from django.core.management.base import BaseCommand

from portfolio.models import TFC, Docente, Licenciatura, Tecnologia, Competencia


class Command(BaseCommand):
    help = "Carrega os TFCs do JSON (versão rápida)"

    def handle(self, *args, **options):
        caminho_json = "data/TFCS.json"

        self.stdout.write("A ler o ficheiro TFCS.json...")

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

                # Orientador
                orientador_nome = item.get("orientador") or "Desconhecido"
                orientador, _ = Docente.objects.get_or_create(nome=orientador_nome)

                # Licenciatura
                lic_str = item.get("licenciaturas") or ""
                nome_lic = lic_str.split(".")[0].strip() if "." in lic_str else lic_str or "Engenharia Informática"
                licenciatura, _ = Licenciatura.objects.get_or_create(nome=nome_lic)
                
                # Tecnologias
                tech_nomes = item.get("tecnologias usadas") or []
                tecnologias = []
                for nome in tech_nomes:
                    if nome:
                        tech, _ = Tecnologia.objects.get_or_create(
                            nome=nome,
                            defaults={"tipo": "Linguagem/Ferramenta", "URL": "#", "interesseNivel": 7}
                        )
                        tecnologias.append(tech)

                # Áreas
                area_nomes = item.get("áreas") or []
                areas = []
                for nome in area_nomes:
                    if nome:
                        area, _ = Competencia.objects.get_or_create(
                            nome=nome,
                            defaults={"tipo": "Área Temática", "nivel": 8}
                        )
                        areas.append(area)

                # TFC - agora adiciona mesmo que falte URL ou resumo
                tfc, criado = TFC.objects.update_or_create(
                    titulo=titulo,
                    aluno=item.get("nome") or "Autor Desconhecido",
                    defaults={
                        "orientador": orientador,
                        "licenciatura": licenciatura,
                        "descricao": (item.get("resumo") or "")[:200],
                        "URL": item.get("link para PDF") or "",          # aceita vazio
                        "destaque": False,
                    }
                )

                tfc.tecnologia.set(tecnologias)
                tfc.area.set(areas)

                if criado:
                    criados += 1
                    self.stdout.write(f"✅ Criado: {titulo}")
                else:
                    atualizados += 1
                    self.stdout.write(f"🔄 Atualizado: {titulo}")

            except Exception as e:
                self.stdout.write(f"❌ Erro em '{item.get('titulo', 'sem título')}': {e}")

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Concluído! Criados: {criados} | Atualizados: {atualizados}"
        ))