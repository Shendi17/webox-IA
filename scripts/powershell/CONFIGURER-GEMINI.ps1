# ============================================
# CONFIGURATION RAPIDE GEMINI PRO (GRATUIT)
# ============================================
# Ce script configure Gemini Pro pour tester
# l'IA gratuitement sans carte bancaire
# ============================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  CONFIGURATION GEMINI PRO (GRATUIT)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Gemini Pro est le modèle IA de Google, GRATUIT jusqu'à 60 req/min !" -ForegroundColor Green
Write-Host ""
Write-Host "Étapes :" -ForegroundColor Yellow
Write-Host "1. Va sur : https://makersuite.google.com/app/apikey" -ForegroundColor White
Write-Host "2. Connecte-toi avec ton compte Google" -ForegroundColor White
Write-Host "3. Clique sur 'Get API Key' ou 'Create API Key'" -ForegroundColor White
Write-Host "4. Copie la clé (commence par AIza...)" -ForegroundColor White
Write-Host ""

# Ouvrir le navigateur
Write-Host "Veux-tu ouvrir le site dans ton navigateur ? (O/N)" -ForegroundColor Yellow
$openBrowser = Read-Host

if ($openBrowser -eq "O" -or $openBrowser -eq "o") {
    Start-Process "https://makersuite.google.com/app/apikey"
    Write-Host "✓ Navigateur ouvert !" -ForegroundColor Green
    Write-Host ""
}

# Demander la clé
Write-Host "Colle ta clé API Gemini Pro ici (ou appuie sur Entrée pour annuler) :" -ForegroundColor Yellow
$apiKey = Read-Host

if ([string]::IsNullOrWhiteSpace($apiKey)) {
    Write-Host ""
    Write-Host "✗ Annulé. Aucune clé fournie." -ForegroundColor Red
    Write-Host ""
    Write-Host "Appuie sur une touche pour fermer..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 0
}

# Vérifier le format
if (-not $apiKey.StartsWith("AIza")) {
    Write-Host ""
    Write-Host "⚠️  La clé ne semble pas valide (devrait commencer par 'AIza')" -ForegroundColor Yellow
    Write-Host "Veux-tu continuer quand même ? (O/N)" -ForegroundColor Yellow
    $continue = Read-Host
    
    if ($continue -ne "O" -and $continue -ne "o") {
        Write-Host "✗ Annulé." -ForegroundColor Red
        Write-Host ""
        Write-Host "Appuie sur une touche pour fermer..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 0
    }
}

Write-Host ""
Write-Host "Configuration du fichier .env..." -ForegroundColor Yellow

# Lire le fichier .env
$envPath = ".env"
if (-not (Test-Path $envPath)) {
    Write-Host "✗ Fichier .env introuvable !" -ForegroundColor Red
    Write-Host "  Copie .env.example vers .env d'abord" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Appuie sur une touche pour fermer..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

try {
    $envContent = Get-Content $envPath -Raw -Encoding UTF8
    
    # Vérifier si GOOGLE_API_KEY existe déjà
    if ($envContent -match "GOOGLE_API_KEY=.+") {
        Write-Host "⚠️  Une clé Google existe déjà dans .env" -ForegroundColor Yellow
        Write-Host "Veux-tu la remplacer ? (O/N)" -ForegroundColor Yellow
        $replace = Read-Host
        
        if ($replace -ne "O" -and $replace -ne "o") {
            Write-Host "✗ Annulé. Clé existante conservée." -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Appuie sur une touche pour fermer..." -ForegroundColor Yellow
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 0
        }
        
        # Remplacer
        $envContent = $envContent -replace "GOOGLE_API_KEY=.*", "GOOGLE_API_KEY=$apiKey"
    } else {
        # Ajouter
        if ($envContent -match "GOOGLE_API_KEY=\s*$") {
            $envContent = $envContent -replace "GOOGLE_API_KEY=\s*$", "GOOGLE_API_KEY=$apiKey"
        } else {
            $envContent += "`nGOOGLE_API_KEY=$apiKey`n"
        }
    }
    
    # Sauvegarder
    Set-Content -Path $envPath -Value $envContent -Encoding UTF8 -NoNewline
    
    Write-Host "✓ Clé Gemini Pro configurée avec succès !" -ForegroundColor Green
    Write-Host ""
    
    # Proposer de redémarrer le serveur
    Write-Host "Veux-tu redémarrer le serveur maintenant ? (O/N)" -ForegroundColor Yellow
    $restart = Read-Host
    
    if ($restart -eq "O" -or $restart -eq "o") {
        Write-Host ""
        Write-Host "Démarrage du serveur..." -ForegroundColor Yellow
        Write-Host ""
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python main.py"
        Write-Host "✓ Serveur démarré dans une nouvelle fenêtre !" -ForegroundColor Green
        Write-Host ""
        Write-Host "Attends 5 secondes puis teste sur :" -ForegroundColor Cyan
        Write-Host "http://localhost:8000/projects/2/editor" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "Pour démarrer le serveur manuellement :" -ForegroundColor Yellow
        Write-Host "python main.py" -ForegroundColor White
    }
    
} catch {
    Write-Host "✗ Erreur lors de la configuration : $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Appuie sur une touche pour fermer..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
