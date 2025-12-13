# Configuration automatique complete de WeBox Multi-IA
# Ce script configure tout automatiquement

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "         CONFIGURATION AUTOMATIQUE WEBOX MULTI-IA              " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Fonction pour verifier les droits admin
function Test-Administrator {
    $user = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($user)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Verifier les droits admin
if (-not (Test-Administrator)) {
    Write-Host "ATTENTION: Ce script necessite des droits administrateur" -ForegroundColor Yellow
    Write-Host "Relancement avec les droits administrateur..." -ForegroundColor Cyan
    
    $scriptPath = $MyInvocation.MyCommand.Path
    Start-Process powershell -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -File `"$scriptPath`""
    exit
}

Write-Host "OK - Droits administrateur confirmes" -ForegroundColor Green
Write-Host ""

# Etape 1 : Configuration du fichier hosts
Write-Host "================================================================" -ForegroundColor Gray
Write-Host "ETAPE 1/4 : Configuration du fichier hosts" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""

$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$hostsEntry = "127.0.0.1    webox.local"

try {
    $hostsContent = Get-Content $hostsPath -Raw
    
    if ($hostsContent -match "webox\.local") {
        Write-Host "Une entree webox.local existe deja - suppression..." -ForegroundColor Yellow
        $hostsContent = $hostsContent -replace ".*webox\.local.*\r?\n?", ""
        Write-Host "Ancienne entree supprimee" -ForegroundColor Yellow
    }
    
    # Ajouter la nouvelle entree
    if (-not $hostsContent.EndsWith("`n")) {
        $hostsContent += "`n"
    }
    $hostsContent += "$hostsEntry`n"
    
    Set-Content -Path $hostsPath -Value $hostsContent -NoNewline
    Write-Host "OK - Entree ajoutee : $hostsEntry" -ForegroundColor Green
    
    # Vider le cache DNS
    Write-Host "Vidage du cache DNS..." -ForegroundColor Cyan
    ipconfig /flushdns | Out-Null
    Write-Host "OK - Cache DNS vide" -ForegroundColor Green
    
} catch {
    Write-Host "ERREUR lors de la modification du fichier hosts" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host ""

# Etape 2 : Verification du fichier .env
Write-Host "================================================================" -ForegroundColor Gray
Write-Host "ETAPE 2/4 : Verification des cles API" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""

$envPath = "c:\Users\Anthony\CascadeProjects\webox\.env"

if (-not (Test-Path $envPath)) {
    Write-Host "Fichier .env non trouve - creation..." -ForegroundColor Yellow
    Copy-Item "c:\Users\Anthony\CascadeProjects\webox\.env.example" $envPath
    Write-Host "OK - Fichier .env cree" -ForegroundColor Green
}

$envContent = Get-Content $envPath -Raw

$hasOpenAI = $envContent -match "OPENAI_API_KEY=sk-[a-zA-Z0-9]+"
$hasAnthropic = $envContent -match "ANTHROPIC_API_KEY=sk-ant-[a-zA-Z0-9]+"
$hasGoogle = $envContent -match "GOOGLE_API_KEY=AIza[a-zA-Z0-9]+"

if ($hasOpenAI) { Write-Host "OK - OpenAI configure" -ForegroundColor Green }
else { Write-Host "ATTENTION - OpenAI non configure" -ForegroundColor Yellow }

if ($hasAnthropic) { Write-Host "OK - Anthropic configure" -ForegroundColor Green }
else { Write-Host "ATTENTION - Anthropic non configure" -ForegroundColor Yellow }

if ($hasGoogle) { Write-Host "OK - Google AI configure" -ForegroundColor Green }
else { Write-Host "ATTENTION - Google AI non configure" -ForegroundColor Yellow }

Write-Host ""

if (-not ($hasOpenAI -or $hasAnthropic -or $hasGoogle)) {
    Write-Host "ATTENTION : Aucune cle API configuree !" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Voulez-vous configurer vos cles API maintenant ? (O/N)" -ForegroundColor Cyan
    $response = Read-Host
    
    if ($response -eq "O" -or $response -eq "o") {
        notepad $envPath
        Write-Host ""
        Write-Host "Appuyez sur une touche apres avoir configure vos cles API..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
}

Write-Host ""

# Etape 3 : Arreter les anciennes instances
Write-Host "================================================================" -ForegroundColor Gray
Write-Host "ETAPE 3/4 : Nettoyage des anciennes instances" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""

$processes = Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue
if ($processes) {
    foreach ($proc in $processes) {
        $processId = $proc.OwningProcess
        Write-Host "Arret du processus $processId..." -ForegroundColor Yellow
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
    }
    Write-Host "OK - Anciennes instances arretees" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    Write-Host "OK - Aucune instance en cours" -ForegroundColor Green
}

Write-Host ""

# Etape 4 : Lancer l'application
Write-Host "================================================================" -ForegroundColor Gray
Write-Host "ETAPE 4/4 : Lancement de l'application" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""

Write-Host "L'application sera accessible sur :" -ForegroundColor Green
Write-Host ""
Write-Host "   -> http://webox.local:8501 (recommande)" -ForegroundColor Cyan
Write-Host "   -> http://localhost:8501" -ForegroundColor Cyan
Write-Host "   -> http://127.0.0.1:8501" -ForegroundColor Cyan
Write-Host ""

Write-Host "Demarrage de Streamlit..." -ForegroundColor Cyan
Write-Host ""

# Changer de repertoire
Set-Location "c:\Users\Anthony\CascadeProjects\webox"

# Attendre 2 secondes
Start-Sleep -Seconds 2

# Ouvrir le navigateur sur webox.local
Write-Host "Ouverture du navigateur..." -ForegroundColor Cyan
Start-Process "http://webox.local:8501"

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "              CONFIGURATION TERMINEE !                          " -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "L'application va demarrer maintenant..." -ForegroundColor Yellow
Write-Host "Le navigateur s'est ouvert sur webox.local" -ForegroundColor Yellow
Write-Host ""
Write-Host "Appuyez sur une touche pour lancer Streamlit..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Lancer Streamlit
streamlit run app.py --server.headless true
