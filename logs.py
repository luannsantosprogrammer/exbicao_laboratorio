import requests
import os
from playwright.sync_api import sync_playwright


CAMINHO = os.getcwd()


# ====================================
# Abrindo navegador para iniciar e automação
# ====================================
def abrir_navegador(visibilidade, link,local):
    playwright = sync_playwright().start()

    navegador = playwright.chromium.launch_persistent_context(
        user_data_dir=f"{CAMINHO}/{local}",
        headless=visibilidade
    )

    pagina = navegador.pages[0]
    pagina.goto(link)
    pagina.wait_for_timeout(5000)
    return pagina

def certifica_login(pagina,automacao,local,link):
    if 'login' in pagina.url:
        pagina.close()
        abrir_navegador(False,link,local)
        # aviso_de_erro('Você não está logado no Brisa Indicadores')
        logs_dash(f"Precisa logar no {automacao}")

        enter = input("Log, aperte enter")



# ===================================
# Status de log das automações
# ===================================

# ==================================
def logs_ativos(mensagem):
    url  = ''
    requests.post(url, json={"log_ativos.txt":mensagem})
    

def logs_dash(mensagem):
    url  = ''
    requests.post(url, json={"log_dash.txt":mensagem})
    


def logs_inspecao(mensagem):
    url  = ''
    resposta = requests.post(url, json={"ativo":[mensagem]})


