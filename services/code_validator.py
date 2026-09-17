"""
Módulo de validação para questões práticas de Código Web (HTML, CSS, JavaScript).
Impede o envio de texto puro, lero-lero ou respostas sem código válido.
"""

import re
from html.parser import HTMLParser

# Conjunto de tags HTML comuns e válidas
VALID_HTML_TAGS = {
    "a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi",
    "bdo", "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code",
    "col", "colgroup", "data", "datalist", "dd", "del", "details", "dfn", "dialog",
    "div", "dl", "dt", "em", "embed", "fieldset", "figcaption", "figure", "footer",
    "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr",
    "html", "i", "iframe", "img", "input", "ins", "kbd", "label", "legend", "li",
    "link", "main", "map", "mark", "menu", "meta", "meter", "nav", "noscript",
    "object", "ol", "optgroup", "option", "output", "p", "param", "picture", "pre",
    "progress", "q", "rp", "rt", "ruby", "s", "samp", "script", "search", "section",
    "select", "slot", "small", "source", "span", "strong", "style", "sub", "summary",
    "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead",
    "time", "title", "tr", "track", "u", "ul", "var", "video", "wbr", "svg", "path", "circle"
}

# Principais propriedades CSS comuns para validação sintática
COMMON_CSS_PROPERTIES = {
    "color", "background", "background-color", "background-image", "background-size",
    "margin", "margin-top", "margin-bottom", "margin-left", "margin-right",
    "padding", "padding-top", "padding-bottom", "padding-left", "padding-right",
    "font-size", "font-family", "font-weight", "font-style", "line-height",
    "text-align", "text-decoration", "text-transform", "letter-spacing",
    "width", "height", "min-width", "max-width", "min-height", "max-height",
    "display", "flex", "flex-direction", "justify-content", "align-items", "align-content",
    "grid", "grid-template-columns", "grid-template-rows", "gap", "grid-gap",
    "border", "border-radius", "border-color", "border-width", "border-style",
    "position", "top", "bottom", "left", "right", "z-index", "overflow", "overflow-x", "overflow-y",
    "opacity", "box-shadow", "text-shadow", "transition", "transform", "animation",
    "cursor", "box-sizing", "list-style", "outline", "visibility"
}

# Palavras-chave e padrões característicos de JavaScript
JS_KEYWORD_PATTERNS = [
    r'\b(let|const|var)\s+[a-zA-Z_$][a-zA-Z0-9_$]*\b',
    r'\bfunction\s*([a-zA-Z_$][a-zA-Z0-9_$]*)?\s*\(',
    r'\b(if|for|while|switch|catch)\s*\(',
    r'=>',
    r'\bconsole\.(log|warn|error|info|debug)\s*\(',
    r'\b(document|window)\.[a-zA-Z_$]',
    r'\b(getElementById|getElementsByClassName|getElementsByTagName|querySelector|querySelectorAll|addEventListener|removeEventListener)\s*\(',
    r'\b(alert|prompt|confirm|setTimeout|setInterval|clearTimeout|clearInterval)\s*\(',
    r'\b(return|break|continue|throw|typeof|instanceof|new)\b',
    r'\b(Math|JSON|Array|Object|String|Number|Date|Promise|fetch)\.[a-zA-Z_$]',
    r'(\.innerHTML|\.innerText|\.textContent|\.value|\.style|\.classList|\.appendChild|\.createElement)\b'
]


class StrictHTMLTagCounter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.unknown_tags = []
        self.has_unclosed_tags = False

    def handle_starttag(self, tag, attrs):
        lower_tag = tag.lower()
        if lower_tag in VALID_HTML_TAGS:
            self.tags.append(lower_tag)
        else:
            self.unknown_tags.append(lower_tag)

    def handle_startendtag(self, tag, attrs):
        lower_tag = tag.lower()
        if lower_tag in VALID_HTML_TAGS:
            self.tags.append(lower_tag)
        else:
            self.unknown_tags.append(lower_tag)


def validate_html_code(html_str: str, required: bool = True) -> tuple[bool, str]:
    """
    Valida se a string fornecida contém código HTML estruturado válido.
    Rejeita texto puro ou ausência de tags HTML reais.
    """
    if not html_str or not html_str.strip():
        if required:
            return False, "O código HTML é obrigatório e não pode ficar em branco."
        return True, ""

    stripped = html_str.strip()

    # Checa se há pelo menos um par de tags ou tag auto-fechada
    tag_regex = re.compile(r'<\s*([a-zA-Z0-9]+)(\s+[^>]*)?>', re.IGNORECASE)
    matches = tag_regex.findall(stripped)

    if not matches:
        return False, "O campo HTML não contém nenhuma tag HTML válida (ex: <div>, <h1>, <p>, <button>, etc.). Digite código HTML e não texto comum."

    parser = StrictHTMLTagCounter()
    try:
        parser.feed(stripped)
    except Exception as e:
        return False, f"Erro de sintaxe no HTML: {str(e)}"

    valid_tags_count = len(parser.tags)
    if valid_tags_count == 0:
        return False, "Nenhuma tag HTML reconhecida foi encontrada. Verifique se as tags estão escritas corretamente (ex: <div class='...'>)."

    # Verifica se a maior parte do conteúdo não é apenas texto aleatório sem tags
    # Remove todo código dentro de tags
    text_outside_tags = re.sub(r'<[^>]*>', '', stripped).strip()
    
    # Se o texto fora de tags for longo (mais de 150 chars) e houver menos de 2 tags, provavelmente é redação disfarçada
    if len(text_outside_tags) > 150 and valid_tags_count < 2:
        return False, "O campo HTML parece conter apenas texto corrido. Estruture o conteúdo utilizando elementos HTML adequados."

    return True, ""


def validate_css_code(css_str: str, required: bool = False) -> tuple[bool, str]:
    """
    Valida se a string contém código CSS estruturado válido no formato:
    seletor { propriedade: valor; }
    """
    if not css_str or not css_str.strip():
        if required:
            return False, "O código CSS é obrigatório para esta questão."
        return True, ""

    stripped = css_str.strip()

    # Deve conter blocos com chaves { ... }
    blocks = re.findall(r'([^{]+)\{([^}]+)\}', stripped, re.DOTALL)
    if not blocks:
        return False, "O código CSS deve conter regras com seletores e chaves no formato `seletor { propriedade: valor; }` (ex: `h1 { color: blue; }`)."

    # Verifica dentro de cada bloco se há declarações do tipo prop: valor
    has_valid_declaration = False
    for selector, content in blocks:
        selector = selector.strip()
        # Seletor muito longo sem caracteres típicos de CSS pode ser texto corrido
        if len(selector) > 80 and not re.search(r'^[.#a-zA-Z0-9_\-\s,:>+~*\[\]="\']+$', selector):
            return False, f"Seletor CSS inválido: '{selector[:40]}...'. Escreva seletores CSS válidos (ex: `.btn`, `#titulo`, `div > p`)."

        declarations = [d.strip() for d in content.split(';') if d.strip()]
        for decl in declarations:
            if ':' in decl:
                prop, val = decl.split(':', 1)
                prop = prop.strip().lower()
                val = val.strip()
                if prop in COMMON_CSS_PROPERTIES or re.match(r'^[a-z\-]+$', prop):
                    if len(val) > 0:
                        has_valid_declaration = True

    if not has_valid_declaration:
        return False, "Nenhuma propriedade CSS válida encontrada (ex: `color: #333; font-size: 16px; margin: 10px;`)."

    return True, ""


def validate_js_code(js_str: str, required: bool = False) -> tuple[bool, str]:
    """
    Valida se a string contém código JavaScript válido com palavras-chave,
    manipulação de DOM ou estruturas lógicas de JS.
    """
    if not js_str or not js_str.strip():
        if required:
            return False, "O código JavaScript é obrigatório para esta questão."
        return True, ""

    stripped = js_str.strip()

    # Balanceamento básico de delimitadores
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    in_string = False
    str_char = ''
    escaped = False

    for char in stripped:
        if escaped:
            escaped = False
            continue
        if char == '\\':
            escaped = True
            continue
        if char in ("'", '"', '`'):
            if not in_string:
                in_string = True
                str_char = char
            elif str_char == char:
                in_string = False
            continue
        if in_string:
            continue

        if char in pairs.values():
            stack.append(char)
        elif char in pairs.keys():
            if not stack or stack[-1] != pairs[char]:
                return False, f"Erro de sintaxe JavaScript: delimitador '{char}' não balanceado ou fechado incorretamente."
            stack.pop()

    if stack:
        return False, f"Erro de sintaxe JavaScript: bloco ou parênteses '{stack[-1]}' aberto e não fechado."

    # Procura por palavras-chave ou padrões JS
    matched_patterns = 0
    for pattern in JS_KEYWORD_PATTERNS:
        if re.search(pattern, stripped, re.IGNORECASE):
            matched_patterns += 1

    if matched_patterns == 0:
        return False, "O campo JavaScript não contém instruções ou sintaxe reconhecível de JS (ex: `function`, `const`, `document.getElementById`, `addEventListener`, etc.). Digite código de programação real."

    return True, ""


def validate_web_submission(html_code: str, css_code: str, js_code: str, options: list = None) -> tuple[bool, list[str]]:
    """
    Realiza a validação completa da submissão de questão de Código Web.
    Retorna (is_valid, list_of_errors).
    """
    options = options or []
    errors = []

    req_html = "REQ_HTML" in options or "CODE_WEB" in options or not options  # Padrão: HTML obrigatório
    req_css = "REQ_CSS" in options
    req_js = "REQ_JS" in options

    # 1. HTML
    html_ok, html_err = validate_html_code(html_code, required=req_html)
    if not html_ok:
        errors.append(f"📄 HTML: {html_err}")

    # 2. CSS (se preenchido ou se obrigatório)
    if css_code.strip() or req_css:
        css_ok, css_err = validate_css_code(css_code, required=req_css)
        if not css_ok:
            errors.append(f"🎨 CSS: {css_err}")

    # 3. JS (se preenchido ou se obrigatório)
    if js_code.strip() or req_js:
        js_ok, js_err = validate_js_code(js_code, required=req_js)
        if not js_ok:
            errors.append(f"⚡ JavaScript: {js_err}")

    return len(errors) == 0, errors
