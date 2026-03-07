import streamlit as st

def show_page():
    st.header("📺 Sala de Aula Virtual")
    
    aula_selecionada = st.selectbox("Escolha a aula:", 
        ["Aula 1: Introdução ao Python", "Aula 2: Data Science Básico", "Aula 3: Streamlit Avançado"])
    
    st.divider()
    
    if aula_selecionada == "Aula 1: Introdução ao Python":
        st.subheader("Aula 1: Conceitos Fundamentais")
        st.video("https://www.youtube.com/watch?v=rfscVS0vtbw") 
        st.markdown("**Resumo da Aula:**\nNesta aula aprendemos sobre variáveis, tipos de dados e estruturas de controle.")
    elif aula_selecionada == "Aula 2: Data Science Básico":
        st.subheader("Aula 2: Manipulando Dados")
        st.info("Vídeo da Aula 2 estaria aqui.")
        st.markdown("Conteúdo sobre Pandas e NumPy.")
    else:
        st.subheader("Aula 3: Criando Web Apps")
        st.info("Vídeo da Aula 3 estaria aqui.")