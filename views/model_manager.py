import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8001"

def get_status():
    try:
        response = requests.get(f"{API_URL}/status")
        return response.json()
    except requests.ConnectionError:
        return {"status": "api_down"}

def show_page():
    st.header("🤖 Gerenciador de Servidor de Modelos Locais")
    st.markdown("---")

    status_data = get_status()
    status = status_data.get("status", "error")

    if status == "api_down":
        st.error("A API de gerenciamento de modelos não está respondendo. Certifique-se de que ela foi iniciada junto com o SysAva.")
        return

    if status == "running":
        st.success(f"**Servidor Ativo** (PID: {status_data.get('pid')})")
        with st.expander("Detalhes do Comando em Execução"):
            st.code(status_data.get('command', 'N/A'), language='bash')
        
        if st.button("Parar Servidor", type="primary", use_container_width=True):
            with st.spinner("Parando o servidor..."):
                try:
                    requests.post(f"{API_URL}/stop")
                    st.toast("Servidor parado!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao parar o servidor: {e}")

    else: # 'stopped' or 'error'
        st.info("**Servidor Parado**")
        
        with st.form("start_server_form"):
            st.subheader("Iniciar Novo Servidor")
            
            try:
                models_response = requests.get(f"{API_URL}/models")
                if models_response.status_code == 200:
                    available_models = models_response.json().get("models", [])
                    if not available_models:
                        st.warning("Nenhum modelo .gguf encontrado no cache do Hugging Face.")
                        selected_model = None
                    else:
                        selected_model = st.selectbox("1. Selecione o Modelo", available_models)
                else:
                    st.error("Falha ao buscar a lista de modelos.")
                    selected_model = None
            except requests.ConnectionError:
                st.error("Falha ao conectar na API para buscar modelos.")
                selected_model = None

            port = st.number_input("2. Porta do Servidor", min_value=1024, max_value=65535, value=8009)
            n_gpu_layers = st.number_input("3. Camadas de GPU (ngl)", min_value=0, help="Use 0 para CPU. Para GPUs Intel, o suporte pode variar (tente 0 primeiro).")

            submitted = st.form_submit_button("Iniciar Servidor", use_container_width=True, disabled=(not selected_model))

            if submitted and selected_model:
                with st.spinner("Enviando comando para iniciar o servidor..."):
                    try:
                        payload = {
                            "model_path": selected_model,
                            "port": port,
                            "n_gpu_layers": n_gpu_layers
                        }
                        response = requests.post(f"{API_URL}/start", json=payload)
                        if response.status_code == 200:
                            st.toast("Comando de inicialização enviado!")
                            time.sleep(2) # Dá tempo para o servidor começar a iniciar
                            st.rerun()
                        else:
                            st.error(f"Erro: {response.json().get('detail')}")
                    except Exception as e:
                        st.error(f"Erro ao iniciar o servidor: {e}")

    st.divider()
    st.subheader("Logs do Servidor")
    if st.button("Atualizar Logs"):
        st.rerun()

    try:
        logs_response = requests.get(f"{API_URL}/logs")
        if logs_response.status_code == 200:
            st.code(logs_response.json().get("logs", ""), language='log')
        else:
            st.warning("Não foi possível carregar os logs.")
    except requests.ConnectionError:
        st.warning("API de gerenciamento indisponível para buscar logs.")