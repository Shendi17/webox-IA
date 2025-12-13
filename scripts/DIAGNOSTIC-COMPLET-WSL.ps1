# Diagnostic complet et réparation WSL
# Date : 1er Novembre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     DIAGNOSTIC COMPLET WSL - RÉPARATION FORCÉE                 " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    exit
}

Write-Host "PHASE 1 : DIAGNOSTIC APPROFONDI" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Gray
Write-Host ""

# 1. Vérifier les dépendances du service
Write-Host "1. Dépendances du service LxssManager..." -ForegroundColor Yellow
$dependencies = sc.exe qc LxssManager | Select-String "DEPENDENCIES"
Write-Host "   $dependencies" -ForegroundColor White

# 2. Vérifier l'état détaillé
Write-Host ""
Write-Host "2. État détaillé du service..." -ForegroundColor Yellow
$serviceDetails = sc.exe query LxssManager
Write-Host $serviceDetails

# 3. Vérifier les services liés
Write-Host ""
Write-Host "3. Services liés..." -ForegroundColor Yellow
$services = @("LxssManager", "vmcompute", "HvHost", "vmsmp")
foreach ($svc in $services) {
    $s = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($s) {
        Write-Host "   $svc : $($s.Status) - $($s.StartType)" -ForegroundColor White
    } else {
        Write-Host "   $svc : Non trouvé" -ForegroundColor Red
    }
}

# 4. Vérifier les pilotes
Write-Host ""
Write-Host "4. Pilotes de virtualisation..." -ForegroundColor Yellow
$drivers = @("wslcore", "vmmem", "hvservice")
foreach ($drv in $drivers) {
    $d = Get-WindowsDriver -Online | Where-Object { $_.Driver -like "*$drv*" } -ErrorAction SilentlyContinue
    if ($d) {
        Write-Host "   $drv : Installé" -ForegroundColor Green
    } else {
        Write-Host "   $drv : Non trouvé" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "PHASE 2 : RÉPARATION FORCÉE" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Gray
Write-Host ""

# Arrêter tous les services
Write-Host "Arrêt de tous les services WSL..." -ForegroundColor Yellow
Stop-Service -Name LxssManager -Force -ErrorAction SilentlyContinue
Stop-Service -Name vmcompute -Force -ErrorAction SilentlyContinue
Stop-Service -Name HvHost -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Configurer via registre avec tous les paramètres
Write-Host "Configuration du registre..." -ForegroundColor Yellow
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\LxssManager"

# Start = 3 (Manuel)
Set-ItemProperty -Path $regPath -Name "Start" -Value 3 -Force -ErrorAction SilentlyContinue

# Type = 32 (Service Win32 propre)
Set-ItemProperty -Path $regPath -Name "Type" -Value 32 -Force -ErrorAction SilentlyContinue

# ErrorControl = 1 (Normal)
Set-ItemProperty -Path $regPath -Name "ErrorControl" -Value 1 -Force -ErrorAction SilentlyContinue

Write-Host "✅ Registre configuré" -ForegroundColor Green

# Configurer via sc.exe
Write-Host ""
Write-Host "Configuration via sc.exe..." -ForegroundColor Yellow
sc.exe config LxssManager start= demand
sc.exe config LxssManager type= own
sc.exe config LxssManager error= normal

# Configurer les dépendances
Write-Host ""
Write-Host "Configuration des services dépendants..." -ForegroundColor Yellow
sc.exe config vmcompute start= demand
sc.exe config HvHost start= demand

# Démarrer dans l'ordre
Write-Host ""
Write-Host "Démarrage des services dans l'ordre..." -ForegroundColor Yellow

Write-Host "  1. HvHost..." -ForegroundColor White
sc.exe start HvHost 2>$null
Start-Sleep -Seconds 1

Write-Host "  2. vmcompute..." -ForegroundColor White
sc.exe start vmcompute 2>$null
Start-Sleep -Seconds 1

Write-Host "  3. LxssManager..." -ForegroundColor White
$startResult = sc.exe start LxssManager 2>&1
Write-Host "     $startResult" -ForegroundColor Gray
Start-Sleep -Seconds 2

# Vérification finale
Write-Host ""
Write-Host "PHASE 3 : VÉRIFICATION" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Gray
Write-Host ""

$lxss = Get-Service -Name LxssManager
$vmcomp = Get-Service -Name vmcompute

Write-Host "État des services :" -ForegroundColor Yellow
Write-Host "  LxssManager : $($lxss.Status)" -ForegroundColor $(if ($lxss.Status -eq "Running") { "Green" } else { "Red" })
Write-Host "  vmcompute   : $($vmcomp.Status)" -ForegroundColor $(if ($vmcomp.Status -eq "Running") { "Green" } else { "Red" })

Write-Host ""

if ($lxss.Status -eq "Running") {
    Write-Host "✅ SERVICE LXSSMANAGER DÉMARRÉ !" -ForegroundColor Green
    Write-Host ""
    
    # Test WSL
    Write-Host "Test de WSL..." -ForegroundColor Yellow
    $wslTest = wsl --status 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ WSL fonctionne !" -ForegroundColor Green
        Write-Host ""
        Write-Host $wslTest
        Write-Host ""
        Write-Host "SUCCÈS ! Vous pouvez maintenant :" -ForegroundColor Cyan
        Write-Host "  1. Installer Ubuntu via Microsoft Store" -ForegroundColor White
        Write-Host "  2. Ou exécuter : wsl --install -d Ubuntu" -ForegroundColor White
        Write-Host ""
        
        $install = Read-Host "Voulez-vous installer Ubuntu maintenant ? (O/N)"
        if ($install -eq "O" -or $install -eq "o") {
            Write-Host ""
            Write-Host "Installation d'Ubuntu..." -ForegroundColor Cyan
            wsl --install -d Ubuntu --no-launch
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Ubuntu installé !" -ForegroundColor Green
                Write-Host ""
                Write-Host "Lancez Docker Desktop maintenant !" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "⚠️  WSL ne répond pas encore" -ForegroundColor Yellow
        Write-Host "Essayez d'installer Ubuntu via Microsoft Store" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ LE SERVICE NE DÉMARRE TOUJOURS PAS" -ForegroundColor Red
    Write-Host ""
    Write-Host "Dernière tentative : Vérifier les logs d'événements..." -ForegroundColor Yellow
    Write-Host ""
    
    # Afficher les dernières erreurs du service
    $events = Get-EventLog -LogName System -Source "Service Control Manager" -Newest 5 -ErrorAction SilentlyContinue | 
              Where-Object { $_.Message -like "*LxssManager*" }
    
    if ($events) {
        Write-Host "Erreurs récentes :" -ForegroundColor Red
        foreach ($event in $events) {
            Write-Host "  - $($event.TimeGenerated) : $($event.Message)" -ForegroundColor White
        }
    }
    
    Write-Host ""
    Write-Host "Le service est probablement bloqué par :" -ForegroundColor Yellow
    Write-Host "  1. Un antivirus (Kaspersky, McAfee, Norton, etc.)" -ForegroundColor White
    Write-Host "  2. Une politique de groupe d'entreprise" -ForegroundColor White
    Write-Host "  3. Un pilote manquant ou corrompu" -ForegroundColor White
    Write-Host ""
    Write-Host "Vérifiez votre antivirus et désactivez-le temporairement" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
