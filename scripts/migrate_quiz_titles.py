"""
Migração: corrige títulos de quizzes duplicados/genéricos.

Problema: o gerador de aulas criava quizzes com o mesmo título genérico
(ex: "📝 Quiz: Teste seu Conhecimento!") para todas as aulas. Como o sistema
identificava a conclusão pelo título, responder um quiz marcava vários outros
como concluídos, além de compartilhar tentativas e notas.

Esta migração:
  1. Mantém apenas um quiz por aula (o que tiver mais questões; empate -> menor ID).
  2. Remove os quizzes excedentes e suas questões.
  3. Renomeia o quiz mantido para "Quiz: {título da aula}".

Uso:
    python scripts/migrate_quiz_titles.py            # simulação (dry-run, não altera nada)
    python scripts/migrate_quiz_titles.py --apply    # aplica as alterações
"""

import os
import sys
from collections import Counter, defaultdict

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


def main():
    dry_run = "--apply" not in sys.argv

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    load_dotenv(os.path.join(root_dir, '.env'))

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("❌ Credenciais do Supabase (SUPABASE_URL, SUPABASE_KEY) não encontradas no .env")
        return

    print("🔌 Conectando ao Supabase...")
    supabase = create_client(url, key)

    print("📥 Carregando quizzes, aulas e questões...")
    quizzes = fetch_all(supabase, "quizzes", "id, lesson_id, title")
    lessons = fetch_all(supabase, "lessons", "id, title")
    questions = fetch_all(supabase, "quiz_questions", "id, quiz_id")

    lesson_map = {l['id']: l for l in lessons}
    question_count = Counter(q['quiz_id'] for q in questions)

    by_lesson = defaultdict(list)
    for quiz in quizzes:
        by_lesson[quiz.get('lesson_id')].append(quiz)

    print(f"🔍 {len(quizzes)} quizzes em {len(by_lesson)} aulas | "
          f"{len(quizzes) - len(by_lesson)} quizzes excedentes a remover.")
    if dry_run:
        print("⚠️  MODO SIMULAÇÃO — nada será alterado. Use --apply para aplicar.\n")

    renamed = deleted = skipped = 0

    for lesson_id, quiz_list in by_lesson.items():
        lesson = lesson_map.get(lesson_id)
        if not lesson:
            skipped += len(quiz_list)
            continue

        # Mantém o quiz com mais questões (empate -> menor ID)
        quiz_list.sort(key=lambda z: (-question_count.get(z['id'], 0), z['id']))
        keeper = quiz_list[0]
        extras = quiz_list[1:]
        new_title = f"Quiz: {lesson['title']}".strip()

        if len(quiz_list) > 1:
            print(f"📚 Aula {lesson_id} ({lesson['title'][:45]}) — {len(quiz_list)} quizzes")
            for extra in extras:
                print(f"   🗑️  remover quiz id={extra['id']} (questões: {question_count.get(extra['id'], 0)})")
            print(f"   ✅ manter  quiz id={keeper['id']} (questões: {question_count.get(keeper['id'], 0)})")

        if not dry_run:
            for extra in extras:
                supabase.table("quiz_questions").delete().eq("quiz_id", extra['id']).execute()
                supabase.table("quizzes").delete().eq("id", extra['id']).execute()
                deleted += 1
            if keeper['title'] != new_title:
                supabase.table("quizzes").update({"title": new_title}).eq("id", keeper['id']).execute()
                renamed += 1
        else:
            deleted += len(extras)
            if keeper['title'] != new_title:
                renamed += 1

    print(f"\n🏁 Concluído. Renomeados: {renamed} | Removidos: {deleted} | Ignorados: {skipped}")
    if dry_run:
        print("ℹ️  Nenhuma alteração foi aplicada (dry-run).")


if __name__ == "__main__":
    main()
