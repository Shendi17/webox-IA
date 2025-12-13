// Script principal
console.log('🚀 Projet chargé avec succès !');

function sayHello() {
    alert('👋 Bonjour depuis WeBox Studio !');
    console.log('Bouton cliqué !');
}

// Animation au chargement
document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ DOM chargé');
    
    const container = document.querySelector('.container');
    container.style.opacity = '0';
    container.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        container.style.transition = 'all 0.5s ease';
        container.style.opacity = '1';
        container.style.transform = 'translateY(0)';
    }, 100);
});