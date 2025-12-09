const heroContent = document.getElementById('hero-content');
window.addEventListener('scroll', () => {
    let scrollY = window.scrollY;

    // Movimiento hacia abajo (parallax)
    let translateY = scrollY * 0.6;

    // Escala (más pequeño mientras baja)
    let scale = Math.max(1 - scrollY / 1000, 0.9); // mínimo 70% tamaño ---1000, 0.7

    // Opacidad (se va escondiendo)
    let opacity = Math.max(1 - scrollY / 999, 0);

    heroContent.style.transform = `translateY(${translateY}px) scale(${scale})`;
    heroContent.style.opacity = opacity;
});
