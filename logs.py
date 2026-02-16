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
    url  = 'https://script.google.com/macros/s/AKfycbxXjnUYBI1Uw4S2H9C0UDL8I95Oh9YV1KnOfmr0bgu7OaZ_OZMj5hxE_avtEYCG9_UZnw/exec'
    requests.post(url, json={"log_ativos.txt":mensagem})
    

def logs_dash(mensagem):
    url  = 'https://script.google.com/macros/s/AKfycbxXjnUYBI1Uw4S2H9C0UDL8I95Oh9YV1KnOfmr0bgu7OaZ_OZMj5hxE_avtEYCG9_UZnw/exec'
    requests.post(url, json={"log_dash.txt":mensagem})
    


def logs_inspecao(mensagem):
    url  = 'https://script.google.com/macros/s/AKfycbyIeB7JmTITA92lYqDAkWGII44D8CSo2MqCp-7tqFZfl2b6NwEtHFZ2wPembtgaECs2Aw/exec'
    resposta = requests.post(url, json={"ativo":[mensagem]})


