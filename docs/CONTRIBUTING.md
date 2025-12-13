# 🤝 Guide de Contribution - WeBox Multi-IA

Merci de votre intérêt pour contribuer à WeBox Multi-IA ! Ce document vous guidera à travers le processus de contribution.

---

## 📋 Table des Matières

1. [Code de Conduite](#code-de-conduite)
2. [Comment Contribuer](#comment-contribuer)
3. [Processus de Développement](#processus-de-développement)
4. [Standards de Code](#standards-de-code)
5. [Soumettre une Pull Request](#soumettre-une-pull-request)
6. [Signaler un Bug](#signaler-un-bug)
7. [Proposer une Fonctionnalité](#proposer-une-fonctionnalité)

---

## 📜 Code de Conduite

En participant à ce projet, vous acceptez de respecter notre code de conduite :

- **Respect** : Traitez tous les contributeurs avec respect
- **Collaboration** : Soyez ouvert aux feedbacks et aux suggestions
- **Inclusivité** : Accueillez les contributeurs de tous niveaux
- **Professionnalisme** : Maintenez un environnement professionnel

---

## 🚀 Comment Contribuer

Il existe plusieurs façons de contribuer :

### 1. Signaler des Bugs
Trouvé un bug ? Créez une issue avec :
- Description claire du problème
- Étapes pour reproduire
- Comportement attendu vs actuel
- Captures d'écran si applicable
- Environnement (OS, version Python, etc.)

### 2. Proposer des Fonctionnalités
Une idée d'amélioration ? Créez une issue avec :
- Description de la fonctionnalité
- Cas d'usage
- Bénéfices attendus
- Exemples ou maquettes si possible

### 3. Améliorer la Documentation
- Corriger des fautes
- Ajouter des exemples
- Clarifier des instructions
- Traduire en d'autres langues

### 4. Contribuer au Code
- Corriger des bugs
- Implémenter de nouvelles fonctionnalités
- Optimiser les performances
- Améliorer l'UI/UX

---

## 🔧 Processus de Développement

### 1. Fork et Clone

```bash
# Fork le repository sur GitHub
# Puis clonez votre fork
git clone https://github.com/VOTRE-USERNAME/webox.git
cd webox
```

### 2. Créer une Branche

```bash
# Créez une branche pour votre contribution
git checkout -b feature/ma-nouvelle-fonctionnalite
# ou
git checkout -b fix/correction-bug
```

### 3. Installer les Dépendances

```bash
# Créez un environnement virtuel
python -m venv venv

# Activez-le (Windows)
.\venv\Scripts\activate

# Installez les dépendances
pip install -r requirements.txt
```

### 4. Développer

- Écrivez votre code
- Testez localement
- Suivez les standards de code (voir ci-dessous)

### 5. Commit

```bash
# Ajoutez vos changements
git add .

# Commit avec un message descriptif
git commit -m "feat: ajout de la fonctionnalité X"
# ou
git commit -m "fix: correction du bug Y"
```

**Convention de nommage des commits :**
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage, style
- `refactor:` Refactoring de code
- `test:` Ajout de tests
- `chore:` Tâches de maintenance

### 6. Push et Pull Request

```bash
# Push vers votre fork
git push origin feature/ma-nouvelle-fonctionnalite

# Créez une Pull Request sur GitHub
```

---

## 📏 Standards de Code

### Python

**Style :**
- Suivez [PEP 8](https://pep8.org/)
- Utilisez des noms de variables descriptifs
- Commentez le code complexe
- Docstrings pour toutes les fonctions/classes

**Exemple :**
```python
def calculate_response_time(start_time: float, end_time: float) -> float:
    """
    Calcule le temps de réponse en secondes.
    
    Args:
        start_time: Timestamp de début
        end_time: Timestamp de fin
        
    Returns:
        Temps de réponse en secondes
    """
    return end_time - start_time
```

**Formatage :**
```bash
# Utilisez black pour le formatage
pip install black
black .

# Vérifiez avec flake8
pip install flake8
flake8 .
```

### Structure des Fichiers

```
webox/
├── app.py              # Application principale
├── config.py           # Configuration
├── ai_providers.py     # Gestionnaires d'IA
├── utils.py            # Utilitaires
├── requirements.txt    # Dépendances
├── README.md          # Documentation
└── tests/             # Tests (à créer)
    └── test_*.py
```

---

## 🔍 Tests

Avant de soumettre votre PR :

### Tests Manuels
1. Lancez l'application : `streamlit run app.py`
2. Testez votre fonctionnalité
3. Vérifiez qu'aucune régression n'est introduite

### Tests Automatisés (à venir)
```bash
# Exécutez les tests
pytest

# Avec couverture
pytest --cov=.
```

---

## 📝 Soumettre une Pull Request

### Checklist avant soumission :

- [ ] Le code suit les standards PEP 8
- [ ] Les fonctions sont documentées
- [ ] Le code a été testé localement
- [ ] Aucune régression introduite
- [ ] Les fichiers inutiles sont exclus (.env, __pycache__, etc.)
- [ ] Le commit message est descriptif
- [ ] La PR a une description claire

### Template de Pull Request :

```markdown
## Description
[Décrivez vos changements]

## Type de changement
- [ ] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Breaking change
- [ ] Documentation

## Comment tester
[Étapes pour tester vos changements]

## Checklist
- [ ] Code testé localement
- [ ] Documentation mise à jour
- [ ] Pas de warnings
- [ ] Suit les standards de code

## Screenshots (si applicable)
[Ajoutez des captures d'écran]
```

---

## 🐛 Signaler un Bug

### Template d'Issue pour Bug :

```markdown
## Description du Bug
[Description claire et concise]

## Étapes pour Reproduire
1. Allez sur '...'
2. Cliquez sur '...'
3. Faites défiler jusqu'à '...'
4. Voir l'erreur

## Comportement Attendu
[Ce qui devrait se passer]

## Comportement Actuel
[Ce qui se passe réellement]

## Screenshots
[Si applicable]

## Environnement
- OS: [ex. Windows 11]
- Python: [ex. 3.11]
- Version: [ex. 1.0.0]

## Logs d'Erreur
```
[Collez les logs ici]
```

## Informations Additionnelles
[Tout autre contexte utile]
```

---

## 💡 Proposer une Fonctionnalité

### Template d'Issue pour Fonctionnalité :

```markdown
## Fonctionnalité Proposée
[Description claire de la fonctionnalité]

## Problème Résolu
[Quel problème cette fonctionnalité résout-elle ?]

## Solution Proposée
[Comment implémenteriez-vous cette fonctionnalité ?]

## Alternatives Considérées
[Autres approches possibles]

## Cas d'Usage
[Exemples concrets d'utilisation]

## Bénéfices
- [Bénéfice 1]
- [Bénéfice 2]

## Mockups/Exemples
[Si applicable]
```

---

## 🎯 Domaines de Contribution

### Priorités Actuelles

**Haute Priorité :**
- [ ] Tests unitaires et d'intégration
- [ ] Export de conversations
- [ ] Amélioration de la gestion d'erreurs
- [ ] Optimisation des performances

**Moyenne Priorité :**
- [ ] Support de nouveaux modèles d'IA
- [ ] Thèmes personnalisables
- [ ] Statistiques d'utilisation
- [ ] Mode hors-ligne

**Basse Priorité :**
- [ ] Intégrations tierces
- [ ] Plugins
- [ ] API REST
- [ ] Mode collaboratif

### Compétences Recherchées

- **Python** : Backend, optimisation
- **Streamlit** : UI/UX, composants
- **IA/ML** : Intégration de nouveaux modèles
- **DevOps** : CI/CD, déploiement
- **Documentation** : Guides, tutoriels
- **Design** : UI/UX, maquettes

---

## 📞 Questions ?

- **Issues** : Pour les bugs et fonctionnalités
- **Discussions** : Pour les questions générales
- **Email** : [votre-email]

---

## 🙏 Remerciements

Merci à tous les contributeurs qui aident à améliorer WeBox Multi-IA !

### Contributeurs Principaux
- [Votre nom] - Créateur et mainteneur principal

### Contributeurs
[Liste mise à jour automatiquement]

---

## 📄 Licence

En contribuant, vous acceptez que vos contributions soient sous licence MIT.

---

**Bonne contribution ! 🚀**
