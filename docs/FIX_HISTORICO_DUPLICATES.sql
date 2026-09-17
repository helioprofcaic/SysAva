-- ============================================================
-- FIX:historico_aulas - Remove duplicatas e adiciona UNIQUE
-- ============================================================

-- 1. Remove duplicatas, mantendo apenas o registro mais antigo (menor id) de cada combinação
DELETE FROM historico_aulas
WHERE id NOT IN (
    SELECT MIN(id)
    FROM historico_aulas
    GROUP BY data_aula, horario, turma_id, disciplina_id
);

-- 2. Adiciona a constraint UNIQUE (necessária para o upsert funcionar)
ALTER TABLE historico_aulas
    ADD CONSTRAINT historico_aulas_unique
    UNIQUE (data_aula, horario, turma_id, disciplina_id);

-- 3. Recarrega o cache do schema
NOTIFY pgrst, 'reload schema';

-- 4. Verificação: quantos registros restam?
SELECT COUNT(*) AS total_registros FROM historico_aulas;
