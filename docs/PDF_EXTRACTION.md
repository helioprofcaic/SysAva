# 📄 Extração Otimizada de PDFs

Este documento descreve o sistema avançado de extração de texto de PDFs implementado no SysAva, otimizado para uso com modelos de IA.

## Visão Geral

O sistema foi projetado para superar as limitações da extração padrão de PDFs, fornecendo texto limpo, bem formatado e otimizado para compreensão por modelos de linguagem (LLMs).

## Componentes Principais

### 1. PDFExtractor (`services/pdf_extractor.py`)

Classe principal responsável pela extração e formatação de PDFs.

**Características:**
- Extração precisa usando `pdfplumber`
- Detecção automática de tabelas
- Preservação de estrutura do documento
- Limpeza de artefatos de formatação
- Formatação otimizada para IA

### 2. GerenciadorContextoAula (`services/contexto_aulas.py`)

Integrado com o novo extrador, fornece contexto formatado para o gerador de aulas.

## Instalação

```bash
# Instalar dependências necessárias
pip install pdfplumber pypdfium2

# Ou atualizar todas as dependências
pip install -r requirements.txt
```

## Uso

### Extração Básica

```python
from services.pdf_extractor import extract_pdf_text

# Extrai texto formatado para IA
text = extract_pdf_text("documento.pdf")
print(text)
```

### Extração com Metadados

```python
from services.pdf_extractor import PDFExtractor

extractor = PDFExtractor()
content = extractor.extract_from_file("documento.pdf")

# Acessa metadados
print(f"Título: {content.metadata.title}")
print(f"Autor: {content.metadata.author}")
print(f"Páginas: {content.metadata.page_count}")

# Acessa tabelas encontradas
for i, table in enumerate(content.tables, 1):
    print(f"Tabela {i}: {len(table)} linhas")

# Formata para IA
formatted = extractor.format_for_ai(content)
```

### Múltiplos PDFs

```python
from services.pdf_extractor import extract_multiple_pdfs

files = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
combined_text = extract_multiple_pdfs(files)
```

## Formato de Saída

O texto extraído é formatado da seguinte forma:

```markdown
============================================================
DOCUMENTO: nome_do_documento.pdf
TÍTULO: Título do Documento
AUTOR: Nome do Autor
PÁGINAS: Número de Páginas
============================================================

## RESUMO DO DOCUMENTO
Total de páginas: N
Seções identificadas: N
Tabelas encontradas: N
  Tabela 1: N linhas x N colunas

## CONTEÚDO COMPLETO

### Página 1

[Conteúdo da página com estrutura preservada]

**Tabelas nesta página:**

**Tabela 1:**

| Coluna 1 | Coluna 2 | Coluna 3 |
| --- | --- | --- |
| Dado 1 | Dado 2 | Dado 3 |

### Página 2

[Conteúdo da página...]
```

## Benefícios para Modelos de IA

1. **Hierarquia Clara**: Cabeçalhos Markdown (`##`, `###`) facilitam a navegação
2. **Estrutura Preservada**: Listas e enumerações mantêm sua formatação
3. **Tabelas Formatadas**: Dados tabulares são apresentados de forma clara
4. **Metadados**: Informações contextuais ajudam o modelo a entender o documento
5. **Resumo**: Visão geral permite identificação rápida do conteúdo
6. **Texto Limpo**: Sem artefatos de formatação ou caracteres indesejados

## Comparações

### Método Antigo (pypdf)

```python
# Extração básica sem formatação
from pypdf import PdfReader

reader = PdfReader("documento.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"
```

**Limitações:**
- Texto sem formatação
- Perda de estrutura
- Sem detecção de tabelas
- Sem metadados
- Artefatos de formatação

### Método Novo (pdfplumber)

```python
# Extração otimizada com formatação
from services.pdf_extractor import extract_pdf_text

text = extract_pdf_text("documento.pdf", format_for_ai=True)
```

**Vantagens:**
- ~35% mais conteúdo extraído
- Estrutura preservada
- Tabelas detectadas e formatadas
- Metadados extraídos
- Texto limpo e legível

## Testes

### Executar Testes de Extração

```bash
# Teste básico de extração
python scripts/test_pdf_extraction.py

# Testes de integração
python scripts/test_integration.py

# Demonistração das melhorias
python scripts/demo_pdf_improvements.py
```

### Teste com Arquivo Específico

```python
from services.pdf_extractor import PDFExtractor

extractor = PDFExtractor()
content = extractor.extract_from_file("caminho/para/documento.pdf")

# Verifica resultados
print(f"Caracteres extraídos: {len(content.full_text)}")
print(f"Tabelas encontradas: {len(content.tables)}")
print(f"Seções identificadas: {content.structure_summary.count('Seções identificadas:')}")
```

## Solução de Problemas

### pdfplumber não está instalado

```bash
pip install pdfplumber
```

### Erro de importação

Verifique se o `services/pdf_extractor.py` está no diretório correto e se as dependências estão instaladas.

### Texto extraído está vazio

1. Verifique se o PDF não é uma imagem (scan)
2. Teste com outro PDF para confirmar
3. Verifique se o PDF não está corrompido

### Tabelas não são detectadas

A detecção de tabelas depende da estrutura visual do PDF. PDFs com tabelas gráficas (sem linhas de separação claras) podem não ser detectados.

## Compatibilidade

- **Python**: 3.8+
- **Sistemas**: Windows, macOS, Linux
- **Dependências**: pdfplumber, pypdfium2 (opcional)

## Roadmap

- [ ] Suporte a PDFs escaneados (OCR)
- [ ] Extração de imagens e legendas
- [ ] Processamento em lote otimizado
- [ ] Cache de extrações para performance
- [ ] Suporte a PDFs protegidos com senha

## Contribuindo

Ao adicionar novas funcionalidades de extração:

1. Mantenha a compatibilidade com a interface existente
2. Adicione testes para novos cenários
3. Atualize esta documentação
4. Execute os testes de regressão

## Licença

Este módulo faz parte do projeto SysAva e está sujeito à mesma licença.
