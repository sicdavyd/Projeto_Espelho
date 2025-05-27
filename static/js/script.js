document.addEventListener('DOMContentLoaded', function () {
  // Configuração do carrossel
  let indiceAtual = 0;
  const imagens = document.querySelectorAll(".carrossel-img");
  const intervalo = 4000; // 4 segundos

  function mostrarImagem(indice) {
    imagens.forEach((img, i) => {
      img.classList.toggle("ativa", i === indice);
    });
  }

  function avancarImagem() {
    indiceAtual = (indiceAtual + 1) % imagens.length;
    mostrarImagem(indiceAtual);
  }

  // Iniciar carrossel
  mostrarImagem(indiceAtual);
  const carrosselInterval = setInterval(avancarImagem, intervalo);

  // Pausar carrossel quando o mouse estiver sobre ele
  const carrosselContainer = document.querySelector(".carrossel-container");
  if (carrosselContainer) {
    carrosselContainer.addEventListener("mouseenter", () => {
      clearInterval(carrosselInterval);
    });

    carrosselContainer.addEventListener("mouseleave", () => {
      carrosselInterval = setInterval(avancarImagem, intervalo);
    });
  }

  // Mostrar preview da imagem selecionada
  const fileInput = document.getElementById("inputEscolher");
  if (fileInput) {
    fileInput.addEventListener("change", function (e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
          // Substitui o carrossel pela imagem selecionada
          const carrossel = document.querySelector(".carrossel");
          carrossel.innerHTML = `
            <img src="${event.target.result}" class="carrossel-img ativa" 
                 alt="Imagem selecionada" style="object-fit: contain;">
          `;

          // Esconde o overlay de upload
          const overlay = document.querySelector(".upload-overlay");
          if (overlay) overlay.style.display = "none";
        };
        reader.readAsDataURL(file);
      }
    });
  }
});