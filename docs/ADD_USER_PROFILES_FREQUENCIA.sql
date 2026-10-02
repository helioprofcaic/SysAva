-- =============================================================================
-- IS-040 — Mecanismo de inativos por aluno (frequência)
-- Projeto Supabase novo (xfuddmsvnievbipddvsx)
--
-- Executar no SQL Editor do Supabase. A coluna `frequencia_status` espelha o
-- estado de frequência do aluno e é gravada junto com os flags de `app_users`:
--   'normal'  -> is_active = true,  is_portal = true   (aparece, conta presença)
--   'falta'   -> is_active = false, is_portal = true   (aparece na chamada como Falta)
--   'inativo' -> is_portal   = false, status='inactive'(excluído da lista de chamada)
--
-- Sem essas colunas o código continua funcionando: o portal deriva o status a
-- partir de app_users.is_active / app_users.is_portal (fallback).
-- =============================================================================

ALTER TABLE public.user_profiles
    ADD COLUMN IF NOT EXISTS frequencia_status TEXT NOT NULL DEFAULT 'normal',
    ADD COLUMN IF NOT EXISTS motivo TEXT DEFAULT '',
    ADD COLUMN IF NOT EXISTS atualizado_em TIMESTAMPTZ DEFAULT NOW();

ALTER TABLE public.user_profiles
    DROP CONSTRAINT IF EXISTS user_profiles_frequencia_status_check;

ALTER TABLE public.user_profiles
    ADD CONSTRAINT user_profiles_frequencia_status_check
    CHECK (frequencia_status IN ('normal', 'falta', 'inativo'));

GRANT ALL ON public.user_profiles TO anon, authenticated, service_role;

NOTIFY pgrst, 'reload schema';
