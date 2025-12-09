document.addEventListener('DOMContentLoaded', () => {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) e.target.classList.add('visible');
    });
  }, {threshold: 0.20});

  document.querySelectorAll('.appear').forEach(el => observer.observe(el));
});