# Script PowerShell pour appliquer le theme coherent
# Date: 13 Decembre 2024

Write-Host "Application du theme coherent..." -ForegroundColor Cyan

$templatesPath = "C:\Users\Anthony\CascadeProjects\webox\templates\dashboard"
$filesModified = 0

# Exclure les fichiers deja traites
$excludeFiles = @("base_dashboard.html", "blog_old_with_generator.html")

$htmlFiles = Get-ChildItem -Path $templatesPath -Filter "*.html" | Where-Object { $excludeFiles -notcontains $_.Name }

Write-Host "Fichiers a traiter: $($htmlFiles.Count)" -ForegroundColor Yellow

foreach ($file in $htmlFiles) {
    Write-Host "Traitement de: $($file.Name)" -ForegroundColor White
    
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $modified = $false
    
    # Remplacer le gradient violet/bleu par bleu fonce
    $pattern1 = 'background:\s*linear-gradient\(135deg,\s*#667eea\s+0%,\s*#764ba2\s+100%\)'
    $replacement1 = 'background: linear-gradient(135deg, #0f3460 0%, #1a1a2e 100%)'
    
    if ($content -match $pattern1) {
        $content = $content -replace $pattern1, $replacement1
        Write-Host "  Hero gradient mis a jour" -ForegroundColor Green
        $modified = $true
    }
    
    # Remplacer boutons blancs par boutons jaunes
    $pattern2 = 'background:\s*white;\s*color:\s*#667eea;'
    $replacement2 = 'background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); color: #1a1a2e; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);'
    
    if ($content -match $pattern2) {
        $content = $content -replace $pattern2, $replacement2
        Write-Host "  Boutons mis a jour" -ForegroundColor Green
        $modified = $true
    }
    
    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
        $filesModified++
        Write-Host "  Fichier sauvegarde" -ForegroundColor Green
    }
}

Write-Host "`nTraitement termine!" -ForegroundColor Green
Write-Host "Fichiers modifies: $filesModified" -ForegroundColor Cyan
