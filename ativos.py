import requests,logs
from datetime import datetime,timedelta
import pandas as pd







horarios_ativos = [
'08:00','08:10','08:30','08:40',
'09:00','09:10','09:30','09:40',
'10:00','10:10','10:30','10:40',
'11:00','11:10','11:30','11:40',
'12:00','12:10','12:30','12:40'
'13:00','13:10','13:30','13:40',
'14:00','14:10','14:30','14:40',
'15:00','15:10','15:30','15:40',
'16:00','16:10','16:30','16:40',
'17:00','17:10','17:30','17:40'
]


# ===================================
# ATIVOS
# ===================================


# ====================================
# Busco os indicadores do site indicadores para nossa utilidade 
# ====================================
def pegando_indicadores_ativos(pagina):

    pagina.reload()
    pagina.wait_for_timeout(5000)
    #pegando dados do indicadores
    pagina.locator(".ant-btn-primary").nth(2).click()
    pagina.wait_for_timeout(2000)
    input = pagina.locator(".ant-select-selection-search-input")
    input.nth(1).click()
    input.nth(1).fill("Laboratório")
    pagina.wait_for_timeout(2000)
    pagina.locator(".ant-select-item-option-content").click()
    pagina.wait_for_timeout(2000)
    pagina.locator(".ant-btn-primary").nth(4).click()
    pagina.reload()
    pagina.wait_for_timeout(2000)
    pagina.query_selector_all(".ant-tabs-tab-btn")[1].click()

    linha1 = pagina.evaluate('() => document.querySelectorAll(".ant-table-row")[1].innerText.includes("Processado")')

    while not linha1:

        pagina.reload()
        pagina.wait_for_timeout(5000)

        # vou até a página de downloads dos indicadores
        pagina.locator(".ant-tabs-tab-btn").nth(1).click()
        pagina.wait_for_timeout(5000)

        linha1 = pagina.evaluate('() => document.querySelectorAll(".ant-table-row")[1].innerText.includes("Processado")')


    botao1 = pagina.locator(".spaceBetweenIcons").nth(0)

    # Primeiro download
    with pagina.expect_download() as download_info1:
        botao1.click()
        pagina.wait_for_timeout(5000)
        
    download1 = download_info1.value
    download1.save_as("arquivos_csv/estoque_por_localidade.csv")
    
    pagina.wait_for_timeout(20000)
    pagina.reload()
    pagina.wait_for_timeout(5000)


# ====================================


def envio_subcategorias(pagina):
    #gerando data de 3 meses atrás a partir da data atual
    mes_atual = datetime.now()
    tres_meses_atras = mes_atual - timedelta(days=90)
    
    # lendo csv
    estoque_por_localidade = pd.read_csv('arquivos_csv/estoque_por_localidade.csv')
    onu = estoque_por_localidade.sort_values(
        by='data_ultima_movimentacao_hstorico',
        ascending=True
    )

    #filtrando ONU e alterando os nan para se adequar a api do appscript
    onu = estoque_por_localidade[estoque_por_localidade['nome_item'].str.contains('Onu',case=False)].fillna(' ')

    #transformando a coluna data_ultima_movimentacao_confirmada em datetime 
    onu['data_ultima_movimentacao_confirmada'] = pd.to_datetime(onu['data_ultima_movimentacao_confirmada'])

    #filtrando dados de 3 meses atrás até a data atual
    onu = onu[onu['data_ultima_movimentacao_confirmada'] >= tres_meses_atras]

    #transformando em tipo texto para se adequar a api
    onu = onu.astype(str)

    #pegando as colunas necessárias 
    onu = onu[['numero_serie','nome_subcategoria','data_ultima_movimentacao_confirmada']]
    numero_serie_subcategoria = [onu.columns.tolist()] + onu.values.tolist()
    
    pagina.wait_for_timeout(5000)

    #enviando para a planilha
    url = ''

    requests.post(url, json={'dados':numero_serie_subcategoria})
    pagina.wait_for_timeout(5000)
    

def envio_roteadores(pagina):

    #gerando data de 3 meses atrás a partir da data atual
    mes_atual = datetime.now()
    tres_meses_atras = mes_atual - timedelta(days=90)

    # lendo csv
    sheet = pd.read_csv('arquivos_csv/estoque_por_localidade.csv')

    #transformando a coluna data_ultima_movimentacao_confirmada em datetime 
    sheet['data_ultima_movimentacao_confirmada'] = pd.to_datetime(sheet['data_ultima_movimentacao_confirmada'])

    #filtrando apenas roteadores
    sheet = sheet[sheet["nome_item"].str.contains("Roteador")]

    #retirando os que contém Cpe
    nao_cpe = sheet[~sheet["nome_item"].str.contains("Cpe")]

    #retirando os que contém Fwa
    nao_fwa = nao_cpe[~nao_cpe["nome_item"].str.contains("Fwa")]

    #filtrando dados de 3 meses atrás até a data atual
    apenas_roteadores = nao_fwa[nao_fwa['data_ultima_movimentacao_confirmada'] >= tres_meses_atras]

    #transformando em tipo texto para se adequar a api
    apenas_roteadores = apenas_roteadores.astype(str)

    #pegando as colunas necessárias 
    apenas_roteadores = apenas_roteadores[['numero_serie','nome_item','nome_localidade']]

    roteadores = apenas_roteadores.values.tolist()

    pagina.wait_for_timeout(5000)
    url = ''
    requests.post(url, json={'dados':roteadores})


def sub_categorias_e_roteadores():

    horario_atual = datetime.now().strftime("%H:%M")

    if horario_atual in horarios_ativos:
        pagina = logs.abrir_navegador(True,
                    "",
                    ".config/google-chrome/ativos_dash"
                                        )

        logs.certifica_login(pagina,"Indicadores",
                    ".config/google-chrome/ativos_dash",
                    ""
                    )
        logs.logs_ativos('Buscando indicadores dos Ativos')
        
        pegando_indicadores_ativos(pagina)

        logs.logs_ativos('Indicadores dos ativos pegos com sucesso!')

        pagina.wait_for_timeout(3000)
        requests.post('http://localhost:5000/status',
                                json={'status':'Indicadores dos ativos pegos com sucesso!'})
        
        logs.logs_ativos('Iniciando envio dos indicadores dos subcategorias')

        envio_subcategorias(pagina)

        pagina.wait_for_timeout(3000)

        logs.logs_ativos('Iniciando envio dos indicadores dos roteadores')

        envio_roteadores(pagina)

        logs.logs_ativos('Sub e Roteadores enviados com sucesso!')

        pagina.close()

sub_categorias_e_roteadores()