document.addEventListener("DOMContentLoaded", function () {
    let images = document.querySelectorAll(".carousel img");
    let currentIndex = 0;

    function changeImage() {
        images[currentIndex].style.opacity = "0"; // Oculta la imagen actual
        currentIndex = (currentIndex + 1) % images.length; // Avanza al siguiente índice
        images[currentIndex].style.opacity = "1"; // Muestra la nueva imagen
    }

    setInterval(changeImage, 4000); // Cambia la imagen cada 4 segundos
});