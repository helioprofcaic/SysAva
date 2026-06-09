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
import json
import requests
from datetime import datetime

# --- Configuração de Path ---
# URL da sua API local rodando na porta 8000
API_URL = "http://127.0.0.1:8000"

# Adiciona o diretório raiz do projeto ao sys.path para que possamos importar os serviços.
# O script está em 'data/repo/plugins', subimos 4 níveis para chegar na raiz 'SysAva'.
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from dotenv import load_dotenv
    from services import database as db
except ImportError as e:
    print(f"Erro de importação: {e}")
    print("Certifique-se de que as dependências como 'python-dotenv' e 'supabase' estão instaladas no ambiente virtual.")
    sys.exit(1)


def sync_local_to_supabase():
    """Puxa dados da API local e envia para o Supabase (Cloud)."""
    print("\n--- SINCRONIZANDO AUTOMAÇÃO: LOCAL -> SUPABASE ---")
    
    # 1. Sincronizar Histórico de Aulas
    try:
        print("  -> Sincronizando 'historico_aulas'...")
        resp = requests.get(f"{API_URL}/historico")
        if resp.status_code == 200:
            data = resp.json()
            for item in data:
                # O Supabase usa Snake Case e o Pydantic da API retorna o mesmo
                item.pop('id', None) # Deixa o Supabase gerar o ID dele
                db.supabase.table("historico_aulas").upsert(item).execute()
            print(f"     ✅ {len(data)} registros de histórico sincronizados.")
    except Exception as e:
        print(f"     ⚠️ Falha ao sincronizar histórico: {e}")

    # 2. Sincronizar Planejamento
    try:
        print("  -> Sincronizando 'planejamento'...")
        resp = requests.get(f"{API_URL}/planejamento/pendente")
        if resp.status_code == 200:
            data = resp.json()
            for item in data:
                item.pop('id', None)
                db.supabase.table("planejamento").upsert(item).execute()
            print(f"     ✅ {len(data)} registros de planejamento sincronizados.")
    except Exception as e:
        print(f"     ⚠️ Falha ao sincronizar planejamento: {e}")

    # 3. Sincronizar Master Config (SQLite -> Cloud)
    try:
        print("  -> Sincronizando 'master_config'...")
        resp = requests.get(f"{API_URL}/config/all")
        if resp.status_code == 200:
            data = resp.json()
            for item in data:
                # item é {"key": "...", "value": "..."}
                # Se o valor for string, tentamos converter para JSON para o campo JSONB do Supabase
                val = item['value']
                if isinstance(val, str):
                    try: val = json.loads(val)
                    except: pass
                db.supabase.table("master_config").upsert({"key": item['key'], "value": val}).execute()
            print(f"     ✅ {len(data)} chaves de configuração sincronizadas.")
    except Exception as e:
        print(f"     ⚠️ Falha ao sincronizar configurações: {e}")

def run_audit():
    """Realiza uma contagem de registros nas tabelas principais."""
    print("\n--- INICIANDO AUDITORIA RÁPIDA ---")

    # Mapeamento de tabelas para labels amigáveis (As 12 tabelas principais)
    audit_targets = {
        "app_users": "Usuários",
        "classes": "Turmas",
        "subjects": "Disciplinas",
        "lessons": "Aulas",
        "quizzes": "Quizzes",
        "quiz_questions": "Questões de Quiz",
        "assessments": "Avaliações (Provas)",
        "assessment_questions": "Questões de Prova",
        "attendance": "Registros de Frequência",
        "weekly_schedule": "Grade Horária",
        "student_enrollments": "Matrículas",
        "class_subjects": "Vínculos Turma/Disc",
        "historico_aulas": "Histórico de Automação (Robô)",
        "planejamento": "Fila de Planejamento",
        "master_config": "Espelhamento de Configurações"
    }
    
    results = {}

    for table, label in audit_targets.items():
        try:
            res = db.supabase.table(table).select("*", count='exact').execute()
            print(f"✅ {label}: {res.count}")
            results[table] = {"label": label, "count": res.count, "status": "ok"}
        except Exception:
            print(f"⚠️ {label}: Tabela ainda não existe no Supabase.")
            results[table] = {"label": label, "count": 0, "status": "missing"}

    # Salva o resumo para a API ler
    report_path = os.path.join(os.path.dirname(__file__), "audit_summary.json")
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
            
        print(f"--- AUDITORIA CONCLUÍDA ({len(audit_targets)} tabelas) ---\n")

    except Exception as e:
        print(f"❌ Erro durante a auditoria: {e}")


def run_backup():
    """Cria um backup do banco de dados em um arquivo SQLite."""
    print("\n--- INICIANDO BACKUP PARA SQLITE ---")

    # Tabelas a serem backupeadas
    TABLES_TO_BACKUP = [
        'app_users', 'classes', 'subjects', 'lessons', 'quizzes', 'quiz_questions',
        'assessments', 'assessment_questions', 'attendance', 'weekly_schedule',
        'student_enrollments', 'class_subjects', 'historico_aulas', 
        'planejamento', 'master_config'
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
            try:
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
            except Exception as e:
                print(f"     - ⚠️ Pulando tabela '{table_name}': Não encontrada na nuvem ou erro de acesso.")

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
    
    # Primeiro, envia os dados locais da automação para a nuvem
    sync_local_to_supabase()
    
    # Depois realiza a auditoria e o backup normal
    run_audit()
    run_backup()

if __name__ == "__main__":
    main()