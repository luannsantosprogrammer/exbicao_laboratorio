function tempo(){
    return new Promise(resolve => setTimeout(resolve, 2000));
}
async function main(){
var botoes = document.querySelectorAll(".ant-btn-primary");
 await botoes[2].click()
 await tempo();
let campoLocalidade = document.querySelectorAll(".ant-select-selection-search-input")[1];
await campoLocalidade.click();
document.dispatchEvent(new Event('click', { bubbles: true }));
await tempo();

campoLocalidade.value = "Laboratório";
campoLocalidade.dispatchEvent(new Event('input', { bubbles: true }));
await tempo();


document.querySelector(".ant-select-item-option-content").click();
await document.querySelectorAll(".ant-btn-primary")[4].click();
}

main();