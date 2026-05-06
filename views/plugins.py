import streamlit as st
from services import database as db
import os
import re
import sys
import subprocess
import base64

# Tenta importar o visualizador de PDF, se não existir, a funcionalidade ficará desabilitada.
try:
    from streamlit_pdf_viewer import pdf_viewer
    PDF_VIEWER_AVAILABLE = True
except ImportError:
    PDF_VIEWER_AVAILABLE = False

def find_local_pdfs():
    """Encontra todos os arquivos PDF nos diretórios de dados."""
    pdf_files = {}
    search_paths = [os.path.join("data", "repo", "ebooks"), os.path.join("data", "Turmas")]
    
    for path in search_paths:
        if os.path.exists(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.lower().endswith(".pdf"):
                        # Usa o caminho relativo como chave para evitar nomes duplicados
                        relative_path = os.path.relpath(os.path.join(root, file), "data")
                        pdf_files[relative_path] = os.path.join(root, file)
    return pdf_files

def show_page():
    st.header("🧩 Extensões e Plugins")

    # Verificação de permissão
    if st.session_state.get('role') not in ['admin', 'teacher']:
        st.error("Acesso negado. Esta área é restrita a professores e administradores.")
        return

    st.markdown("""
    Esta seção permite executar funcionalidades nativas e scripts Python externos para estender as capacidades do SysAva.
    """)

    tab_native, tab_external = st.tabs(["🔌 Plugins Nativos", "📂 Plugins Externos (data/repo/plugins)"])

    # --- Aba de Plugins Nativos ---
    with tab_native:
        with st.expander("🎓 Gerador de Certificados (Exemplo)"):
            st.info("Exemplo de integração de um componente para gerar certificados de conclusão.")

            # Lógica para selecionar aluno e curso para gerar certificado
            classes_cert = db.get_classes()
            if not classes_cert:
                st.warning("Nenhuma turma cadastrada para emitir certificados.")
            else:
                class_options_cert = {c['name']: c['id'] for c in classes_cert}
                selected_class_name_cert = st.selectbox("Selecione a Turma para emitir certificados", options=["-- Selecione --"] + list(class_options_cert.keys()), key="cert_class")

                if selected_class_name_cert != "-- Selecione --":
                    class_id_cert = class_options_cert[selected_class_name_cert]
                    students_cert = db.get_students_by_class(class_id_cert)
                    student_options_cert = {s['name']: s['username'] for s in students_cert}
                    
                    selected_student_name_cert = st.selectbox("Selecione o Aluno", options=["-- Selecione --"] + list(student_options_cert.keys()), key="cert_student")

                    if selected_student_name_cert != "-- Selecione --":
                        st.success(f"Pronto para gerar o certificado para **{selected_student_name_cert}** da turma **{selected_class_name_cert}**.")
                        if st.button("📄 Gerar Certificado (Exemplo)"):
                            st.balloons()
                            st.success("Certificado gerado! (Esta é uma demonstração da funcionalidade).")
        
        st.divider()
        st.markdown("### 📚 Leitor de E-books (PDF)")

        if not PDF_VIEWER_AVAILABLE:
            st.error("O componente de visualização de PDF não está instalado. Execute `pip install streamlit-pdf-viewer` no seu terminal.")
        else:
            pdf_files_map = find_local_pdfs()
            if not pdf_files_map:
                st.warning("Nenhum arquivo PDF encontrado nas pastas `data/repo/ebooks` ou `data/Turmas`.")
            else:
                # Exibe os nomes dos arquivos de forma mais amigável
                display_names = sorted(list(pdf_files_map.keys()))
                selected_pdf_key = st.selectbox("Selecione um e-book para ler:", ["-- Selecione --"] + display_names)

                if selected_pdf_key != "-- Selecione --":
                    pdf_path = pdf_files_map[selected_pdf_key]
                    try:
                        with open(pdf_path, "rb") as f:
                            pdf_data = f.read()
                        pdf_viewer(pdf_data)
                    except Exception as e:
                        st.error(f"Não foi possível abrir o PDF: {e}")

    # --- Aba de Plugins Externos ---
    with tab_external:
        st.markdown("### 📂 Executar Plugins Externos")
        st.warning("⚠️ **Atenção:** Esta funcionalidade executa scripts Python diretamente. Use apenas scripts de fontes confiáveis.")

        plugins_dir = os.path.join("data", "repo", "plugins")

        if not os.path.exists(plugins_dir):
            st.info(f"Para adicionar plugins externos, crie a pasta `{plugins_dir}` e coloque seus arquivos `.py` nela.")
        else:
            try:
                plugin_files = [f for f in os.listdir(plugins_dir) if f.endswith(".py")]
                if not plugin_files:
                    st.info(f"Nenhum plugin (`.py`) encontrado na pasta `{plugins_dir}`.")
                else:
                    st.success(f"Encontrados {len(plugin_files)} plugins:")
                    for plugin_file in plugin_files:
                        plugin_path = os.path.join(plugins_dir, plugin_file)
                        with st.expander(f"**{plugin_file}**"):
                            # Tenta ler a docstring do arquivo para exibir como descrição
                            try:
                                with open(plugin_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    docstring_match = re.match(r'^\s*"""(.*?)"""', content, re.DOTALL)
                                    if docstring_match:
                                        st.caption(docstring_match.group(1).strip())
                                    else:
                                        st.caption("Nenhuma descrição (docstring) encontrada no início do script.")
                            except Exception:
                                st.caption("Não foi possível ler a descrição do arquivo.")

                            if st.button(f"Executar {plugin_file}", key=f"run_{plugin_file}"):
                                with st.spinner(f"Executando {plugin_file}..."):
                                    # Usamos sys.executable para garantir que o script rode com o mesmo interpretador Python do Streamlit
                                    result = subprocess.run(
                                        [sys.executable, plugin_path],
                                        capture_output=True,
                                        text=True,
                                        encoding='utf-8'
                                    )
                                    st.markdown("---")
                                    st.markdown("#### ✅ Resultado da Execução:")
                                    if result.stdout:
                                        st.code(result.stdout, language='bash')
                                    if result.stderr:
                                        st.error("Ocorreram erros durante a execução:")
                                        st.code(result.stderr, language='bash')
                                    if not result.stdout and not result.stderr:
                                        st.info("O script foi executado mas não produziu nenhuma saída no console.")
            except Exception as e:
                st.error(f"Ocorreu um erro ao listar os plugins: {e}")