"""
Serviço de extração de texto de PDFs com formatação otimizada para IA.
Utiliza pdfplumber para extração precisa e preservação de estrutura.
"""

import os
import re
import io
import base64
import hashlib
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
from pathlib import Path
from PIL import Image

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
class ExtractedAsset:
    """Ilustração ou imagem extraída do PDF."""
    filename: str
    relative_path: str
    absolute_path: str
    page_number: int
    image_index: int
    width: int
    height: int
    image_format: str
    image_hash: str
    context_topic: str = ""
    caption_hint: str = ""
    svg_filename: str = ""
    svg_relative_path: str = ""
    svg_absolute_path: str = ""
    svg_content: str = ""


@dataclass
class ExtractedContent:
    """Conteúdo extraído de um PDF."""
    metadata: PDFMetadata
    full_text: str
    pages: List[Dict[str, Any]]
    tables: List[List[List[str]]]
    structure_summary: str
    assets: List[ExtractedAsset] = field(default_factory=list)


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
    
    def extract_from_file(
        self,
        file_path: str,
        extract_tables: bool = True,
        extract_assets: bool = True,
        output_assets_dir: Optional[str] = None,
        relative_to_dir: Optional[str] = None,
        save_images: bool = True
    ) -> ExtractedContent:
        """
        Extrai texto, tabelas e ilustrações de um arquivo PDF.
        
        Args:
            file_path: Caminho para o arquivo PDF
            extract_tables: Se deve extrair tabelas (padrão: True)
            extract_assets: Se deve extrair imagens e ilustrações (padrão: True)
            output_assets_dir: Diretório de destino para imagens extraídas
            relative_to_dir: Diretório base para geração de caminhos relativos em Markdown
            save_images: Se deve salvar os arquivos de imagem no disco (padrão: True)
            
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
                
                # Extrai imagens/ilustrações se solicitado
                assets = []
                if extract_assets:
                    assets = self._extract_images_from_pdf(
                        file_path=file_path,
                        pages_content=pages_content,
                        output_assets_dir=output_assets_dir,
                        relative_to_dir=relative_to_dir,
                        save_images=save_images
                    )

                # Gera resumo estruturado
                structure_summary = self._generate_structure_summary(pages_content, all_tables, len(assets))
                
                return ExtractedContent(
                    metadata=metadata,
                    full_text=full_text,
                    pages=pages_content,
                    tables=all_tables,
                    structure_summary=structure_summary,
                    assets=assets
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
    
    def _detect_context_for_image(self, page_text: str, page_num: int, img_idx: int) -> tuple:
        """Detecta o tópico da seção e gera uma sugestão de legenda para a imagem com base no texto da página."""
        if not page_text:
            return f"Tópico da Página {page_num}", f"Ilustração {img_idx + 1}"
        
        lower = page_text.lower()
        
        # 1. Checagens semânticas por ordem de especificidade e estrutura de seções
        if "1. introdução" in lower:
            if img_idx == 0:
                return "Introdução ao Design Visual", "Conceito e Cenário do Design Visual"
            else:
                return "Princípios C-R-A-P e Avaliação de Design", "Princípios de Contraste e Repetição"

        if "2. avaliação de design" in lower and "1. introdução" not in lower:
            return "Princípios C-R-A-P e Avaliação de Design", "Princípios de Contraste e Repetição"

        if "3. especificação do design" in lower or "protótipos de alta" in lower or "matriz csd" in lower:
            if img_idx == 0 and ("alinhamento" in lower or "proximidade" in lower):
                return "Alinhamento e Proximidade em Interfaces", "Disposição e Agrupamento Visual (CRAP)"
            return "Especificação do Design, Protótipos e Matriz CSD", "Protótipos de Alta Fidelidade e Matriz CSD"

        if "4. usabilidade" in lower:
            if ("acessibilidade" in lower or "inclusivas" in lower) and img_idx >= 1:
                return "Usabilidade e Acessibilidade em Interfaces", "Acessibilidade e Inclusão Digital"
            return "Pilares de Usabilidade e Wireframing", "Os Cinco Pilares da Usabilidade"

        if "5. a/b testing" in lower or "teste a/b" in lower or "criação das versões a e b" in lower:
            return "Metodologia de Teste A/B", "Comparação de Versões em Teste A/B"

        if "feedback" in lower or "expressão honesta" in lower:
            if ("integrar" in lower or "jornada digital" in lower) and img_idx >= 1:
                return "Integração do Feedback na Jornada Digital", "Evolução Contínua da Experiência do Usuário"
            return "Feedback do Usuário e Diálogo Contínuo", "Coleta e Valorização do Feedback do Usuário"

        if "alinhamento" in lower or "proximidade" in lower:
            if img_idx == 0:
                return "Alinhamento e Proximidade em Interfaces", "Disposição e Agrupamento Visual (CRAP)"

        # 2. Fallback para cabeçalhos encontrados na página
        lines = [l.strip() for l in page_text.split('\n') if l.strip()]
        headers = []
        for line in lines:
            if re.match(r'^\d+\.\s+[A-ZÁÉÍÓÚÃÕÇ\s]+', line):
                clean_line = re.sub(r'^\d+\.\s*', '', line).strip().title()
                headers.append(clean_line)
        
        if headers:
            h_idx = min(img_idx, len(headers) - 1)
            return headers[h_idx], f"Ilustração de {headers[h_idx]}"

        return f"Conteúdo da Página {page_num}", f"Ilustração {img_idx + 1}"

    def _extract_images_from_pdf(
        self,
        file_path: str,
        pages_content: List[Dict[str, Any]],
        output_assets_dir: Optional[str] = None,
        relative_to_dir: Optional[str] = None,
        save_images: bool = True
    ) -> List[ExtractedAsset]:
        """
        Extrai imagens/ilustrações relevantes do PDF, salvando-as na pasta de assets
        e filtrando cabeçalhos/logos repetidos e capas de página inteira.
        """
        assets = []
        try:
            from pypdf import PdfReader
        except ImportError:
            return assets

        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            if total_pages == 0:
                return assets

            pdf_stem = Path(file_path).stem
            # Gera nome padronizado de pasta: ex. aula_06
            m_aula = re.search(r'(?i)aula[_\s-]*0?(\d+)', pdf_stem)
            m_num = re.search(r'^0?(\d+)$', pdf_stem)
            if m_aula:
                lesson_folder = f"aula_{int(m_aula.group(1)):02d}"
                file_prefix = f"aula_{int(m_aula.group(1)):02d}"
            elif m_num:
                lesson_folder = f"aula_{int(m_num.group(1)):02d}"
                file_prefix = f"aula_{int(m_num.group(1)):02d}"
            else:
                clean_stem = re.sub(r'[^a-zA-Z0-9_-]', '_', pdf_stem).lower()
                lesson_folder = clean_stem
                file_prefix = clean_stem

            pdf_dir = os.path.dirname(os.path.abspath(file_path))
            
            if output_assets_dir is None:
                # Se está dentro de 'seductec', cria seductec/assets/<lesson_folder>
                output_assets_dir = os.path.join(pdf_dir, "assets", lesson_folder)

            if save_images:
                os.makedirs(output_assets_dir, exist_ok=True)

            # Primeira passagem: hash das imagens para identificar logos repetidos
            hash_counts = {}
            raw_images_list = []

            for page_idx, page in enumerate(reader.pages, 1):
                for img_idx, img in enumerate(page.images):
                    try:
                        raw_data = img.data
                        img_hash = hashlib.md5(raw_data).hexdigest()
                        hash_counts[img_hash] = hash_counts.get(img_hash, 0) + 1
                        
                        im = Image.open(io.BytesIO(raw_data))
                        fmt = (im.format or 'png').lower()
                        if fmt == 'jpeg':
                            fmt = 'jpg'
                            
                        raw_images_list.append({
                            'page_num': page_idx,
                            'img_idx': img_idx,
                            'name': img.name,
                            'data': raw_data,
                            'hash': img_hash,
                            'width': im.width,
                            'height': im.height,
                            'format': fmt
                        })
                    except Exception:
                        continue

            # Filtra logos de cabeçalho e capas de fundo
            page_img_counter = {}
            for item in raw_images_list:
                p_num = item['page_num']
                h = item['hash']
                w = item['width']
                height = item['height']
                
                # 1. Filtra logos de cabeçalho repetidos em 2+ páginas
                if hash_counts[h] > 1 and height < 200:
                    continue
                    
                # 2. Filtra capa inteira da primeira página ou ícones da capa
                if p_num == 1:
                    continue
                    
                # 3. Filtra imagens minúsculas (ícones de layout < 50px)
                if w < 50 or height < 50:
                    continue

                page_img_counter[p_num] = page_img_counter.get(p_num, 0) + 1
                curr_idx = page_img_counter[p_num]
                
                base_name = f"{file_prefix}_p{p_num:02d}_{curr_idx:02d}"
                out_filename = f"{base_name}.{item['format']}"
                svg_filename = f"{base_name}.svg"
                
                abs_dest = os.path.join(output_assets_dir, out_filename)
                abs_svg_dest = os.path.join(output_assets_dir, svg_filename)
                
                # Gera Base64 e String SVG autocontida
                b64_data = base64.b64encode(item['data']).decode('utf-8')
                mime_type = f"image/{'jpeg' if item['format'] in ['jpg', 'jpeg'] else 'png'}"
                svg_id = f"clip-{file_prefix}-p{p_num:02d}-{curr_idx:02d}"
                
                # Dimensões e proporções para encaixe lateral elegante ao texto (layout editorial)
                render_w = min(w, 240)
                render_h = int(height * (render_w / w)) if w > 0 else height

                svg_content = (
                    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" '
                    f'width="{render_w}" height="{render_h}" '
                    f'style="float: right; margin: 4px 0 16px 24px; max-width: 38%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); clear: right;">'
                    f'<defs><clipPath id="{svg_id}"><rect width="{w}" height="{height}" rx="8" ry="8"/></clipPath></defs>'
                    f'<image href="data:{mime_type};base64,{b64_data}" width="{w}" height="{height}" clip-path="url(#{svg_id})" />'
                    f'</svg>'
                )

                if save_images:
                    with open(abs_dest, 'wb') as f_out:
                        f_out.write(item['data'])
                    with open(abs_svg_dest, 'w', encoding='utf-8') as f_svg:
                        f_svg.write(svg_content)

                # Calcula caminhos relativos
                if relative_to_dir:
                    rel_path = os.path.relpath(abs_dest, relative_to_dir).replace('\\', '/')
                    rel_svg_path = os.path.relpath(abs_svg_dest, relative_to_dir).replace('\\', '/')
                else:
                    rel_path = os.path.relpath(abs_dest, os.path.dirname(os.path.dirname(output_assets_dir))).replace('\\', '/')
                    rel_svg_path = os.path.relpath(abs_svg_dest, os.path.dirname(os.path.dirname(output_assets_dir))).replace('\\', '/')

                # Busca texto da página correspondente
                page_text = ""
                if p_num <= len(pages_content):
                    page_text = pages_content[p_num - 1].get('text', '')

                context_topic, caption_hint = self._detect_context_for_image(page_text, p_num, curr_idx - 1)

                asset = ExtractedAsset(
                    filename=out_filename,
                    relative_path=rel_path,
                    absolute_path=abs_dest,
                    page_number=p_num,
                    image_index=curr_idx,
                    width=w,
                    height=height,
                    image_format=item['format'],
                    image_hash=h,
                    context_topic=context_topic,
                    caption_hint=caption_hint,
                    svg_filename=svg_filename,
                    svg_relative_path=rel_svg_path,
                    svg_absolute_path=abs_svg_dest,
                    svg_content=svg_content
                )
                assets.append(asset)

        except Exception as e:
            print(f"[Aviso] Falha ao extrair imagens do PDF: {e}")

        return assets

    def _generate_structure_summary(self, pages: List[Dict], tables: List, asset_count: int = 0) -> str:
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
        
        if asset_count > 0:
            summary_parts.append(f"Ilustrações extraídas: {asset_count}")

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

        # Indexa ilustrações por página para âncoras contextuais inline
        assets_by_page = {}
        for asset in content.assets:
            assets_by_page.setdefault(asset.page_number, []).append(asset)

        # Conteúdo textual — com âncoras de ilustrações posicionadas no fluxo da leitura
        for page in content.pages:
            page_num = page['page_number']
            text = page.get('text', '')
            tables = page.get('tables', [])
            page_assets = assets_by_page.get(page_num, [])

            if text.strip() or tables or page_assets:
                output_parts.append(f"--- Página {page_num} ---")

                # Se a página contém ilustrações, insere a âncora contextual
                if page_assets:
                    for a in page_assets:
                        output_parts.append(f"[📷 ILUSTRAÇÃO DESTA SEÇÃO: ![{a.caption_hint}]({a.relative_path}) -> Tópico: {a.context_topic}]")

                if text.strip():
                    output_parts.append(text)

                # Formata tabelas encontradas
                if tables:
                    for i, table in enumerate(tables, 1):
                        output_parts.append(self._format_table(table, i))

        # Guia explícito de posicionamento para o LLM
        if content.assets:
            output_parts.append("\n## 🗺️ GUIA DE POSICIONAMENTO DAS ILUSTRAÇÕES (MUITO IMPORTANTE):")
            output_parts.append("Distribua as ilustrações exatamente nos tópicos explicativos correspondentes. Posicione cada tag de imagem no início do parágrafo da sua seção para que o texto envolva a imagem:")
            for asset in content.assets:
                output_parts.append(
                    f"- `![{asset.caption_hint}]({asset.relative_path})` ➔ Posicionar no início de: **{asset.context_topic}** (Página {asset.page_number})"
                )
            output_parts.append("\nREGRA DE DESIGN: Cada ilustração deve ficar junto ao seu conceito específico. Nunca agrupe múltiplas ilustrações no mesmo parágrafo ou no final do texto.\n")

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


def convert_markdown_images_to_svg(
    markdown_text: str,
    assets: Optional[List[ExtractedAsset]] = None,
    assets_dir: Optional[str] = None
) -> str:
    """
    Converte referências de imagens Markdown (![alt](caminho)) e arquivos de assets
    em strings SVG autocontidas, permitindo persistência direta e portabilidade no Supabase.
    """
    if not markdown_text:
        return ""

    result = markdown_text

    # Se uma lista de assets extraídos foi fornecida, constrói um mapa por nome de arquivo e caminho relativo
    asset_map = {}
    if assets:
        for a in assets:
            if a.svg_content:
                asset_map[a.filename.lower()] = a.svg_content
                asset_map[a.svg_filename.lower()] = a.svg_content
                asset_map[a.relative_path.lower()] = a.svg_content
                asset_map[a.svg_relative_path.lower()] = a.svg_content
                # Também mapeia apenas o nome do arquivo sem extensão
                stem = Path(a.filename).stem.lower()
                asset_map[stem] = a.svg_content

    # Se foi passado um assets_dir, carrega os SVGs ou converte imagens locais
    if assets_dir and os.path.exists(assets_dir):
        for root, _, files in os.walk(assets_dir):
            for file in files:
                f_path = os.path.join(root, file)
                f_lower = file.lower()
                f_stem = Path(file).stem.lower()
                
                if f_lower.endswith('.svg') and f_lower not in asset_map:
                    try:
                        with open(f_path, 'r', encoding='utf-8') as f:
                            svg_data = f.read().strip()
                            asset_map[f_lower] = svg_data
                            asset_map[f_stem] = svg_data
                    except Exception:
                        pass
                elif f_lower.endswith(('.png', '.jpg', '.jpeg')) and f_lower not in asset_map:
                    try:
                        with open(f_path, 'rb') as f:
                            raw = f.read()
                        im = Image.open(io.BytesIO(raw))
                        fmt = 'jpeg' if f_lower.endswith(('.jpg', '.jpeg')) else 'png'
                        b64 = base64.b64encode(raw).decode('utf-8')
                        w, h = im.size
                        svg_id = f"clip-{f_stem}"
                        render_w = min(w, 240)
                        render_h = int(h * (render_w / w)) if w > 0 else h
                        svg_data = (
                            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
                            f'width="{render_w}" height="{render_h}" '
                            f'style="float: right; margin: 4px 0 16px 24px; max-width: 38%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); clear: right;">'
                            f'<defs><clipPath id="{svg_id}"><rect width="{w}" height="{h}" rx="8" ry="8"/></clipPath></defs>'
                            f'<image href="data:image/{fmt};base64,{b64}" width="{w}" height="{h}" clip-path="url(#{svg_id})" />'
                            f'</svg>'
                        )
                        asset_map[f_lower] = svg_data
                        asset_map[f_stem] = svg_data
                    except Exception:
                        pass

    # Substitui tags de imagem Markdown (![alt](path))
    def _repl_img(match):
        alt = match.group(1).strip()
        src = match.group(2).strip()
        src_lower = src.lower()
        src_filename = os.path.basename(src).lower()
        src_stem = Path(src_filename).stem.lower()

        # 1. Busca no mapa de assets pré-carregados
        if src_lower in asset_map:
            return f"\n{asset_map[src_lower]}\n"
        elif src_filename in asset_map:
            return f"\n{asset_map[src_filename]}\n"
        elif src_stem in asset_map:
            return f"\n{asset_map[src_stem]}\n"

        # 2. Se o caminho direto existe no disco
        if os.path.exists(src) and os.path.isfile(src):
            try:
                if src_lower.endswith('.svg'):
                    with open(src, 'r', encoding='utf-8') as f:
                        return f"\n{f.read().strip()}\n"
                with open(src, 'rb') as f:
                    raw = f.read()
                im = Image.open(io.BytesIO(raw))
                fmt = 'jpeg' if src_lower.endswith(('.jpg', '.jpeg')) else 'png'
                b64 = base64.b64encode(raw).decode('utf-8')
                w, h = im.size
                render_w = min(w, 240)
                render_h = int(h * (render_w / w)) if w > 0 else h
                svg_id = f"clip-{src_stem}"
                return (
                    f'\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
                    f'width="{render_w}" height="{render_h}" '
                    f'style="float: right; margin: 4px 0 16px 24px; max-width: 38%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); clear: right;">'
                    f'<defs><clipPath id="{svg_id}"><rect width="{w}" height="{h}" rx="8" ry="8"/></clipPath></defs>'
                    f'<image href="data:image/{fmt};base64,{b64}" width="{w}" height="{h}" clip-path="url(#{svg_id})" />'
                    f'</svg>\n'
                )
            except Exception:
                pass

        # 3. Busca recursiva na pasta data/Turmas por nome de arquivo correspondente
        data_dir = os.path.join(os.getcwd(), "data")
        if os.path.exists(data_dir):
            for root, _, files in os.walk(data_dir):
                for f in files:
                    if f.lower() == src_filename or Path(f).stem.lower() == src_stem:
                        candidate_path = os.path.join(root, f)
                        try:
                            if candidate_path.lower().endswith('.svg'):
                                with open(candidate_path, 'r', encoding='utf-8') as f_svg:
                                    return f"\n{f_svg.read().strip()}\n"
                            elif candidate_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                                with open(candidate_path, 'rb') as f_img:
                                    raw = f_img.read()
                                im = Image.open(io.BytesIO(raw))
                                fmt = 'jpeg' if candidate_path.lower().endswith(('.jpg', '.jpeg')) else 'png'
                                b64 = base64.b64encode(raw).decode('utf-8')
                                w, h = im.size
                                render_w = min(w, 240)
                                render_h = int(h * (render_w / w)) if w > 0 else h
                                svg_id = f"clip-{src_stem}"
                                return (
                                    f'\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
                                    f'width="{render_w}" height="{render_h}" '
                                    f'style="float: right; margin: 4px 0 16px 24px; max-width: 38%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); clear: right;">'
                                    f'<defs><clipPath id="{svg_id}"><rect width="{w}" height="{h}" rx="8" ry="8"/></clipPath></defs>'
                                    f'<image href="data:image/{fmt};base64,{b64}" width="{w}" height="{h}" clip-path="url(#{svg_id})" />'
                                    f'</svg>\n'
                                )
                        except Exception:
                            pass

        # 4. Se não encontrar o arquivo de imagem, não deixa o link quebrado que gera o ícone de imagem quebrada no navegador
        if alt:
            return f"\n\n> 🎨 **Ilustração Oficial:** *{alt}*\n\n"
        return ""

    result = re.sub(r'!\[(.*?)\]\((.*?)\)', _repl_img, result)
    return result


def extract_pdf_text(
    file_path: str,
    format_for_ai: bool = True,
    extract_assets: bool = True,
    output_assets_dir: Optional[str] = None,
    relative_to_dir: Optional[str] = None
) -> str:
    """
    Função de conveniência para extração rápida de texto e ilustrações de PDF.
    
    Args:
        file_path: Caminho para o arquivo PDF
        format_for_ai: Se deve formatar para leitura por IA (padrão: True)
        extract_assets: Se deve extrair ilustrações (padrão: True)
        output_assets_dir: Diretório para salvar imagens extraídas
        relative_to_dir: Diretório base para caminhos relativos de markdown
        
    Returns:
        Texto extraído e formatado
    """
    extractor = PDFExtractor()
    content = extractor.extract_from_file(
        file_path,
        extract_assets=extract_assets,
        output_assets_dir=output_assets_dir,
        relative_to_dir=relative_to_dir
    )
    
    if format_for_ai:
        return extractor.format_for_ai(content)
    else:
        return content.full_text


def extract_multiple_pdfs(
    file_paths: List[str],
    format_for_ai: bool = True,
    extract_assets: bool = True,
    relative_to_dir: Optional[str] = None
) -> str:
    """
    Extrai texto de múltiplos PDFs e combina.
    
    Args:
        file_paths: Lista de caminhos para arquivos PDF
        format_for_ai: Se deve formatar para leitura por IA
        extract_assets: Se deve extrair ilustrações
        relative_to_dir: Diretório base para caminhos relativos
        
    Returns:
        Texto combinado de todos os PDFs
    """
    extractor = PDFExtractor()
    combined_text = []
    
    for file_path in file_paths:
        try:
            content = extractor.extract_from_file(
                file_path,
                extract_assets=extract_assets,
                relative_to_dir=relative_to_dir
            )
            
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
