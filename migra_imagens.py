import os
from django.core.files import File
from portfolio.models import Projeto, Tecnologia, Artigo, Licenciatura, UnidadeCurricular, TFC

def migrar_imagens():
    print("🚀 Iniciando migração de imagens para Cloudinary...\n")

    models_to_migrate = [
        (Projeto, 'imagem', 'titulo'),
        (Tecnologia, 'logo', 'nome'),
        (Artigo, 'fotografia', 'titulo'),
        (Licenciatura, 'imagem', 'nome'),      # se tiveres este campo
        (UnidadeCurricular, 'imagem', 'nome'), # se tiveres este campo
        (TFC, 'imagem', 'titulo'),             # se tiveres este campo
    ]

    for Model, field_name, title_field in models_to_migrate:
        print(f"🔄 Migrando imagens de {Model.__name__}...")
        count = 0
        
        for obj in Model.objects.all():
            image_field = getattr(obj, field_name, None)
            
            if image_field and image_field.name:
                local_path = image_field.path
                
                if os.path.exists(local_path):
                    try:
                        with open(local_path, 'rb') as f:
                            # Faz upload para o Cloudinary
                            image_field.save(
                                os.path.basename(local_path),
                                File(f),
                                save=True
                            )
                        count += 1
                        print(f"✅ Migrado: {Model.__name__} - {getattr(obj, title_field)}")
                    except Exception as e:
                        print(f"❌ Erro ao migrar {getattr(obj, title_field)}: {e}")
                else:
                    print(f"⚠️  Ficheiro não encontrado: {local_path}")
        
        print(f"   → {count} imagens migradas de {Model.__name__}\n")

    print("🎉 Migração concluída!")


# Executar automaticamente quando correr o script
if __name__ == "__main__":
    import django
    django.setup()
    migrar_imagens()