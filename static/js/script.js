document.addEventListener('DOMContentLoaded', function () {
  // Elementos do modal
  const modal = document.getElementById('uploadModal');
  const navButton = document.getElementById('navButton');
  const ctaButton = document.getElementById('ctaButton');
  const closeButton = document.querySelector('.close-button');
  const uploadForm = document.getElementById('uploadForm');

  // Carrossel da página principal
  const mainCarouselImages = document.querySelectorAll('.carousel-img');
  let mainCarouselIndex = 0;

  // Carrossel do modal
  const modalCarouselImages = document.querySelectorAll('.carrossel-img');
  let modalCarouselIndex = 0;

  // Funções para mostrar/ocultar modal
  function openModal() {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
  }

  // Event listeners para os botões
  if (navButton) navButton.addEventListener('click', openModal);
  if (ctaButton) ctaButton.addEventListener('click', openModal);
  if (closeButton) closeButton.addEventListener('click', closeModal);

  // Fechar modal ao clicar fora
  modal.addEventListener('click', function (e) {
    if (e.target === modal) closeModal();
  });

  // Carrossel da página principal
  function showNextMainImage() {
    mainCarouselImages[mainCarouselIndex].classList.remove('active');
    mainCarouselIndex = (mainCarouselIndex + 1) % mainCarouselImages.length;
    mainCarouselImages[mainCarouselIndex].classList.add('active');
  }

  // Carrossel do modal
  function showNextModalImage() {
    modalCarouselImages[modalCarouselIndex].classList.remove('ativa');
    modalCarouselIndex = (modalCarouselIndex + 1) % modalCarouselImages.length;
    modalCarouselImages[modalCarouselIndex].classList.add('ativa');
  }

  // Iniciar carrosseis
  if (mainCarouselImages.length > 0) {
    mainCarouselImages[0].classList.add('active');
    setInterval(showNextMainImage, 3000);
  }

  if (modalCarouselImages.length > 0) {
    modalCarouselImages[0].classList.add('ativa');
    setInterval(showNextModalImage, 3000);
  }

  // Preview da imagem selecionada
  const fileInput = document.getElementById('inputEscolher');
  if (fileInput) {
    fileInput.addEventListener('change', function (e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
          // Substitui o carrossel pela imagem selecionada
          const carrossel = document.querySelector('.carrossel');
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

  // Efeitos hover nos botões
  if (navButton) {
    navButton.addEventListener('mouseenter', function () {
      this.style.transform = 'translateY(-2px)';
    });

    navButton.addEventListener('mouseleave', function () {
      this.style.transform = 'translateY(0)';
    });
  }

  if (ctaButton) {
    ctaButton.addEventListener('mouseenter', function () {
      this.style.transform = 'translateY(-3px)';
    });

    ctaButton.addEventListener('mouseleave', function () {
      this.style.transform = 'translateY(0)';
    });
  }
});