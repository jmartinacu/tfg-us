document.addEventListener("DOMContentLoaded", function() {
    const wrapper = document.querySelector('.carousel-wrapper');
    const carousel = document.querySelector('.carousel-images');
    const prevBtn = document.querySelector('.carousel-button.prev');
    const nextBtn = document.querySelector('.carousel-button.next');
    let scrollAmount = 0;

    function getMaxScroll() {
        return carousel.scrollWidth - wrapper.clientWidth;
    }

    function updateJustifyContent() {
        if (carousel.scrollWidth > wrapper.clientWidth) {
            carousel.style.justifyContent = "flex-start";
        } else {
            carousel.style.justifyContent = "center";
        }
    }

    function carouselScrollRight() {
        const maxScroll = getMaxScroll();
        if (scrollAmount < maxScroll) {
            scrollAmount = Math.min(scrollAmount + wrapper.clientWidth, maxScroll);
            carousel.style.transform = `translateX(-${scrollAmount}px)`;
        }
        updateButtons();
    }

    function carouselScrollLeft() {
        if (scrollAmount > 0) {
            scrollAmount = Math.max(scrollAmount - wrapper.clientWidth, 0);
            carousel.style.transform = `translateX(-${scrollAmount}px)`;
        }
        updateButtons();
    }

    function updateButtons() {
        prevBtn.disabled = scrollAmount <= 0;
        nextBtn.disabled = scrollAmount >= getMaxScroll() - 1;
    }

    // Inicializar eventos
    prevBtn.addEventListener('click', carouselScrollLeft);
    nextBtn.addEventListener('click', carouselScrollRight);

    window.addEventListener('resize', function() {
        // Si el scroll actual es mayor que el nuevo máximo, reajusta
        if (scrollAmount > getMaxScroll()) {
            scrollAmount = getMaxScroll();
            carousel.style.transform = `translateX(-${scrollAmount}px)`;
        }
        updateJustifyContent();
        updateButtons();
    });

    // Llamar al empezar
    updateJustifyContent();
    updateButtons();
});