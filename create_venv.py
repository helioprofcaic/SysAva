# create_venv.py
import os
import subprocess
import sys

venv_dir = ".sysenv"

def create_virtualenv():
    print(f"Usando Python: {sys.executable}")
    print(f"Versão do Python: {sys.version}")

    print("Criando ambiente virtual...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        print("Ambiente virtual criado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao criar ambiente virtual: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_virtualenv()
