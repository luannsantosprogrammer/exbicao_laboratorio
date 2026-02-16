var botoes = document.querySelectorAll(".ant-btn-primary");
botoes[3].click()
function buscandoDados(){
// pegando inputs
var inputs = document.querySelectorAll("input")
//pegando o input data
inputs[3].click()
const numerosData = document.querySelectorAll(".ant-picker-cell-in-view")
//selecionando primeiro dia do mes
document.querySelectorAll(".ant-picker-cell-in-view")[0].click()
const data = new Date();
// selecionando o ultimo dia do mes
for(var i = 0;i < numerosData.length;i++){
  if(numerosData[i].innerText == data.getDate()){
    numerosData[i].click()
  }
}

async function localidades(campoLocalidade, localidade) {
    // Clica no campo desejado
    inputs[campoLocalidade].click();

    // Espera até que as opções estejam visíveis
    await new Promise(resolve => setTimeout(resolve, 1000)); // Aqui você pode trocar por um observer também

    // Clica na opção desejada
    document.querySelectorAll(".ant-select-item-option-content")[localidade].click();
}

// Agora executa elas em sequência:
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
    // localidade laboratório
  await localidades(7, 11);
  await localidades(8, 0);
  await delay(500);
  document.querySelectorAll(".ant-btn-primary")[4].click();
  await localidades(8, 1);
  await delay(500);
  document.querySelectorAll(".ant-btn-primary")[4].click();

  //localidade fornecedor
  await localidades(7, 10);
  await localidades(8, 0);
  await delay(500);
  document.querySelectorAll(".ant-btn-primary")[4].click();
  await localidades(8, 1);
  await delay(500);
  document.querySelectorAll(".ant-btn-primary")[4].click();

  await localidades(7, 11);
  await localidades(8, 4);
  await delay(4000);
  document.querySelectorAll(".ant-btn-primary")[4].click();

})();

}  

setTimeout(
    ()=>{        
        buscandoDados();      
    },3000
)
