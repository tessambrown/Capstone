
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