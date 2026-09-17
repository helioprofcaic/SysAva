"""Diagnóstico: analisa duplicatas no historico_aulas."""
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))
from supabase import create_client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_ANON_KEY")
sb = create_client(url, key)

# Busca registros de I-B para disciplina 11
res = sb.table("historico_aulas").select("*").eq("disciplina_id", 11).ilike("turma", "%INTEGRAL-I-B%").execute()

print(f"Total I-B + disc11: {len(res.data)} registros\n")

# Agrupa por (data_aula, horario)
from collections import Counter
keys = Counter()
for r in res.data:
    k = (r.get('data_aula'), r.get('horario'), r.get('turma_id'), r.get('disciplina_id'))
    keys[k] += 1

print("=== DUPLICATAS (mesma data+horario+turma+disciplina) ===")
dups = {k: v for k, v in keys.items() if v > 1}
for k, v in sorted(dups.items()):
    print(f"  {k}: {v} registros")

print(f"\nTotal combinações únicas: {len(keys)}")
print(f"Combinações duplicadas: {len(dups)}")

# Verifica registros com turma_id null
null_tid = [r for r in res.data if not r.get('turma_id')]
print(f"\nRegistros com turma_id=null: {len(null_tid)}")

# Verifica variações de turma
turmas = Counter(r.get('turma') for r in res.data)
print(f"\nValores de turma:")
for t, c in turmas.items():
    print(f"  '{t}': {c}")

# Verifica variações de horario
horarios = Counter(r.get('horario') for r in res.data)
print(f"\nValores de horario:")
for h, c in horarios.items():
    print(f"  '{h}': {c}")
