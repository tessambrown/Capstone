
// hero section arrow
document.getElementById('scrollBtn').addEventListener('click', () => {
    document.getElementById('features').scrollIntoView({ behavior: 'smooth' });
});

function scrollToContent() {
    document.getElementById('features').scrollIntoView({ behavior: 'smooth' });
}

// Intro section stars
const section = document.getElementById('features');
const blobs = document.querySelectorAll('.star-blob');
let lastScrollY = window.scrollY;

window.addEventListener('scroll', () => {
    const scrollingDown = window.scrollY > lastScrollY;
    lastScrollY = window.scrollY;

    const rect = section.getBoundingClientRect();
    const inView = rect.top < window.innerHeight && rect.bottom > 0;

    if (inView) {
        blobs.forEach((blob, i) => {
            setTimeout(() => {
                if (scrollingDown) {
                    // fall in from above
                    blob.style.opacity = '1';
                    blob.style.transform = 'translateY(0) rotate(0deg)';
                } else {
                    // rise in from below
                    blob.style.opacity = '1';
                    blob.style.transform = 'translateY(0) rotate(0deg)';
                }
            }, i * 120);
        });
    } else {
        blobs.forEach((blob, i) => {
            setTimeout(() => {
                if (scrollingDown) {
                    // scrolled past going down — rise out above
                    blob.style.opacity = '0';
                    blob.style.transform = 'translateY(-80px) rotate(-10deg)';
                } else {
                    // scrolled back up — fall out below
                    blob.style.opacity = '0';
                    blob.style.transform = 'translateY(80px) rotate(10deg)';
                }
            }, i * 120);
        });
    }
});

// Carousel
const track = document.getElementById('carouselTrack');
const slides = track.querySelectorAll('.carousel-slide');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

let current = 0;
const visible = 3; // how many slides show at once
const total = slides.length;

function updateCarousel() {
  const slideWidth = slides[0].offsetWidth + 24; // width + gap
  track.style.transform = `translateX(-${current * slideWidth}px)`;

  // disable buttons at the ends
  prevBtn.disabled = current === 0;
  nextBtn.disabled = current >= total - visible;
  prevBtn.style.opacity = prevBtn.disabled ? '0.3' : '1';
  nextBtn.style.opacity = nextBtn.disabled ? '0.3' : '1';
}

nextBtn.addEventListener('click', () => {
  if (current < total - visible) {
    current++;
    updateCarousel();
  }
});

prevBtn.addEventListener('click', () => {
  if (current > 0) {
    current--;
    updateCarousel();
  }
});

updateCarousel();

// Auto-cycling slideshows
const slideshows = document.querySelectorAll('.version-slideshow');

slideshows.forEach(slideshow => {
  const images = slideshow.querySelectorAll('img');
  let current = 0;

  setInterval(() => {
    images[current].style.opacity = '0';
    current = (current + 1) % images.length;
    images[current].style.opacity = '1';
  }, 5000); // changes every 2.5 seconds — adjust as needed
});

// Scrollytelling — user customization section
const steps = document.querySelectorAll('.scrolly-step');

const stepObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      // Deactivate all steps
      steps.forEach(s => s.classList.remove('is-active'));
      // Activate the current one
      entry.target.classList.add('is-active');
    }
  });
}, {
  rootMargin: '-40% 0px -40% 0px', // triggers when step is in the middle of the viewport
  threshold: 0
});

steps.forEach(step => stepObserver.observe(step));

let el = document.querySelector('.scrolly-sticky');
while (el) {
  const style = window.getComputedStyle(el);
  if (style.overflow !== 'visible') {
    console.log('clipping ancestor:', el, style.overflow);
  }
  el = el.parentElement;
}