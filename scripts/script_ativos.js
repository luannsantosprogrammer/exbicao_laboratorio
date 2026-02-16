// clicando botão do formulário
document.querySelectorAll(".spaceBetweenIcons")[2].click();
function delay(tempo) {
    // função de delay para aguardar processo anterior
    return new Promise(resolve => setTimeout(resolve, tempo));
}

// camptando os inputs do formulário
const seletor = document.querySelectorAll(".ant-picker-input")
delay(2000)

// selecionando a data atual e clicando no campo de data
function selecionandoData(indice){
    seletor[indice].click()
    const data = new Date();

    const datas = document.querySelectorAll(".ant-picker-cell");
    console.log(` ${data.getDate()} `)
    
    
    for (let index = 0; index < datas.length; index++) {
        if (data.getDate() == datas[index].innerText){
            datas[index].click()
            break
        }
        
    }
}

// selecionando a data atual e clicando no campo de data
// e depois selecionando a data de ontem
// para o campo de data final
selecionandoData(0)
delay(2000)
selecionandoData(1)
delay(2000)

// selecionando os inputs do formulário
const inputs = document.querySelectorAll("input");

// função que selecionará opções sugeridas para adiconar no relatório
async function selecionandoLocalidade(numero_input, localidade) {
    inputs[numero_input].click();
    await delay(500);
    document.querySelectorAll(".ant-select-item-option-content")[localidade].click();
}

async function executarTudo() {
    // esses 3 primeiros pegarão rejeitado, cancelado e pendente == não
    await selecionandoLocalidade(13, 1);
    await selecionandoLocalidade(14, 1);
    await selecionandoLocalidade(15, 0);

    // aqui será para a localidade CD
    await selecionandoLocalidade(7, 0);
    await selecionandoLocalidade(8, 11);
    await document.querySelectorAll(".ant-btn")[6].click()

    // aqui será para a localidade Regional
    await selecionandoLocalidade(7, 1);
    await document.querySelectorAll(".ant-btn")[6].click()



}

executarTudo();