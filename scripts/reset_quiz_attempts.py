"""
Reset seletivo de tentativas de quiz (SysAva).

Contexto: o gerador antigo criava quizzes com títulos genéricos repetidos
(ex: "📝 Quiz: Teste seu Conhecimento!") e o sistema identificava a tentativa
pelo título. Resultado: quizzes apareciam "respondidos" sem o aluno responder
e o limite de 3 tentativas era compartilhado entre aulas.

Este script corrige o histórico (tabela `user_history`):
  - Tentativas com título ESPECÍFICO e resolvível -> recebem "| quiz_id:X"
    (a nota legítima é preservada e passa a contar para o quiz certo).
  - Tentativas com título GENÉRICO ou ambíguo -> são removidas (não podem ser
    atribuídas a uma aula; o aluno refaz e ganha nota nova).

Uso:
    python scripts/reset_quiz_attempts.py            # simulação (dry-run)
    python scripts/reset_quiz_attempts.py --apply    # aplica as alterações
    python scripts/reset_quiz_attempts.py --apply --subject-id 8   # só uma disciplina
"""

import os
import re
import sys
import unicodedata
from collections import defaultdict

from dotenv import load_dotenv
from supabase import create_client


def fetch_all(supabase, table, columns="*", page_size=1000):
    """Busca todas as linhas de uma tabela, contornando o limite padrão do Supabase."""
    rows = []
    start = 0
    while True:
        res = supabase.table(table).select(columns).range(start, start + page_size - 1).execute()
        data = res.data or []
        rows.extend(data)
        if len(data) < page_size:
            break
        start += page_size
    return rows


def is_generic_quiz_title(title):
    """Detecta títulos genéricos gerados pelo template da IA (não identificam a aula)."""
    if not title:
        return True
    norm = unicodedata.normalize('NFKD', str(title)).encode('ascii', 'ignore').decode('ascii').lower()
    norm = re.sub(r'[^a-z0-9]', '', norm)
    if norm in ("quiz", "quiztesteseuconhecimento", "quizquiztesteseuconhecimento"):
        return True
    if "testeseuconhecimento" in norm:
        return True
    if "perguntasmultiplaescolha" in norm:
        return True
    if "quiz" in norm and "perguntas" in norm and "escolha" in norm:
        return True
    return False


def lesson_number(text):
    m = re.search(r'Aula\s*0*(\d+)', text or '', re.IGNORECASE)
    return int(m.group(1)) if m else None


def resolve_quiz_id(title, subject_id, by_title, lesson_map):
    """Tenta descobrir a qual quiz uma tentativa antiga pertence."""
    candidates = by_title.get(title, [])
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]['id']

    if subject_id is not None:
        by_subject = [q for q in candidates
                      if lesson_map.get(q['lesson_id'], {}).get('subject_id') == subject_id]
        if len(by_subject) == 1:
            return by_subject[0]['id']
        candidates = by_subject or candidates

    number = lesson_number(title)
    if number is not None:
        by_number = [q for q in candidates
                     if lesson_number(lesson_map.get(q['lesson_id'], {}).get('title')) == number]
        if len(by_number) == 1:
            return by_number[0]['id']

    return None


def main():
    apply = "--apply" in sys.argv
    subject_filter = None
    if "--subject-id" in sys.argv:
        subject_filter = str(sys.argv[sys.argv.index("--subject-id") + 1])

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    load_dotenv(os.path.join(root_dir, '.env'))

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("❌ Credenciais do Supabase (SUPABASE_URL, SUPABASE_KEY) não encontradas no .env")
        return

    print("🔌 Conectando ao Supabase...")
    supabase = create_client(url, key)

    print("📥 Carregando quizzes, aulas e histórico...")
    quizzes = fetch_all(supabase, "quizzes", "id, lesson_id, title")
    lessons = fetch_all(supabase, "lessons", "id, title, subject_id")
    rows = fetch_all(supabase, "user_history", "id, username, activity")

    lesson_map = {l['id']: l for l in lessons}
    by_title = defaultdict(list)
    for q in quizzes:
        by_title[q['title']].append(q)

    attempts = [r for r in rows if str(r.get("activity", "")).startswith("Concluiu Quiz:")]

    by_activity = defaultdict(list)
    for r in attempts:
        by_activity[r['activity']].append(r['id'])

    to_remap = []   # (old_activity, new_activity, [ids])
    to_delete = []  # [ids]
    kept = 0
    ambiguous = []

    for act, ids in by_activity.items():
        if subject_filter:
            m = re.search(r'\| subject_id:(\d+)', act)
            if not m or m.group(1) != subject_filter:
                continue

        if "| quiz_id:" in act:
            kept += len(ids)
            continue

        clean = act.split('|')[0].strip()
        m = re.match(r'Concluiu Quiz:\s*(.*?)\s*\(\d+/\d+\)\s*$', clean)
        title = m.group(1).strip() if m else clean.replace("Concluiu Quiz:", "").strip()

        sm = re.search(r'\| subject_id:(\d+)', act)
        subject_id = int(sm.group(1)) if sm else None

        qid = resolve_quiz_id(title, subject_id, by_title, lesson_map)
        if qid is not None:
            to_remap.append((act, f"{act} | quiz_id:{qid}", ids))
        else:
            to_delete.extend(ids)
            if not is_generic_quiz_title(title):
                ambiguous.append((title, len(ids)))

    remap_rows = sum(len(ids) for _, _, ids in to_remap)
    print(f"\n📊 Tentativas de quiz no histórico: {len(attempts)}")
    print(f"   ✅ já com quiz_id (preservadas): {kept}")
    print(f"   🔗 a remapear (preserva nota):    {remap_rows} ({len(to_remap)} títulos distintos)")
    print(f"   🗑️  a remover (genéricas/ambíguas): {len(to_delete)}")

    if ambiguous:
        print("\n⚠️  Títulos específicos sem correspondência única (serão removidos):")
        for title, n in sorted(ambiguous, key=lambda x: -x[1])[:15]:
            print(f"   {n:3d}x  {title[:80]}")

    if not apply:
        print("\n⚠️  MODO SIMULAÇÃO — nada foi alterado. Use --apply para aplicar.")
        return

    print("\n🚀 Aplicando alterações...")
    for old_act, new_act, ids in to_remap:
        supabase.table("user_history").update({"activity": new_act}).eq("activity", old_act).execute()

    removed = 0
    for i in range(0, len(to_delete), 200):
        batch = to_delete[i:i + 200]
        supabase.table("user_history").delete().in_("id", batch).execute()
        removed += len(batch)

    print(f"\n🏁 Concluído. Remapeadas: {remap_rows} | Removidas: {removed} | Preservadas: {kept}")


if __name__ == "__main__":
    main()
