# Diagnostic ultra-détaillé du problème WSL
# Date : 1er Novembre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     DIAGNOSTIC ULTRA-DÉTAILLÉ WSL                              " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    exit
}

$logFile = "C:\Users\Anthony\CascadeProjects\webox\diagnostic-wsl.txt"
$output = @()

function Add-Log {
    param([string]$Message)
    Write-Host $Message
    $output += $Message
}

Add-Log ""
Add-Log "DIAGNOSTIC WSL - $(Get-Date)"
Add-Log "=" * 80
Add-Log ""

# 1. INFORMATIONS SYSTÈME
Add-Log "1. INFORMATIONS SYSTÈME"
Add-Log "-" * 80

$os = Get-CimInstance -ClassName Win32_OperatingSystem
Add-Log "OS : $($os.Caption)"
Add-Log "Version : $($os.Version)"
Add-Log "Build : $($os.BuildNumber)"
Add-Log "Architecture : $($os.OSArchitecture)"
Add-Log "Langue : $($os.OSLanguage)"
Add-Log ""

# 2. VIRTUALISATION
Add-Log "2. VIRTUALISATION"
Add-Log "-" * 80

$cpu = Get-CimInstance -ClassName Win32_Processor
Add-Log "CPU : $($cpu.Name)"
Add-Log "Virtualisation activée : $($cpu.VirtualizationFirmwareEnabled)"
Add-Log "Hyper-V présent : $((Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All).State)"
Add-Log ""

# 3. SERVICES DÉTAILLÉS
Add-Log "3. SERVICES WSL ET DÉPENDANCES"
Add-Log "-" * 80

$services = @("LxssManager", "vmcompute", "HvHost", "vmsmp", "RPCSS")
foreach ($svcName in $services) {
    $svc = Get-Service -Name $svcName -ErrorAction SilentlyContinue
    if ($svc) {
        Add-Log ""
        Add-Log "Service : $svcName"
        Add-Log "  État : $($svc.Status)"
        Add-Log "  Type démarrage : $($svc.StartType)"
        Add-Log "  Peut s'arrêter : $($svc.CanStop)"
        Add-Log "  Peut se mettre en pause : $($svc.CanPauseAndContinue)"
        
        # Détails via sc.exe
        $scDetails = sc.exe qc $svcName
        Add-Log "  Détails sc.exe :"
        foreach ($line in $scDetails) {
            Add-Log "    $line"
        }
    } else {
        Add-Log "Service $svcName : NON TROUVÉ"
    }
}
Add-Log ""

# 4. REGISTRE
Add-Log "4. CONFIGURATION REGISTRE"
Add-Log "-" * 80

$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\LxssManager"
if (Test-Path $regPath) {
    $regKeys = Get-ItemProperty -Path $regPath
    Add-Log "Clés de registre LxssManager :"
    Add-Log "  Start : $($regKeys.Start) (2=Auto, 3=Manuel, 4=Désactivé)"
    Add-Log "  Type : $($regKeys.Type)"
    Add-Log "  ErrorControl : $($regKeys.ErrorControl)"
    Add-Log "  ImagePath : $($regKeys.ImagePath)"
    
    if ($regKeys.PSObject.Properties.Name -contains "DependOnService") {
        Add-Log "  DependOnService : $($regKeys.DependOnService)"
    }
} else {
    Add-Log "❌ Clé de registre LxssManager non trouvée !"
}
Add-Log ""

# 5. FONCTIONNALITÉS WINDOWS
Add-Log "5. FONCTIONNALITÉS WINDOWS"
Add-Log "-" * 80

$features = @(
    "Microsoft-Windows-Subsystem-Linux",
    "VirtualMachinePlatform",
    "Microsoft-Hyper-V-All",
    "Microsoft-Hyper-V",
    "HypervisorPlatform"
)

foreach ($feature in $features) {
    $feat = Get-WindowsOptionalFeature -Online -FeatureName $feature -ErrorAction SilentlyContinue
    if ($feat) {
        Add-Log "$feature : $($feat.State)"
    } else {
        Add-Log "$feature : Non disponible"
    }
}
Add-Log ""

# 6. LOGS D'ÉVÉNEMENTS
Add-Log "6. LOGS D'ÉVÉNEMENTS RÉCENTS (WSL)"
Add-Log "-" * 80

$events = Get-WinEvent -FilterHashtable @{
    LogName='System'
    ProviderName='Service Control Manager'
    StartTime=(Get-Date).AddHours(-1)
} -MaxEvents 50 -ErrorAction SilentlyContinue | 
Where-Object { $_.Message -like "*LxssManager*" -or $_.Message -like "*WSL*" }

if ($events) {
    foreach ($evt in $events) {
        Add-Log ""
        Add-Log "[$($evt.TimeCreated)] Niveau: $($evt.LevelDisplayName)"
        Add-Log "Message: $($evt.Message)"
    }
} else {
    Add-Log "Aucun événement WSL trouvé dans la dernière heure"
}
Add-Log ""

# 7. PILOTES
Add-Log "7. PILOTES DE VIRTUALISATION"
Add-Log "-" * 80

$drivers = Get-WindowsDriver -Online -All | Where-Object { 
    $_.Driver -like "*wsl*" -or 
    $_.Driver -like "*hyper*" -or 
    $_.Driver -like "*vm*" 
}

if ($drivers) {
    foreach ($drv in $drivers) {
        Add-Log "Pilote : $($drv.Driver)"
        Add-Log "  Provider : $($drv.ProviderName)"
        Add-Log "  Version : $($drv.Version)"
        Add-Log "  Date : $($drv.Date)"
        Add-Log ""
    }
} else {
    Add-Log "Aucun pilote de virtualisation trouvé"
}
Add-Log ""

# 8. LOGICIELS DE VIRTUALISATION CONFLICTUELS
Add-Log "8. LOGICIELS DE VIRTUALISATION INSTALLÉS"
Add-Log "-" * 80

$conflictingSoftware = @(
    "VirtualBox",
    "VMware",
    "QEMU",
    "Parallels"
)

$installedSoftware = Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |
                     Select-Object DisplayName, DisplayVersion, Publisher

foreach ($software in $conflictingSoftware) {
    $found = $installedSoftware | Where-Object { $_.DisplayName -like "*$software*" }
    if ($found) {
        Add-Log "⚠️  CONFLIT POTENTIEL : $($found.DisplayName) $($found.DisplayVersion)"
    }
}
Add-Log ""

# 9. DISTRIBUTIONS WSL
Add-Log "9. DISTRIBUTIONS WSL"
Add-Log "-" * 80

$wslList = wsl --list --verbose 2>&1
Add-Log "Résultat de 'wsl --list --verbose' :"
Add-Log $wslList
Add-Log ""

# 10. TEST DE DÉMARRAGE DU SERVICE
Add-Log "10. TEST DE DÉMARRAGE DU SERVICE"
Add-Log "-" * 80

Add-Log "Arrêt du service..."
Stop-Service -Name LxssManager -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

Add-Log "Démarrage du service..."
$startTime = Get-Date
sc.exe start LxssManager 2>&1 | ForEach-Object { Add-Log "  $_" }
Start-Sleep -Seconds 3

$service = Get-Service -Name LxssManager
$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds

Add-Log ""
Add-Log "État après démarrage : $($service.Status)"
Add-Log "Temps écoulé : $duration secondes"

if ($service.Status -eq "Running") {
    Add-Log "✅ Le service démarre correctement"
    
    # Tester combien de temps il reste actif
    Add-Log ""
    Add-Log "Test de stabilité (30 secondes)..."
    for ($i = 1; $i -le 30; $i++) {
        Start-Sleep -Seconds 1
        $svc = Get-Service -Name LxssManager
        if ($svc.Status -ne "Running") {
            Add-Log "❌ Le service s'est arrêté après $i secondes !"
            break
        }
        if ($i % 5 -eq 0) {
            Add-Log "  $i secondes : toujours actif"
        }
    }
    
    $finalSvc = Get-Service -Name LxssManager
    if ($finalSvc.Status -eq "Running") {
        Add-Log "✅ Le service est resté actif pendant 30 secondes"
    }
} else {
    Add-Log "❌ Le service n'a pas démarré"
}
Add-Log ""

# 11. PERMISSIONS
Add-Log "11. PERMISSIONS DU SERVICE"
Add-Log "-" * 80

$servicePath = "C:\Windows\System32\lxss"
if (Test-Path $servicePath) {
    $acl = Get-Acl $servicePath
    Add-Log "Permissions du dossier lxss :"
    foreach ($access in $acl.Access) {
        Add-Log "  $($access.IdentityReference) : $($access.FileSystemRights)"
    }
} else {
    Add-Log "❌ Dossier lxss non trouvé !"
}
Add-Log ""

# Sauvegarder le rapport
$output | Out-File -FilePath $logFile -Encoding UTF8

Write-Host ""
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ DIAGNOSTIC TERMINÉ" -ForegroundColor Green
Write-Host ""
Write-Host "Rapport sauvegardé dans :" -ForegroundColor Cyan
Write-Host "  $logFile" -ForegroundColor White
Write-Host ""
Write-Host "Analysons maintenant les résultats..." -ForegroundColor Yellow
Write-Host ""

# ANALYSE AUTOMATIQUE
Write-Host "ANALYSE AUTOMATIQUE :" -ForegroundColor Cyan
Write-Host ""

$issues = @()

# Vérifier si le service reste actif
$svc = Get-Service -Name LxssManager
if ($svc.Status -ne "Running") {
    $issues += "Le service LxssManager ne reste pas actif"
}

# Vérifier les logiciels conflictuels
$vbox = $installedSoftware | Where-Object { $_.DisplayName -like "*VirtualBox*" }
$vmware = $installedSoftware | Where-Object { $_.DisplayName -like "*VMware*" }

if ($vbox) {
    $issues += "VirtualBox installé (conflit avec Hyper-V)"
}
if ($vmware) {
    $issues += "VMware installé (conflit avec Hyper-V)"
}

# Vérifier la virtualisation
if (-not $cpu.VirtualizationFirmwareEnabled) {
    $issues += "Virtualisation désactivée dans le BIOS"
}

if ($issues.Count -gt 0) {
    Write-Host "PROBLÈMES DÉTECTÉS :" -ForegroundColor Red
    foreach ($issue in $issues) {
        Write-Host "  ❌ $issue" -ForegroundColor Red
    }
} else {
    Write-Host "✅ Aucun problème évident détecté" -ForegroundColor Green
}

Write-Host ""
Write-Host "Consultez le rapport complet pour plus de détails." -ForegroundColor Yellow
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
