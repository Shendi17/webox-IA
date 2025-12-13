# Installation forcée du pilote WSL
# Date : 1er Novembre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     INSTALLATION FORCÉE PILOTE WSL                             " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    exit
}

Write-Host "DIAGNOSTIC APPROFONDI" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Gray
Write-Host ""

# Vérifier la version de Windows
$os = Get-CimInstance -ClassName Win32_OperatingSystem
Write-Host "Windows : $($os.Caption) - Build $($os.BuildNumber)" -ForegroundColor White

if ($os.BuildNumber -lt 19041) {
    Write-Host "⚠️  Votre version de Windows est trop ancienne pour WSL 2" -ForegroundColor Yellow
    Write-Host "   WSL 2 nécessite Windows 10 version 2004 (build 19041) ou supérieur" -ForegroundColor White
    Write-Host ""
    Write-Host "Mettez à jour Windows via Windows Update" -ForegroundColor Cyan
    exit
}

Write-Host "✅ Version de Windows compatible" -ForegroundColor Green
Write-Host ""

# Télécharger et installer le package de mise à jour WSL
Write-Host "TÉLÉCHARGEMENT DU PACKAGE WSL" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Gray
Write-Host ""

$wslUpdateUrl = "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi"
$wslUpdatePath = "$env:TEMP\wsl_update_x64.msi"

Write-Host "Téléchargement du package de mise à jour WSL..." -ForegroundColor Yellow
Write-Host "URL : $wslUpdateUrl" -ForegroundColor Gray

try {
    # Télécharger avec progression
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $wslUpdateUrl -OutFile $wslUpdatePath -UseBasicParsing
    $ProgressPreference = 'Continue'
    
    Write-Host "✅ Téléchargement terminé" -ForegroundColor Green
    Write-Host ""
    
    # Installer le package
    Write-Host "Installation du package WSL..." -ForegroundColor Yellow
    Write-Host "⏳ Cela peut prendre 2-3 minutes..." -ForegroundColor Gray
    Write-Host ""
    
    Start-Process msiexec.exe -ArgumentList "/i `"$wslUpdatePath`" /quiet /norestart" -Wait -NoNewWindow
    
    Write-Host "✅ Package installé" -ForegroundColor Green
    Write-Host ""
    
    # Nettoyer
    Remove-Item $wslUpdatePath -Force -ErrorAction SilentlyContinue
    
} catch {
    Write-Host "❌ Erreur lors du téléchargement : $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Téléchargez manuellement depuis :" -ForegroundColor Yellow
    Write-Host "https://aka.ms/wsl2kernel" -ForegroundColor White
    Write-Host ""
}

# Configurer WSL 2 par défaut
Write-Host "CONFIGURATION WSL 2" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Gray
Write-Host ""

Write-Host "Définition de WSL 2 comme version par défaut..." -ForegroundColor Yellow
wsl --set-default-version 2 2>$null

Write-Host "✅ WSL 2 configuré" -ForegroundColor Green
Write-Host ""

# Vérifier et démarrer le service avec toutes les dépendances
Write-Host "DÉMARRAGE DES SERVICES" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Gray
Write-Host ""

$services = @(
    @{Name="RPCSS"; Display="RPC"},
    @{Name="HvHost"; Display="Hyper-V Host"},
    @{Name="vmcompute"; Display="VM Compute"},
    @{Name="LxssManager"; Display="WSL Manager"}
)

foreach ($svc in $services) {
    Write-Host "Démarrage de $($svc.Display)..." -ForegroundColor Yellow
    
    # Configurer en automatique
    sc.exe config $($svc.Name) start= demand 2>$null
    
    # Démarrer
    sc.exe start $($svc.Name) 2>$null
    Start-Sleep -Seconds 1
    
    # Vérifier
    $service = Get-Service -Name $($svc.Name) -ErrorAction SilentlyContinue
    if ($service -and $service.Status -eq "Running") {
        Write-Host "  ✅ $($svc.Display) : Running" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $($svc.Display) : $($service.Status)" -ForegroundColor Yellow
    }
}

Write-Host ""

# Test final
Write-Host "TEST FINAL" -ForegroundColor Cyan
Write-Host "==========" -ForegroundColor Gray
Write-Host ""

$lxss = Get-Service -Name LxssManager
Write-Host "Service LxssManager : $($lxss.Status)" -ForegroundColor $(if ($lxss.Status -eq "Running") { "Green" } else { "Red" })

if ($lxss.Status -eq "Running") {
    Write-Host ""
    Write-Host "✅ SERVICE DÉMARRÉ !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Tentative d'installation d'Ubuntu..." -ForegroundColor Cyan
    Write-Host ""
    
    # Essayer d'installer Ubuntu IMMÉDIATEMENT
    $installResult = wsl --install -d Ubuntu --no-launch 2>&1
    
    if ($LASTEXITCODE -eq 0 -or $installResult -like "*déjà installé*") {
        Write-Host "✅ UBUNTU INSTALLÉ !" -ForegroundColor Green
        Write-Host ""
        Write-Host "Vérification..." -ForegroundColor Yellow
        wsl --list --verbose
        Write-Host ""
        Write-Host "================================================================" -ForegroundColor Gray
        Write-Host ""
        Write-Host "✅ SUCCÈS COMPLET !" -ForegroundColor Green
        Write-Host ""
        Write-Host "Prochaines étapes :" -ForegroundColor Cyan
        Write-Host "  1. Lancer Ubuntu depuis le menu Démarrer" -ForegroundColor White
        Write-Host "  2. Créer un utilisateur Linux" -ForegroundColor White
        Write-Host "  3. Lancer Docker Desktop" -ForegroundColor White
        Write-Host "  4. Installer PostgreSQL" -ForegroundColor White
    } else {
        Write-Host "❌ Échec de l'installation" -ForegroundColor Red
        Write-Host ""
        Write-Host "Message d'erreur :" -ForegroundColor Yellow
        Write-Host $installResult
        Write-Host ""
        Write-Host "Le service fonctionne mais l'installation échoue." -ForegroundColor Yellow
        Write-Host "Essayez de redémarrer Windows puis de lancer Ubuntu" -ForegroundColor Cyan
    }
} else {
    Write-Host ""
    Write-Host "❌ LE SERVICE NE DÉMARRE PAS" -ForegroundColor Red
    Write-Host ""
    Write-Host "DERNIÈRE SOLUTION : Vérifier les logs système" -ForegroundColor Yellow
    Write-Host ""
    
    # Afficher les logs d'erreur
    Write-Host "Logs d'erreur récents :" -ForegroundColor Cyan
    $events = Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='Service Control Manager'} -MaxEvents 10 -ErrorAction SilentlyContinue |
              Where-Object { $_.Message -like "*LxssManager*" -or $_.Message -like "*WSL*" }
    
    if ($events) {
        foreach ($event in $events) {
            Write-Host ""
            Write-Host "[$($event.TimeCreated)] $($event.LevelDisplayName)" -ForegroundColor Yellow
            Write-Host $event.Message -ForegroundColor White
        }
    } else {
        Write-Host "Aucun log trouvé" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Gray
    Write-Host ""
    Write-Host "CAUSES POSSIBLES :" -ForegroundColor Yellow
    Write-Host "  1. Pilote de virtualisation corrompu" -ForegroundColor White
    Write-Host "  2. Conflit avec un logiciel de virtualisation (VirtualBox, VMware)" -ForegroundColor White
    Write-Host "  3. Registre système corrompu" -ForegroundColor White
    Write-Host ""
    Write-Host "SOLUTIONS :" -ForegroundColor Cyan
    Write-Host "  1. Désinstaller VirtualBox/VMware si installés" -ForegroundColor White
    Write-Host "  2. Redémarrer Windows en mode sans échec et réessayer" -ForegroundColor White
    Write-Host "  3. Réinstaller Windows (solution extrême)" -ForegroundColor White
}

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
