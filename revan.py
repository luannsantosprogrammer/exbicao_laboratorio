from playwright.sync_api import sync_playwright
import requests
import schedule
from datetime import datetime
import pandas as pd
import logs


# ====================================
# Abrindo navegador para iniciar e automação
# ====================================

def abrir_navegador_revan(visibilidade):
    playwright = sync_playwright().start()

    navegador = playwright.chromium.launch_persistent_context(
        user_data_dir=f"{logs.CAMINHO}/.config2/google-chrome/revan",
        headless=visibilidade
    )

    pagina = navegador.pages[0]
    pagina.goto("")
    pagina.wait_for_timeout(5000)
    return pagina


pagina = abrir_navegador_revan(False)


# ====================================
# tratando os dados para que se faça a varredura dos mesmos
# ====================================
def trantando_ativos():

    hoje = datetime.now().strftime("%Y-%m-%d")
    vistoriados = open('arquivos_txt/vistoriados.txt').read()

    dados = pd.read_csv("arquivos_csv/estoque_por_localidade.csv")
    somente_onu = dados[dados['nome_item'].str.contains("Onu", case=False).fillna('')]
    dados_de_hoje = somente_onu[somente_onu['data_ultima_movimentacao_confirmada'] == hoje]
    numero_de_serie = dados_de_hoje['numero_serie'].values.tolist()

    para_vistoriar = [aparelho  for aparelho in numero_de_serie if aparelho not in vistoriados]

    return para_vistoriar

# ====================================
# Fazendo a varredura no Revan para separar as ONUs que estão ainda cadastradas em nome de cliente 
# ====================================
def buscando_ativos(dados):

    neste_momento = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # aqui será feita a varredura dos numeros de série no revan

    lista_para_enviar = [] #lista que guardará numeros de série que serão enviados para a planilha 
    logs.logs_inspecao("Fazendo varredura de ativos")
    for i,serie in enumerate(dados):
        if 'login' in pagina.url: #certificar que ainda está logado
            logs.logs_inspecao('O Revan está deslogado')
            enter = input("Log, aperte enter!")

        pagina.fill('//*[@id="filters"]',serie) #adicionar numero no campo
        pagina.keyboard.press("Enter") #apertar enter para buscar
        pagina.wait_for_timeout(2000)
        
        try:
            #caso apareça a tabela, irá exibir o numero e adicionar ao lista
            #caso contrário, cairá na excessão e passará para próximo numero
            tabela = pagina.locator('//*[@id="main"]/div/div/div[2]/div/div[1]/bn-table/div/div[2]/table/tbody/tr/td[4]').wait_for(timeout=1200)
            lista_para_enviar.append([serie])
            logs.logs_inspecao(f'achei {serie}')


        except:
            ...
        

        # arquivando os numeros que já passaram para que não ocorra uma re-checagem
        with open(f"arquivos_txt/vistoriados.txt", "a") as file:
            file.write(f"{serie}\n")
            

    # se tiver itens para serem enviados, estarão guardados no txt
    if lista_para_enviar != []:
        with open(f'arquivos_txt/ativos_achados-{neste_momento}.txt', 'a') as arquivo:
            for num in lista_para_enviar:   
                arquivo.write(f"{num}\n")

            arquivo.close()

    logs.logs_inspecao("Varredura de ativos finalizada")



# ====================================
def inspecao_revan():
    global pagina
    try:
        if 'login' in pagina.url:
            # aviso_de_erro('Você não está logado no Brisa Indicadores')
            logs.logs_inspecao("Precisa logar no revan")
            enter = input("Log, aperte enter ")

        resposta_indicadores = requests.get('http://localhost:5000/status').json()
        if resposta_indicadores['status'] == 'Indicadores dos ativos pegos com sucesso!':

            logs.logs_inspecao("Verificando se há ONUs para varredura")

            dados = trantando_ativos()
            if dados != []:
                buscando_ativos(dados)
            else:
                logs.logs_inspecao("Não há ONUs para varredura")


            requests.post('http://localhost:5000/status',
                            json={'status':'aguardando'})


        

            
    except Exception as e:
   
        logs.logs_inspecao("Erro ao inspecionar os dados")

    



schedule.every(1).seconds.do(inspecao_revan)

while True:
    pagina.wait_for_timeout(1000)
    schedule.run_pending()



