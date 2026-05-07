"""
Auditoria e Backup do Banco de Dados

Este plugin realiza duas funções principais:
1.  **Auditoria Rápida:** Conta o número de registros nas tabelas principais (usuários, turmas, aulas, etc.) e imprime um resumo.
2.  **Backup em SQLite:** Extrai os dados de todas as tabelas importantes e os salva em um arquivo de banco de dados SQLite local (`.db`).

O arquivo de backup é nomeado com a data atual e salvo nesta mesma pasta de plugins.
"""

import os
import sys
import sqlite3
from datetime import datetime

# --- Configuração de Path ---
# Adiciona o diretório raiz do projeto ao sys.path para que possamos importar os serviços.
# O script está em 'data/repo/plugins', então subimos 3 níveis para chegar à raiz.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from dotenv import load_dotenv
    from services import database as db
except ImportError as e:
    print(f"Erro de importação: {e}")
    print("Certifique-se de que as dependências como 'python-dotenv' e 'supabase' estão instaladas no ambiente virtual.")
    sys.exit(1)


def run_audit():
    """Realiza uma contagem de registros nas tabelas principais."""
    print("\n--- INICIANDO AUDITORIA RÁPIDA ---")
    
    try:
        users = db.supabase.table("app_users").select("*", count='exact').execute().count
        classes = db.supabase.table("classes").select("*", count='exact').execute().count
        subjects = db.supabase.table("subjects").select("*", count='exact').execute().count
        lessons = db.supabase.table("lessons").select("*", count='exact').execute().count
        quizzes = db.supabase.table("quizzes").select("*", count='exact').execute().count
        quiz_questions = db.supabase.table("quiz_questions").select("*", count='exact').execute().count
        assessments = db.supabase.table("assessments").select("*", count='exact').execute().count
        
        print(f"✅ Usuários: {users}")
        print(f"✅ Turmas: {classes}")
        print(f"✅ Disciplinas: {subjects}")
        print(f"✅ Aulas: {lessons}")
        print(f"✅ Quizzes: {quizzes}")
        print(f"✅ Questões de Quiz: {quiz_questions}")
        print(f"✅ Avaliações (Provas): {assessments}")
        print("--- AUDITORIA CONCLUÍDA ---\n")

    except Exception as e:
        print(f"❌ Erro durante a auditoria: {e}")


def run_backup():
    """Cria um backup do banco de dados em um arquivo SQLite."""
    print("\n--- INICIANDO BACKUP PARA SQLITE ---")

    # Tabelas a serem backupeadas
    TABLES_TO_BACKUP = [
        'app_users', 'classes', 'subjects', 'class_subjects', 'student_enrollments',
        'lessons', 'quizzes', 'quiz_questions', 'assessments', 'assessment_questions',
        'student_assessments', 'student_assessment_answers', 'forum_posts', 'user_history'
    ]

    # Nome do arquivo de backup
    date_str = datetime.now().strftime("%Y-%m-%d")
    backup_filename = f"backup_SysAva_{date_str}.db"
    backup_filepath = os.path.join(os.path.dirname(__file__), backup_filename)

    try:
        # Conecta ao banco de dados SQLite (cria se não existir)
        conn = sqlite3.connect(backup_filepath)
        cursor = conn.cursor()
        print(f"💾 Arquivo de backup será salvo em: {backup_filepath}")

        for table_name in TABLES_TO_BACKUP:
            print(f"  -> Processando tabela: '{table_name}'...")
            
            # 1. Busca dados da tabela no Supabase
            response = db.supabase.table(table_name).select("*").execute()
            data = response.data

            if not data:
                print(f"     - Tabela '{table_name}' está vazia. Pulando.")
                continue

            # 2. Cria a tabela no SQLite
            columns = data[0].keys()
            # Para simplificar, todos os campos serão TEXT. Em um backup mais robusto, mapearíamos os tipos.
            # Usamos `IF NOT EXISTS` para segurança.
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{col} TEXT' for col in columns])})"
            cursor.execute(create_table_sql)

            # 3. Limpa a tabela antes de inserir para evitar duplicatas em re-execuções
            cursor.execute(f"DELETE FROM {table_name}")

            # 4. Insere os dados
            placeholders = ', '.join(['?'] * len(columns))
            insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

            rows_to_insert = []
            for row in data:
                # Converte listas/dicionários para string JSON para compatibilidade com SQLite
                values = [str(v) if isinstance(v, (dict, list)) else v for v in row.values()]
                rows_to_insert.append(tuple(values))
            
            cursor.executemany(insert_sql, rows_to_insert)
            print(f"     - {len(rows_to_insert)} registros salvos.")

        # Salva as alterações e fecha a conexão
        conn.commit()
        conn.close()

        print("\n✅ BACKUP CONCLUÍDO COM SUCESSO!")

    except Exception as e:
        print(f"❌ Erro durante o backup: {e}")


def main():
    """Função principal que executa o plugin."""
    print("="*50)
    print("PLUGIN DE AUDITORIA E BACKUP DO SYSAVA")
    print("="*50)

    # Carrega as variáveis de ambiente do arquivo .env na raiz do projeto
    env_path = os.path.join(project_root, '.env')
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
        print("Arquivo .env carregado.")
    
    # Inicializa a conexão com o banco
    if not db.is_db_connected():
        print("\n❌ ERRO: Não foi possível conectar ao banco de dados.")
        print("Verifique se as variáveis SUPABASE_URL e SUPABASE_KEY estão no arquivo .env na raiz do projeto.")
        return

    print("\nConexão com o banco de dados estabelecida com sucesso.")
    
    run_audit()
    run_backup()

if __name__ == "__main__":
    main()