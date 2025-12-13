// Fonctions utilitaires
export function formatDate(date) {
    return new Date(date).toLocaleDateString('fr-FR');
}

export function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
