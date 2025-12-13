# Configuration automatique complète de WeBox Multi-IA
# Ce script configure tout automatiquement

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║         🚀 CONFIGURATION AUTOMATIQUE WEBOX MULTI-IA         ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Fonction pour vérifier les droits admin
function Test-Administrator {
    $user = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($user)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Vérifier les droits admin
if (-not (Test-Administrator)) {
    Write-Host "⚠️  Ce script nécessite des droits administrateur pour configurer webox.local" -ForegroundColor Yellow
    Write-Host "🔄 Relancement avec les droits administrateur..." -ForegroundColor Cyan
    
    $scriptPath = $MyInvocation.MyCommand.Path
    Start-Process powershell -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -File `"$scriptPath`""
    exit
}

Write-Host "✅ Droits administrateur confirmés" -ForegroundColor Green
Write-Host ""

# Étape 1 : Configuration du fichier hosts
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host "📝 ÉTAPE 1/4 : Configuration du fichier hosts" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""

$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$hostsEntry = "127.0.0.1    webox.local"

try {
    $hostsContent = Get-Content $hostsPath -Raw
    
    if ($hostsContent -match "webox\.local") {
        Write-Host "⚠️  Une entrée webox.local existe déjà" -ForegroundColor Yellow
        # Supprimer l'ancienne entrée
        $hostsContent = $hostsContent -replace ".*webox\.local.*\r?\n?", ""
        Write-Host "🗑️  Ancienne entrée supprimée" -ForegroundColor Yellow
    }
    
    # Ajouter la nouvelle entrée
    if (-not $hostsContent.EndsWith("`n")) {
        $hostsContent += "`n"
    }
    $hostsContent += "$hostsEntry`n"
    
    Set-Content -Path $hostsPath -Value $hostsContent -NoNewline
    Write-Host "✅ Entrée ajoutée : $hostsEntry" -ForegroundColor Green
    
    # Vider le cache DNS
    Write-Host "🔄 Vidage du cache DNS..." -ForegroundColor Cyan
    ipconfig /flushdns | Out-Null
    Write-Host "✅ Cache DNS vidé" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Erreur lors de la modification du fichier hosts : $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Appuyez sur une touche pour continuer quand même..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

Write-Host ""

# Étape 2 : Vérification du fichier .env
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host "🔑 ÉTAPE 2/4 : Vérification des clés API" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""

$envPath = "c:\Users\Anthony\CascadeProjects\webox\.env"

if (-not (Test-Path $envPath)) {
    Write-Host "⚠️  Fichier .env non trouvé, création..." -ForegroundColor Yellow
    Copy-Item "c:\Users\Anthony\CascadeProjects\webox\.env.example" $envPath
    Write-Host "✅ Fichier .env créé" -ForegroundColor Green
}

$envContent = Get-Content $envPath -Raw

$hasOpenAI = $envContent -match "OPENAI_API_KEY=sk-[a-zA-Z0-9]+"
$hasAnthropic = $envContent -match "ANTHROPIC_API_KEY=sk-ant-[a-zA-Z0-9]+"
$hasGoogle = $envContent -match "GOOGLE_API_KEY=AIza[a-zA-Z0-9]+"

if ($hasOpenAI) { Write-Host "✅ OpenAI configuré" -ForegroundColor Green }
else { Write-Host "⚠️  OpenAI non configuré" -ForegroundColor Yellow }

if ($hasAnthropic) { Write-Host "✅ Anthropic configuré" -ForegroundColor Green }
else { Write-Host "⚠️  Anthropic non configuré" -ForegroundColor Yellow }

if ($hasGoogle) { Write-Host "✅ Google AI configuré" -ForegroundColor Green }
else { Write-Host "⚠️  Google AI non configuré" -ForegroundColor Yellow }

Write-Host ""

if (-not ($hasOpenAI -or $hasAnthropic -or $hasGoogle)) {
    Write-Host "⚠️  ATTENTION : Aucune clé API configurée !" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "L'application va démarrer mais vous devrez configurer vos clés API" -ForegroundColor Yellow
    Write-Host "pour utiliser les fonctionnalités IA." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Voulez-vous configurer vos clés API maintenant ? (O/N)" -ForegroundColor Cyan
    $response = Read-Host
    
    if ($response -eq "O" -or $response -eq "o") {
        notepad $envPath
        Write-Host ""
        Write-Host "Appuyez sur une touche après avoir configuré vos clés API..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
}

Write-Host ""

# Étape 3 : Arrêter les anciennes instances de Streamlit
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host "🛑 ÉTAPE 3/4 : Nettoyage des anciennes instances" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""

# Trouver et tuer les processus Python qui utilisent le port 8501
$processes = Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue
if ($processes) {
    foreach ($proc in $processes) {
        $processId = $proc.OwningProcess
        Write-Host "🛑 Arrêt du processus $processId..." -ForegroundColor Yellow
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
    }
    Write-Host "✅ Anciennes instances arrêtées" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    Write-Host "✅ Aucune instance en cours" -ForegroundColor Green
}

Write-Host ""

# Étape 4 : Lancer l'application
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host "🚀 ÉTAPE 4/4 : Lancement de l'application" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""

Write-Host "📍 L'application sera accessible sur :" -ForegroundColor Green
Write-Host ""
Write-Host "   → http://webox.local:8501" -ForegroundColor Cyan -NoNewline
Write-Host "  (recommandé)" -ForegroundColor Green
Write-Host "   → http://localhost:8501" -ForegroundColor Cyan
Write-Host "   → http://127.0.0.1:8501" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔄 Démarrage de Streamlit..." -ForegroundColor Cyan
Write-Host ""

# Changer de répertoire
Set-Location "c:\Users\Anthony\CascadeProjects\webox"

# Attendre 2 secondes
Start-Sleep -Seconds 2

# Ouvrir le navigateur sur webox.local
Write-Host "🌐 Ouverture du navigateur..." -ForegroundColor Cyan
Start-Process "http://webox.local:8501"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                              ║" -ForegroundColor Green
Write-Host "║              ✅ CONFIGURATION TERMINÉE !                     ║" -ForegroundColor Green
Write-Host "║                                                              ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "💡 L'application va démarrer dans une nouvelle fenêtre..." -ForegroundColor Yellow
Write-Host "💡 Le navigateur s'ouvrira automatiquement sur webox.local" -ForegroundColor Yellow
Write-Host ""
Write-Host "Appuyez sur une touche pour lancer Streamlit..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Lancer Streamlit
streamlit run app.py --server.headless true
