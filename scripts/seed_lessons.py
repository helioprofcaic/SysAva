# scripts/seed_lessons.py
import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path para importar os serviços
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_lesson_seeder():
    # Configuração do ambiente
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(project_root, '.env')
    load_dotenv(dotenv_path=env_path)

    class MockSecrets(dict):
        def __getitem__(self, key):
            return os.environ.get(key)

    import streamlit as st
    st.secrets = MockSecrets()

    from services import database as db

    if not db.is_db_connected():
        print("ERRO: Conexão com o banco falhou. Verifique o arquivo .env")
        return

    # O caminho base agora aponta para a pasta de Turmas
    base_path = os.path.join(project_root, 'data', 'Turmas')
    print(f"Iniciando importação de aulas em lote a partir de: {base_path}")

    if not os.path.exists(base_path):
        print(f"AVISO: Diretório '{base_path}' não encontrado. Nenhuma aula para importar.")
        return

    total_lessons = 0

    # Usa os.walk para percorrer toda a árvore de diretórios
    for root, dirs, files in os.walk(base_path):
        # Só nos interessam as pastas que contêm arquivos .md
        md_files = [f for f in files if f.lower().endswith(".md")]
        if not md_files:
            continue

        # Calcula o caminho relativo para entender a estrutura
        try:
            relative_path = os.path.relpath(root, base_path)
            path_parts = relative_path.split(os.sep)
        except ValueError:
            continue
        
        # A estrutura esperada é: {turma}\{disciplina}\{semana} (3 partes)
        if len(path_parts) == 3:
            class_name, subject_name, week_folder = path_parts

            if week_folder.upper().startswith('S'):
                print(f"\n Encontrado: Turma '{class_name}' -> Disciplina '{subject_name}' -> Semana '{week_folder}'")

                # Busca a disciplina no banco pelo nome da pasta
                subject_data = db.get_subject_by_name(subject_name)
                if not subject_data:
                    print(f"  ⚠️  Disciplina '{subject_name}' não encontrada no banco. Verifique se o nome da pasta corresponde ao nome no Escola.txt.")
                    continue
                
                subject_id = subject_data['id']

                # Processa os arquivos .md dentro da pasta da semana
                for lesson_file in sorted(md_files):
                    lesson_title = lesson_file[:-3].replace('_', ' ').capitalize()
                    lesson_path = os.path.join(root, lesson_file)

                    with open(lesson_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    lines = content.splitlines()
                    
                    video_url = lines[0].strip() if lines and lines[0].strip().startswith("http") else ""
                    description_lines = []
                    title_found = False
                    
                    for line in lines:
                        stripped = line.strip()
                        
                        # Procura URL de vídeo (primeira ocorrência de http)
                        if stripped.startswith("http") and not video_url:
                            video_url = stripped
                            continue # Não inclui a URL na descrição
                        
                        # Procura o Título da Aula (primeira ocorrência de # ou ##)
                        if not title_found and stripped.startswith("#"):
                            # Remove caracteres de markdown (#) e espaços
                            clean_title = stripped.lstrip("#").strip()
                            if clean_title:
                                lesson_title = clean_title
                                title_found = True
                                continue # Não inclui o título na descrição (já será o cabeçalho)
                        
                        description_lines.append(line)
                    
                    description = "\n".join(description_lines).strip()
                    if not description:
                        description = "Sem descrição"
                    
                    lesson_id = db.upsert_lesson(lesson_title, subject_id, description, video_url)
                    if lesson_id:
                        print(f"    ✅ Aula '{lesson_title}' importada.")
                        total_lessons += 1
        else:
            # Diagnóstico para pastas ignoradas
            if len(path_parts) < 3:
                print(f"  ⚠️  Ignorando pasta '{relative_path}': Estrutura muito rasa (esperado: Turma/Disciplina/Semana).")

    print(f"\nProcesso concluído. Total de aulas importadas: {total_lessons}")

if __name__ == "__main__":
    run_lesson_seeder()