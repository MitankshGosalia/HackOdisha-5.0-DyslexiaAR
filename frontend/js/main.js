// Basic interactivity: mobile nav toggle, scroll reveals, parallax hero, simple carousel

(function () {
  const navToggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.nav');
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear().toString();

  if (navToggle && nav) {
    navToggle.addEventListener('click', () => nav.classList.toggle('open'));
  }

  // Reveal on scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) e.target.classList.add('visible');
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

  // Parallax effect for hero overlay
  const parallax = document.querySelector('.parallax');
  if (parallax) {
    window.addEventListener('scroll', () => {
      const y = window.scrollY * 0.2;
      parallax.style.transform = `translateY(${y}px)`;
    });
  }

  // Simple carousel
  const track = document.getElementById('carousel-track');
  const prev = document.getElementById('carousel-prev');
  const next = document.getElementById('carousel-next');
  if (track && prev && next) {
    const scrollAmount = () => track.clientWidth * 0.7;
    prev.addEventListener('click', () => track.scrollBy({ left: -scrollAmount(), behavior: 'smooth' }));
    next.addEventListener('click', () => track.scrollBy({ left: scrollAmount(), behavior: 'smooth' }));
  }
})();


