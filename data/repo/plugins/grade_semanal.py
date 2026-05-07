"""
Grade Semanal de Aulas

Este plugin permite gerenciar e visualizar o mapa de horários das turmas.
Como o SysAva foca em conteúdo, este plugin estende a funcionalidade para 
organização do tempo.

Uso:
1. Executar via SysAva (Visualização)
2. Executar via Terminal: python grade_semanal.py --edit (Para cadastrar horários)
"""

import os
import sys
import json

# --- Configuração de Path ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from services import database as db
except ImportError:
    print("Erro: Não foi possível importar o serviço de banco de dados.")
    sys.exit(1)

DATA_FILE = os.path.join(os.path.dirname(__file__), "grade_horaria.json")
DIAS_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
# Horários padrão (podem ser personalizados no JSON manualmente)
HORARIOS_PADRAO = ["07:10", "08:10", "09:10", "10:10", "10:30", "11:30", "12:30", "13:30", "14:30", "14:50", "15:50", "16:50"]

def load_grade():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_grade(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def exibir_grade(turma_nome, data):
    turma_data = data.get(turma_nome, {})
    horarios = turma_data.get("config_horarios", HORARIOS_PADRAO)
    
    print(f"\n📅 GRADE SEMANAL - TURMA: {turma_nome}")
    print("=" * 105)
    
    # Cabeçalho
    header = f"{'Horário':<10}"
    for dia in DIAS_SEMANA:
        header += f"| {dia:^16} "
    print(header)
    print("-" * 105)

    # Linhas
    for h in horarios:
        row = f"{h:<10}"
        for dia in DIAS_SEMANA:
            disciplina = turma_data.get(dia, {}).get(h, "---")
            # Trunca o nome da disciplina para caber na coluna
            row += f"| {disciplina[:16]:^16} "
        print(row)
    print("=" * 105)

def menu_edicao():
    print("\n--- MODO DE EDIÇÃO DE GRADE ---")
    grade = load_grade()
    
    # 1. Selecionar Turma
    classes = db.get_classes()
    if not classes:
        print("Nenhuma turma encontrada no banco de dados.")
        return

    print("\nTurmas disponíveis:")
    for i, c in enumerate(classes):
        print(f"[{i+1}] {c['name']}")
    
    try:
        idx = int(input("\nSelecione o número da turma (ou 0 para cancelar): ")) - 1
        if idx == -1: return
        turma_nome = classes[idx]['name']
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return

    if turma_nome not in grade:
        grade[turma_nome] = {dia: {} for dia in DIAS_SEMANA}
        grade[turma_nome]["config_horarios"] = HORARIOS_PADRAO
        save_grade(grade)

    while True:
        # 2. Selecionar Dia
        print(f"\n--- Editando Turma: {turma_nome} ---")
        print("Dias da Semana:")
        for i, dia in enumerate(DIAS_SEMANA):
            print(f"[{i+1}] {dia}")
        print("[0] Sair ou Trocar de Turma")
        
        try:
            sel_dia = input("\nSelecione o dia: ").strip()
            if sel_dia == '0': break
            dia_idx = int(sel_dia) - 1
            dia_selecionado = DIAS_SEMANA[dia_idx]
        except (ValueError, IndexError):
            print("Opção inválida.")
            continue

        while True:
            # 3. Selecionar Horário
            horarios = grade[turma_nome].get("config_horarios", HORARIOS_PADRAO)
            print(f"\nHorários para {dia_selecionado} ({turma_nome}):")
            for i, h in enumerate(horarios):
                # Garante que o dicionário do dia existe
                if dia_selecionado not in grade[turma_nome]:
                    grade[turma_nome][dia_selecionado] = {}
                
                atual = grade[turma_nome][dia_selecionado].get(h, "---")
                print(f"[{i+1}] {h} -> {atual}")
            print("[0] Voltar para seleção de dia")

            try:
                sel_h = input("Selecione o horário para editar: ").strip()
                if sel_h == '0': break
                h_idx = int(sel_h) - 1
                horario_selecionado = horarios[h_idx]
            except (ValueError, IndexError):
                print("Opção inválida.")
                continue

            # 4. Definir Disciplina
            nova_disc = input(f"Disciplina para {dia_selecionado} as {horario_selecionado} (Enter p/ limpar): ").strip()
            
            if nova_disc:
                grade[turma_nome][dia_selecionado][horario_selecionado] = nova_disc
                print("✅ Atualizado!")
            else:
                if horario_selecionado in grade[turma_nome][dia_selecionado]:
                    del grade[turma_nome][dia_selecionado][horario_selecionado]
                    print("🗑️ Removido.")
            
            # Salva a cada modificação para garantir persistência
            save_grade(grade)

def main():
    print("="*50)
    print("PLUGIN: MAPA DE GRADE SEMANAL")
    print("="*50)

    if "--edit" in sys.argv:
        if not db.is_db_connected():
            print("Erro: Banco de dados não conectado. Verifique o .env")
            return
        menu_edicao()
    else:
        grade = load_grade()
        if not grade:
            print("\nNenhuma grade horária cadastrada.")
            print("Para cadastrar, execute este script no terminal com o parâmetro '--edit':")
            print(f"Comando: python data/repo/plugins/grade_semanal.py --edit")
            
            # Exemplo de visualização
            print("\nExemplo de como a grade aparecerá:")
            exibir_grade("Exemplo 3º Ano", {"Exemplo 3º Ano": {"Segunda": {"07:30": "IA Aplicada"}}})
        else:
            for turma in grade:
                exibir_grade(turma, grade)

if __name__ == "__main__":
    main()