import os

def get_school_name():
    """
    Lê o nome da escola a partir do arquivo de configuração 'Escola.txt'.

    Retorna:
        str: O nome da escola encontrado na primeira linha do arquivo, 
             ou 'SysAva' como um valor padrão se o arquivo não existir.
    """
    # Constrói o caminho para o arquivo a partir da localização deste script
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file = os.path.join(project_root, 'data', 'Turmas', 'Escola.txt')
    
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return f.readline().strip()
    return "SysAva"