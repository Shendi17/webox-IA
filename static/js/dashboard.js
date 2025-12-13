// Dashboard JavaScript

console.log('Dashboard.js chargé');

// Débogage des clics sur les cartes
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM chargé');
    
    // Seulement les cartes qui sont des liens
    const cardLinks = document.querySelectorAll('a.dashboard-card');
    console.log('Nombre de cartes-liens trouvées:', cardLinks.length);
    
    cardLinks.forEach((card, index) => {
        console.log(`Carte-lien ${index}:`, card.href);
        
        card.addEventListener('click', function(e) {
            console.log('Clic détecté sur carte-lien:', this.href);
            // Ne pas empêcher le comportement par défaut
            // e.preventDefault();
        });
    });
});

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Animation au scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.dashboard-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all 0.5s ease';
    card.style.pointerEvents = 'auto'; // S'assurer que les clics fonctionnent
    observer.observe(card);
});

// Toggle sidebar sur mobile
const createMobileToggle = () => {
    if (window.innerWidth <= 768) {
        const sidebar = document.querySelector('.sidebar');
        const toggle = document.createElement('button');
        toggle.className = 'mobile-toggle';
        toggle.innerHTML = '☰';
        toggle.style.cssText = `
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: 1001;
            background: #1a1a2e;
            color: #ffd700;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-size: 1.5rem;
            cursor: pointer;
        `;
        
        toggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
        
        document.body.appendChild(toggle);
    }
};

// Initialiser au chargement
window.addEventListener('load', createMobileToggle);
window.addEventListener('resize', createMobileToggle);
