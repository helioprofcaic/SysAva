"""
Serviço de extração de texto de PDFs com formatação otimizada para IA.
Utiliza pdfplumber para extração precisa e preservação de estrutura.
"""

import os
import re
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from pathlib import Path

try:
    import pdfplumber
    from pdfplumber.page import Page
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False
    pdfplumber = None
    Page = None

try:
    import pypdfium2 as pdfium
    HAS_PYPDFIUM2 = True
except ImportError:
    HAS_PYPDFIUM2 = False
    pdfium = None

# Flag global para indicar se o extrador está disponível
HAS_PDF_EXTRACTOR = HAS_PDFPLUMBER


@dataclass
class PDFMetadata:
    """Metadados extraídos do PDF."""
    filename: str
    page_count: int
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    creator: Optional[str] = None
    producer: Optional[str] = None


@dataclass
class ExtractedContent:
    """Conteúdo extraído de um PDF."""
    metadata: PDFMetadata
    full_text: str
    pages: List[Dict[str, Any]]
    tables: List[List[List[str]]]
    structure_summary: str


class PDFExtractor:
    """
    Extrator de texto de PDFs com formatação otimizada para modelos de IA.
    
    Características:
    - Preserva estrutura de parágrafos e listas
    - Detecta e formata tabelas
    - Adiciona marcadores visuais para seções
    - Limpa artefatos de formatação
    - Gera resumo estruturado
    """
    
    def __init__(self):
        if not HAS_PDFPLUMBER:
            raise ImportError(
                "pdfplumber não está instalado. Execute: pip install pdfplumber"
            )
        
        self.section_patterns = [
            r'^(?:CAPÍTULO|CHAPTER|PARTE|PART)\s*[\dIVX]+',
            r'^\d+\.\s+[A-ZÁÉÍÓÚÃÕÇ][a-záéíóúãõç\s]+',
            r'^[IVXLC]+\.\s+[A-ZÁÉÍÓÚÃÕÇ]',
            r'^•\s+|^\d+\)\s+|^\-\s+',
        ]
    
    def extract_from_file(self, file_path: str, extract_tables: bool = True) -> ExtractedContent:
        """
        Extrai texto e estrutura de um arquivo PDF.
        
        Args:
            file_path: Caminho para o arquivo PDF
            extract_tables: Se deve extrair tabelas (padrão: True)
            
        Returns:
            ExtractedContent com todo o conteúdo extraído
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        filename = os.path.basename(file_path)
        
        try:
            with pdfplumber.open(file_path) as pdf:
                # Metadados
                metadata = PDFMetadata(
                    filename=filename,
                    page_count=len(pdf.pages),
                    title=pdf.metadata.get('Title') if pdf.metadata else None,
                    author=pdf.metadata.get('Author') if pdf.metadata else None,
                    subject=pdf.metadata.get('Subject') if pdf.metadata else None,
                    creator=pdf.metadata.get('Creator') if pdf.metadata else None,
                    producer=pdf.metadata.get('Producer') if pdf.metadata else None
                )
                
                pages_content = []
                all_text = []
                all_tables = []
                
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extrai texto com preservação de estrutura
                    page_text = self._extract_page_text(page)
                    
                    # Extrai tabelas se solicitado
                    page_tables = []
                    if extract_tables:
                        page_tables = self._extract_tables(page)
                        all_tables.extend(page_tables)
                    
                    # Armazena conteúdo da página
                    pages_content.append({
                        'page_number': page_num,
                        'text': page_text,
                        'tables': page_tables,
                        'has_tables': len(page_tables) > 0
                    })
                    
                    if page_text.strip():
                        all_text.append(f"--- Página {page_num} ---\n{page_text}")
                
                # Combina todo o texto
                full_text = "\n\n".join(all_text)
                
                # Gera resumo estruturado
                structure_summary = self._generate_structure_summary(pages_content, all_tables)
                
                return ExtractedContent(
                    metadata=metadata,
                    full_text=full_text,
                    pages=pages_content,
                    tables=all_tables,
                    structure_summary=structure_summary
                )
                
        except Exception as e:
            raise Exception(f"Erro ao processar PDF {filename}: {str(e)}")
    
    def _extract_page_text(self, page: Page) -> str:
        """
        Extrai texto de uma página com preservação de estrutura.
        """
        try:
            # Usa extract_text com configurações otimadas
            text = page.extract_text(
                x_tolerance=3,
                y_tolerance=3,
                layout=False,
                x_density=7.25,
                y_density=3
            )
            
            if not text:
                return ""
            
            # Limpa e formata o texto
            text = self._clean_text(text)
            text = self._preserve_structure(text)
            
            return text
            
        except Exception as e:
            print(f"[Aviso] Erro na extração da página: {e}")
            return ""
    
    def _extract_tables(self, page: Page) -> List[List[List[str]]]:
        """
        Extrai tabelas de uma página.
        """
        tables = []
        
        try:
            # Configurações para detecção de tabelas
            table_settings = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "min_words_vertical": 3,
                "min_words_horizontal": 3,
                "snap_tolerance": 5,
                "join_tolerance": 30,
                "edge_min_length": 10,
                "min_words_vertical": 3,
                "min_words_horizontal": 3,
            }
            
            extracted_tables = page.extract_tables(table_settings)
            
            for table in extracted_tables:
                if table and len(table) > 0:
                    # Limpa células vazias e formata
                    cleaned_table = []
                    for row in table:
                        cleaned_row = [str(cell).strip() if cell else "" for cell in row]
                        if any(cell for cell in cleaned_row):  # Pula linhas vazias
                            cleaned_table.append(cleaned_row)
                    
                    if cleaned_table:
                        tables.append(cleaned_table)
                        
        except Exception as e:
            print(f"[Aviso] Erro na extração de tabelas: {e}")
        
        return tables
    
    def _clean_text(self, text: str) -> str:
        """
        Limpa artefatos de formatação do texto extraído.
        """
        if not text:
            return ""
        
        # Remove múltiplos espaços em branco, preservando quebras de linha
        text = re.sub(r'[^\S\n]+', ' ', text)
        
        # Remove linhas vazias consecutivas (mantém apenas uma)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Remove caracteres especiais indesejados
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
        
        # Corrige problemas comuns de encoding
        text = text.replace('â€"', '–')
        text = text.replace('â€"', '—')
        text = text.replace('â€œ', '"')
        text = text.replace('â€\x9d', '"')
        text = text.replace('â€˜', ''')
        text = text.replace('â€™', ''')
        
        return text.strip()
    
    def _preserve_structure(self, text: str) -> str:
        """
        Preserva e melhora a estrutura do documento.
        Quebras de linha mínimas para não desperdiçar tokens.
        """
        if not text:
            return ""

        lines = text.split('\n')
        processed_lines = []

        for line in lines:
            line = line.strip()

            if not line:
                # Linha vazia: mantém apenas uma quebra
                if processed_lines and processed_lines[-1] != '':
                    processed_lines.append('')
                continue

            # Detecta se é cabeçalho/seção
            if self._is_section_header(line):
                # Uma quebra antes e depois (não três)
                processed_lines.append(f"\n## {line}")
            # Detecta se é item de lista
            elif self._is_list_item(line):
                processed_lines.append(f"- {line.lstrip('•-* ')}")
            # Detecta se é numeral de lista
            elif self._is_numbered_item(line):
                processed_lines.append(f"{line}")
            # Linha normal
            else:
                processed_lines.append(line)

        return '\n'.join(processed_lines)
    
    def _is_section_header(self, line: str) -> bool:
        """Verifica se a linha é um cabeçalho de seção."""
        for pattern in self.section_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                return True
        
        # Verifica se está em maiúsculas e tem comprimento razoável
        if line.isupper() and len(line) > 5 and len(line) < 100:
            return True
        
        return False
    
    def _is_list_item(self, line: str) -> bool:
        """Verifica se a linha é um item de lista."""
        return bool(re.match(r'^[•\-\*]\s+', line))
    
    def _is_numbered_item(self, line: str) -> bool:
        """Verifica se a linha é um item numerado."""
        return bool(re.match(r'^\d+[\.\)]\s+', line))
    
    def _generate_structure_summary(self, pages: List[Dict], tables: List) -> str:
        """
        Gera um resumo estruturado do documento.
        """
        summary_parts = []
        
        # Conta seções detectadas
        section_count = 0
        for page in pages:
            text = page.get('text', '')
            section_count += len(re.findall(r'^##\s+', text, re.MULTILINE))
        
        # Adiciona informações ao resumo
        summary_parts.append(f"Total de páginas: {len(pages)}")
        
        if section_count > 0:
            summary_parts.append(f"Seções identificadas: {section_count}")
        
        if tables:
            summary_parts.append(f"Tabelas encontradas: {len(tables)}")
            # Descreve primeiras tabelas
            for i, table in enumerate(tables[:3], 1):
                if table:
                    rows = len(table)
                    cols = len(table[0]) if table else 0
                    summary_parts.append(f"  Tabela {i}: {rows} linhas x {cols} colunas")
        
        pages_with_content = sum(1 for p in pages if p.get('text', '').strip())
        summary_parts.append(f"Páginas com conteúdo textual: {pages_with_content}")
        
        return "\n".join(summary_parts)
    
    def format_for_ai(self, content: ExtractedContent, include_metadata: bool = True) -> str:
        """
        Formata o conteúdo extraído para otimização da leitura por modelos de IA.
        Quebras de linha mínimas para não desperdiçar tokens.

        Args:
            content: Conteúdo extraído do PDF
            include_metadata: Se deve incluir metadados (padrão: True)

        Returns:
            Texto formatado e otimizado para IA
        """
        output_parts = []

        # Cabeçalho compacto com metadados
        if include_metadata:
            meta = [f"DOCUMENTO: {content.metadata.filename}"]
            if content.metadata.title:
                meta.append(f"TÍTULO: {content.metadata.title}")
            if content.metadata.author:
                meta.append(f"AUTOR: {content.metadata.author}")
            meta.append(f"PÁGINAS: {content.metadata.page_count}")
            output_parts.append(" | ".join(meta))

        # Resumo estruturado
        if content.structure_summary:
            output_parts.append(f"RESUMO: {content.structure_summary}")

        # Conteúdo textual —紧凑格式
        for page in content.pages:
            page_num = page['page_number']
            text = page.get('text', '')
            tables = page.get('tables', [])

            if text.strip() or tables:
                output_parts.append(f"--- Página {page_num} ---")

                if text.strip():
                    output_parts.append(text)

                # Formata tabelas encontradas
                if tables:
                    for i, table in enumerate(tables, 1):
                        output_parts.append(self._format_table(table, i))

        return "\n".join(output_parts)
    
    def _format_table(self, table: List[List[str]], table_num: int = 1) -> str:
        """
        Formata uma tabela em Markdown de forma compacta.
        """
        if not table or not table[0]:
            return ""

        lines = [f"Tabela {table_num}:"]

        # Cabeçalho
        header = table[0]
        lines.append("| " + " | ".join(str(cell) for cell in header) + " |")
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")

        # Corpo da tabela
        for row in table[1:]:
            padded_row = row + [""] * (len(header) - len(row))
            lines.append("| " + " | ".join(str(cell) for cell in padded_row[:len(header)]) + " |")

        return "\n".join(lines)


def extract_pdf_text(file_path: str, format_for_ai: bool = True) -> str:
    """
    Função de conveniência para extração rápida de texto de PDF.
    
    Args:
        file_path: Caminho para o arquivo PDF
        format_for_ai: Se deve formatar para leitura por IA (padrão: True)
        
    Returns:
        Texto extraído e formatado
    """
    extractor = PDFExtractor()
    content = extractor.extract_from_file(file_path)
    
    if format_for_ai:
        return extractor.format_for_ai(content)
    else:
        return content.full_text


def extract_multiple_pdfs(file_paths: List[str], format_for_ai: bool = True) -> str:
    """
    Extrai texto de múltiplos PDFs e combina.
    
    Args:
        file_paths: Lista de caminhos para arquivos PDF
        format_for_ai: Se deve formatar para leitura por IA
        
    Returns:
        Texto combinado de todos os PDFs
    """
    extractor = PDFExtractor()
    combined_text = []
    
    for file_path in file_paths:
        try:
            content = extractor.extract_from_file(file_path)
            
            if format_for_ai:
                formatted = extractor.format_for_ai(content)
            else:
                formatted = content.full_text
            
            combined_text.append(formatted)
            
        except Exception as e:
            combined_text.append(f"Erro ao processar {os.path.basename(file_path)}: {str(e)}")
    
    return "\n\n" + "=" * 60 + "\n\n".join(combined_text)


# Função para compatibilidade com código existente
def extract_text_pypdf_fallback(file_path: str) -> str:
    """
    Fallback usando pypdf caso pdfplumber não esteja disponível.
    """
    try:
        from pypdf import PdfReader
        
        reader = PdfReader(file_path)
        text_parts = []
        
        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            if page_text:
                text_parts.append(f"--- Página {page_num} ---\n{page_text}")
        
        return "\n\n".join(text_parts)
        
    except Exception as e:
        return f"Erro na extração: {str(e)}" if str(e) else "Erro desconhecido na extração"


if __name__ == "__main__":
    # Teste rápido
    import sys
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        if os.path.exists(pdf_path):
            print(f"Extraindo texto de: {pdf_path}")
            text = extract_pdf_text(pdf_path)
            print("\n" + "=" * 60)
            print("TEXTO EXTRAÍDO:")
            print("=" * 60)
            print(text[:2000] + "..." if len(text) > 2000 else text)
        else:
            print(f"Arquivo não encontrado: {pdf_path}")
    else:
        print("Uso: python pdf_extractor.py <caminho_para_pdf>")
