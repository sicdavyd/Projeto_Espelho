let indiceAtual = 0;
const imagens = document.querySelectorAll(".containerCarrossel img");

function mostrarImagem(indice) {
  imagens.forEach((img, i) => {
    img.classList.toggle("ativa", i === indice);
  });
}

function avancarImagem() {
  indiceAtual = (indiceAtual + 1) % imagens.length;
  mostrarImagem(indiceAtual);
}

function voltarImagem() {
  indiceAtual = (indiceAtual - 1 + imagens.length) % imagens.length;
  mostrarImagem(indiceAtual);
}

// Iniciar mostrando a primeira imagem
mostrarImagem(indiceAtual);

setInterval(avancarImagem,4000)
//input
document.querySelector(".carrossel").addEventListener("click", () => {
    document.getElementById("inputEscolher").click();
  });
// final input  