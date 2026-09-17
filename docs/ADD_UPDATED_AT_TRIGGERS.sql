-- ============================================================================
-- updated_at + triggers para delta sync (cache local SQLite)
--
-- Objetivo: permitir que o sync incremental use `.gt('updated_at', cursor)`
-- em vez de baixar a tabela inteira. Rodar no SQL Editor do Supabase.
-- Idempotente.
-- ============================================================================

-- 1. Função genérica
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

-- 2. Adiciona a coluna (onde faltar) e cria o trigger em cada tabela existente
DO $$
DECLARE
  t text;
  tabelas text[] := ARRAY[
    'subjects', 'classes', 'class_subjects', 'weekly_schedule',
    'app_users', 'student_enrollments', 'attendance',
    'quizzes', 'quiz_questions', 'assessments', 'assessment_questions',
    'forum_posts', 'lessons', 'historico_aulas', 'planejamento', 'master_config'
  ];
BEGIN
  FOREACH t IN ARRAY tabelas LOOP
    IF EXISTS (
      SELECT 1 FROM information_schema.tables
       WHERE table_schema = 'public' AND table_name = t
    ) THEN
      EXECUTE format('ALTER TABLE %I ADD COLUMN IF NOT EXISTS updated_at timestamptz DEFAULT now()', t);
      EXECUTE format('DROP TRIGGER IF EXISTS trg_set_updated_at ON %I', t);
      EXECUTE format(
        'CREATE TRIGGER trg_set_updated_at BEFORE UPDATE ON %I '
        'FOR EACH ROW EXECUTE FUNCTION set_updated_at()', t
      );
      RAISE NOTICE 'OK: %', t;
    ELSE
      RAISE NOTICE 'Ignorada (não existe): %', t;
    END IF;
  END LOOP;
END $$;

-- 3. Índices para acelerar o pull incremental
CREATE INDEX IF NOT EXISTS idx_subjects_updated_at           ON subjects(updated_at);
CREATE INDEX IF NOT EXISTS idx_classes_updated_at            ON classes(updated_at);
CREATE INDEX IF NOT EXISTS idx_lessons_updated_at            ON lessons(updated_at);
CREATE INDEX IF NOT EXISTS idx_forum_posts_updated_at        ON forum_posts(updated_at);
CREATE INDEX IF NOT EXISTS idx_historico_aulas_updated_at    ON historico_aulas(updated_at);
CREATE INDEX IF NOT EXISTS idx_attendance_updated_at         ON attendance(updated_at);

-- 4. Verificação
SELECT table_name
  FROM information_schema.columns
 WHERE table_schema = 'public' AND column_name = 'updated_at'
 ORDER BY table_name;
