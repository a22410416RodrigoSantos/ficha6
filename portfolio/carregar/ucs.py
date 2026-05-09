import json
import os
from django.core.management.base import BaseCommand

from portfolio.models import UnidadeCurricular


class Command(BaseCommand):
    help = "Carrega todas as Unidades Curriculares dos JSONs da Lusófona"

    def add_arguments(self, parser):
        parser.add_argument(
            '--apagar',
            action='store_true',
            help='Apaga todas as UCs antes de importar',
        )

    def handle(self, *args, **options):
        if options['apagar']:
            UnidadeCurricular.objects.all().delete()
            self.stdout.write(self.style.WARNING("🗑️  Todas as UCs foram apagadas."))

        pasta_jsons = "data/lusofona"
       
        if not os.path.exists(pasta_jsons):
            self.stdout.write(self.style.ERROR(f"Pasta não encontrada: {pasta_jsons}"))
            return

        ficheiros = [f for f in os.listdir(pasta_jsons) if f.endswith("-PT.json")]
       
        self.stdout.write(f"Encontrados {len(ficheiros)} ficheiros de UC. A importar...")

        criados = 0
        atualizados = 0
        ignorados = 0

        for ficheiro in ficheiros:
            caminho = os.path.join(pasta_jsons, ficheiro)
           
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)

                nome = dados.get("curricularUnitName")
                if not nome:
                    ignorados += 1
                    continue

                semestre = dados.get("semester") or dados.get("semestre") or ""
                ano = dados.get("curricularYear")

                uc, criado = UnidadeCurricular.objects.update_or_create(
                    nome=nome,
                    defaults={
                        "semestre": semestre,
                        "descricao": str(dados.get("objectives", ""))[:200],
                        "ects": int(dados.get("ects") or dados.get("creditos") or 0),
                        "ano": ano,
                    }
                )

                if criado:
                    criados += 1
                    self.stdout.write(self.style.SUCCESS(f"✅ Criado: {nome}"))
                else:
                    atualizados += 1
                    self.stdout.write(self.style.SUCCESS(f"🔄 Atualizado: {nome}"))

            except Exception as e:
                ignorados += 1
                self.stdout.write(self.style.ERROR(f"❌ Erro no ficheiro {ficheiro}: {e}"))

        self.stdout.write(self.style.SUCCESS(
            f"\n🎉 Importação concluída!\n"
            f"Criados: {criados} | Atualizados: {atualizados} | Ignorados: {ignorados}"
        ))