/**
 * Gestion de l'authentification
 * Date : 31 Octobre 2025
 */

// Gestion du formulaire de connexion
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const alert = document.getElementById('alert');
        
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(formData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert.className = 'alert alert-success';
                alert.style.display = 'block';
                alert.textContent = data.message;
                
                setTimeout(function() {
                    window.location.href = data.redirect;
                }, 1000);
            } else {
                alert.className = 'alert alert-error';
                alert.style.display = 'block';
                alert.textContent = data.message;
            }
        } catch (error) {
            console.error('Erreur de connexion:', error);
            alert.className = 'alert alert-error';
            alert.style.display = 'block';
            alert.textContent = 'Une erreur est survenue. Veuillez réessayer.';
        }
    });
}

// Gestion du formulaire d'inscription
if (document.getElementById('registerForm')) {
    document.getElementById('registerForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const alert = document.getElementById('alert');
        
        // Vérifier que les mots de passe correspondent
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm_password');
        
        if (password !== confirmPassword) {
            alert.className = 'alert alert-error';
            alert.style.display = 'block';
            alert.textContent = 'Les mots de passe ne correspondent pas.';
            return;
        }
        
        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(formData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert.className = 'alert alert-success';
                alert.style.display = 'block';
                alert.textContent = data.message;
                
                setTimeout(function() {
                    window.location.href = data.redirect;
                }, 1500);
            } else {
                alert.className = 'alert alert-error';
                alert.style.display = 'block';
                alert.textContent = data.message;
            }
        } catch (error) {
            console.error('Erreur d\'inscription:', error);
            alert.className = 'alert alert-error';
            alert.style.display = 'block';
            alert.textContent = 'Une erreur est survenue. Veuillez réessayer.';
        }
    });
}
