import os,requests
from time import sleep
from datetime import datetime,timedelta
import pandas as pd
import logs




horarios_dash = [
    "07:50","08:20","08:50",
    "09:20","09:50","10:20",
    "10:50","11:20","11:50",
    "12:20","12:50","13:20",
    "13:50","14:20","14:50",
    "15:20","15:50","16:20",
    "16:50","17:20","Final de expediente. Obrigado, bom Descanso!"
]



# ===================================
# EXIBIÇÃO
# ===================================



# =============================

def pegando_indicadores_dash(pagina):
    

    pagina.reload()
    pagina.wait_for_timeout(5000)
    # executando o script_dash.js que fará a busca dos dados em relação a cada indicador que nos favorece
    script_dash = open("scripts/script_dash.js","r").read() 
    pagina.evaluate(script_dash)

    pagina.wait_for_timeout(20000)
    pagina.reload()
    pagina.wait_for_timeout(2000)
    
    # segue para a página de dowloads dos arquivos csv
    pagina.locator(".ant-tabs-tab-btn").nth(1).click()
    pagina.wait_for_timeout(5000)



    linha1 = pagina.evaluate('() => document.querySelectorAll(".ant-table-row")[1].innerText.includes("Processado")')
    linha2 = pagina.evaluate('() => document.querySelectorAll(".ant-table-row")[2].innerText.includes("Processado")')
    linha3 = pagina.evaluate('() => document.querySelectorAll(".ant-table-row")[3].innerText.includes("Processado")')
    linha4 = pagina.evaluate('() => document.querySelectorAll(".ant-table-row")[4].innerText.includes("Processado")')
    linha5 = pagina.evaluate('() => document.querySelectorAll(".ant-table-row")[5].innerText.includes("Processado")')

    while not linha1 or not linha2 or not linha3 or not linha4 or not linha5:


        pagina.reload()
        pagina.wait_for_timeout(5000)

        # vou até a página de downloads dos indicadores
        pagina.locator(".ant-tabs-tab-btn").nth(1).click()
        pagina.wait_for_timeout(5000)

        linha1 = pagina.evaluate('() => document.querySelectorAll(".ant-table-row")[1].innerText.includes("Processado")')
        linha2 = pagina.evaluate('() => document.querySelectorAll(".ant-table-row")[2].innerText.includes("Processado")')
        linha3 = pagina.evaluate('() => document.querySelectorAll(".ant-table-row")[3].innerText.includes("Processado")')
        linha4 = pagina.evaluate('() => document.querySelectorAll(".ant-table-row")[4].innerText.includes("Processado")')
        linha5 = pagina.evaluate('() => document.querySelectorAll(".ant-table-row")[5].innerText.includes("Processado")')

    botao1 = pagina.locator(".spaceBetweenIcons").nth(0)
    botao2 = pagina.locator(".spaceBetweenIcons").nth(1)
    botao3 = pagina.locator(".spaceBetweenIcons").nth(2)
    botao4 = pagina.locator(".spaceBetweenIcons").nth(3)
    botao5 = pagina.locator(".spaceBetweenIcons").nth(4)



    def download(botao,nome_do_arquivo):
      with pagina.expect_download() as download_info: 
            for _ in range(3):
                botao.click()
            pagina.wait_for_timeout(1000)
            for _ in range(2):
                botao.click()
            pagina.wait_for_timeout(1000)

      download = download_info.value
      download.save_as(nome_do_arquivo)

    
    download(botao1,"arquivos_csv/labotatorio_sustentabilidade.csv")
    download(botao2,"arquivos_csv/fornecedor_regional.csv")
    download(botao3,"arquivos_csv/fornecedor_cd.csv")
    download(botao4,"arquivos_csv/laboratorio_regional.csv")
    download(botao5,"arquivos_csv/laboratorio_cd.csv")

    def download(botao,nome_do_arquivo):
        with pagina.expect_download() as download_info: 
            for _ in range(3):
                botao.click()
            pagina.wait_for_timeout(1000)
            for _ in range(2):
                botao.click()
            pagina.wait_for_timeout(1000)

        download = download_info.value
        download.save_as(nome_do_arquivo)
    pagina.wait_for_timeout(5000)



# =============================

# =============================
# Tratando os indicadores para que sejam enviandos os dados de forma correta
# =============================
def trantando_dados_dash():

    sustentabilidade = pd.read_csv('arquivos_csv/labotatorio_sustentabilidade.csv')

    fornecedor_regional = pd.read_csv('arquivos_csv/fornecedor_regional.csv')
    fornecedor_cd = pd.read_csv('arquivos_csv/fornecedor_cd.csv')
    laboratorio_cd = pd.read_csv('arquivos_csv/laboratorio_cd.csv')
    laboratorio_regional= pd.read_csv('arquivos_csv/laboratorio_regional.csv')
    sustentabilidade = sustentabilidade[sustentabilidade['deposito_destino_nome'] == 'Setor de sustentabilidade']
    uniao = pd.concat([sustentabilidade,fornecedor_cd,fornecedor_regional,laboratorio_cd,laboratorio_regional],ignore_index=True)
    uniao_filtrada = uniao[(uniao['estado_item_transacao'] != 'Rejeitado') & (uniao['estado_item_transacao'] != 'Cancelado')].fillna("")
    dados = [uniao_filtrada.columns.tolist()] + uniao_filtrada.values.tolist()
    return dados
# ============================

# ============================
# Enviando dados para a planilha do google
# ============================

def enviar_dash(dados):
     
    url_dash = ''
    requests.post(url_dash,json={'dados':dados})



def dash():

    horario_atual = datetime.now().strftime("%H:%M")
    if horario_atual in horarios_dash:
        resultado = "erro"
        while resultado == "erro":
            try:
                pagina = logs.abrir_navegador(True,
                    "",
                    ".config/google-chrome/ativos_dash"
                                        )

                logs.certifica_login(pagina,"Indicadores",
                            ".config/google-chrome/ativos_dash",
                            ""
                            )

                logs.logs_dash('Buscando indicadores do Exibição')

                pegando_indicadores_dash(pagina)

                pagina.wait_for_timeout(3000)

                logs.logs_dash('Indicadores do Exibição pegos com sucesso!')

                dados = trantando_dados_dash()

                logs.logs_dash('Enviando dados para o Exibição')

                enviar_dash(dados)

                logs.logs_dash('Exibição atualizado')

                resultado = "sucesso"

            except Exception as e:
                logs.logs_dash("Erro. Tentaremos assim que pudermos")
                continue

        pagina.close()

dash()