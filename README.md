# exbicao_laboratorio
Ecossistema de exibição e envio de dados para outros processos de automações do ambiente de trabalho;

*Aqui são estabelecidos os horários que a automação deve proseguir com o processo*


dash.py
horarios_dash = [
    "07:50","08:20","08:50",
    "09:20","09:50","10:20",
    "10:50","11:20","11:50",
    "12:20","12:50","13:20",
    "13:50","14:20","14:50",
    "15:20","15:50","16:20",
    "16:50","17:20","Final de expediente. Obrigado, bom Descanso!"
]
`


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

 
## Dash


A função **pegando_indicadores_dash** é uma automação na web em que uma página da empresa é acessado, buscando pelos filtros e baixando CSVs.
Utilizei scripts em JS para otimizar a automação dividindo resposabilidades e diminuindo o aumento de cache.



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




A função **trantando_dados_dash** faz o tratamento limpando dados de acordo com o KPI

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




Esta função serve para enviar os dados para uma API App Script, pois o destino será uma planilha do Google



    def enviar_dash(dados):

        url_dash = ''
        requests.post(url_dash,json={'dados':dados})



---

## Ativos

A função **pegando_indicadores_ativos** serve para buscar os dados através de uma página da empresa




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




Envio os dados pegos pela função anterior salvos numa pasta em formato CSV. Porém, antes de serem enviados serão tratados conforme estabelecido pela equipe. Esses dados serão utilizados para automações do App Script dentro de um Google Planilhas



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

        onu = onu[['numero_serie','nome_subcategoria','data_ultima_movimentacao_confirmada']]
        numero_serie_subcategoria = [onu.columns.tolist()] + onu.values.tolist()

        pagina.wait_for_timeout(5000)

        #enviando para a planilha
        url = ''

        requests.post(url, json={'dados':numero_serie_subcategoria})
        pagina.wait_for_timeout(5000)


        def envio_roteadores(pagina):

            mes_atual = datetime.now()
            tres_meses_atras = mes_atual - timedelta(days=90)

            sheet = pd.read_csv('arquivos_csv/estoque_por_localidade.csv')

            sheet['data_ultima_movimentacao_confirmada'] = pd.to_datetime(sheet['data_ultima_movimentacao_confirmada'])

            sheet = sheet[sheet["nome_item"].str.contains("Roteador")]

            nao_cpe = sheet[~sheet["nome_item"].str.contains("Cpe")]

            nao_fwa = nao_cpe[~nao_cpe["nome_item"].str.contains("Fwa")]

            apenas_roteadores = nao_fwa[nao_fwa['data_ultima_movimentacao_confirmada'] >= tres_meses_atras]

            apenas_roteadores = apenas_roteadores.astype(str)

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



---

## Revan

Com a automação do revan, aproveito os dados baixados pela automação do Ativos e busco equipamentos que ainda estão em nome de clientes e físicamente na empresa usando os números de série dos equipamentos. Isto é uma automação na web numa página da empresa. Caso o equipamento esteja em nome de cliente, enviará um mensagem para colaboradores e eles farão as tratativas necessárias.




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



    def trantando_ativos():

        hoje = datetime.now().strftime("%Y-%m-%d")
        vistoriados = open('arquivos_txt/vistoriados.txt').read()

        dados = pd.read_csv("arquivos_csv/estoque_por_localidade.csv")
        somente_onu = dados[dados['nome_item'].str.contains("Onu", case=False).fillna('')]
        dados_de_hoje = somente_onu[somente_onu['data_ultima_movimentacao_confirmada'] == hoje]
        numero_de_serie = dados_de_hoje['numero_serie'].values.tolist()

        para_vistoriar = [aparelho  for aparelho in numero_de_serie if aparelho not in vistoriados]

        return para_vistoriar


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









---

## Logs

O arquivo logs.py ficam os códigos de envio de mensagens para que eu , desevolvedor possa monitorar essas automações do ecossistema.


    import requests
    import os
    from playwright.sync_api import sync_playwright


    CAMINHO = os.getcwd()


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




    def logs_ativos(mensagem):
        url  = ''
        requests.post(url, json={"log_ativos.txt":mensagem})


    def logs_dash(mensagem):
        url  = ''
        requests.post(url, json={"log_dash.txt":mensagem})



    def logs_inspecao(mensagem):
        url  = ''
        resposta = requests.post(url, json={"ativo":[mensagem]})








## Arquivos bash

Ambos arquivos bash servem para manter o ecossitema ativo. Evitar mais consumo de memória ram.



    ativos_dash.sh
    #!/bin/bash


    while true; do
        python3 /home/luann.santos/Documentos/ativos_dash/dash.py
        sleep 1
        python3 /home/luann.santos/Documentos/ativos_dash/ativos.py
    done





    #!/bin/bash

    while true; do
        revan=$(python3 revan.py)
        
        # Verifica o código de saída do Python
        if [ $? -ne 0 ]; then
            echo "O script revan.py encontrou um erro. Tentando novamente em breve..."
            sleep 5  # Espera 5 segundos antes de tentar de novo
        fi
    done



