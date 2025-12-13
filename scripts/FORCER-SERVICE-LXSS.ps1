# Script pour forcer le service LxssManager à rester actif
# Date : 1er Novembre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     FORCER LE SERVICE LXSSMANAGER                              " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    exit
}

Write-Host "Diagnostic du problème..." -ForegroundColor Cyan
Write-Host ""

# Vérifier le service
$service = Get-Service -Name LxssManager -ErrorAction SilentlyContinue

if ($service) {
    Write-Host "Service LxssManager trouvé" -ForegroundColor Green
    Write-Host "  État actuel : $($service.Status)" -ForegroundColor White
    Write-Host "  Type de démarrage : $($service.StartType)" -ForegroundColor White
} else {
    Write-Host "❌ Service LxssManager non trouvé !" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Tentative 1 : Modification via registre..." -ForegroundColor Cyan

# Modifier directement le registre
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\LxssManager"
try {
    # 2 = Automatic, 3 = Manual, 4 = Disabled
    Set-ItemProperty -Path $regPath -Name "Start" -Value 3 -Force
    Write-Host "✅ Registre modifié (Manuel)" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur : $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Tentative 2 : Modification via sc.exe..." -ForegroundColor Cyan

# Utiliser sc.exe
$scOutput = sc.exe config LxssManager start= demand 2>&1
Write-Host $scOutput

Write-Host ""
Write-Host "Tentative 3 : Démarrage du service..." -ForegroundColor Cyan

# Démarrer via sc.exe
$startOutput = sc.exe start LxssManager 2>&1
Write-Host $startOutput

Start-Sleep -Seconds 2

# Vérifier
$service = Get-Service -Name LxssManager
Write-Host ""
Write-Host "État final : $($service.Status)" -ForegroundColor $(if ($service.Status -eq "Running") { "Green" } else { "Red" })

Write-Host ""
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""

if ($service.Status -eq "Running") {
    Write-Host "✅ SERVICE DÉMARRÉ !" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT : Installez Ubuntu IMMÉDIATEMENT avant que le service ne se désactive :" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Ouvrez le Microsoft Store et installez Ubuntu MAINTENANT !" -ForegroundColor Cyan
    Write-Host ""
    
    $openStore = Read-Host "Ouvrir le Microsoft Store ? (O/N)"
    if ($openStore -eq "O" -or $openStore -eq "o") {
        Start-Process "ms-windows-store://pdp/?ProductId=9PN20MSR04DW"
        Write-Host ""
        Write-Host "✅ Microsoft Store ouvert" -ForegroundColor Green
        Write-Host ""
        Write-Host "Installez Ubuntu RAPIDEMENT puis lancez-le immédiatement !" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ LE SERVICE NE PEUT PAS DÉMARRER" -ForegroundColor Red
    Write-Host ""
    Write-Host "Causes possibles :" -ForegroundColor Yellow
    Write-Host "  1. Antivirus ou logiciel de sécurité bloque le service" -ForegroundColor White
    Write-Host "  2. Politique de groupe d'entreprise" -ForegroundColor White
    Write-Host "  3. Service corrompu" -ForegroundColor White
    Write-Host ""
    Write-Host "SOLUTION : Utiliser SQLite au lieu de PostgreSQL Docker" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "SQLite ne nécessite pas WSL/Docker et fonctionne immédiatement." -ForegroundColor White
    Write-Host "Vous pourrez migrer vers PostgreSQL plus tard si nécessaire." -ForegroundColor White
    Write-Host ""
    
    $useSqlite = Read-Host "Voulez-vous configurer SQLite maintenant ? (O/N)"
    if ($useSqlite -eq "O" -or $useSqlite -eq "o") {
        Write-Host ""
        Write-Host "Configuration SQLite..." -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Exécutez ce script :" -ForegroundColor Yellow
        Write-Host "  cd C:\Users\Anthony\CascadeProjects\webox" -ForegroundColor White
        Write-Host "  python scripts\configurer-sqlite.py" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
