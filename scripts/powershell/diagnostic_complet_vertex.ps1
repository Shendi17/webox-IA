# Diagnostic complet Vertex AI
# Pour comprendre exactement ce qui ne fonctionne pas

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DIAGNOSTIC COMPLET VERTEX AI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$gcloudPath = "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin"
if (Test-Path "$gcloudPath\gcloud.cmd") {
    $env:Path = "$gcloudPath;$env:Path"
}

# 1. Verifier la facturation
Write-Host "[1/8] Verification de la facturation..." -ForegroundColor Green
Write-Host ""

if (Test-Path "$gcloudPath\gcloud.cmd") {
    Write-Host "  Recuperation des informations de facturation..." -ForegroundColor Yellow
    $billingInfo = & "$gcloudPath\gcloud.cmd" beta billing projects describe webox-482718 --format="value(billingAccountName,billingEnabled)" 2>$null
    
    if ($billingInfo) {
        Write-Host "  Informations de facturation:" -ForegroundColor Cyan
        Write-Host "  $billingInfo" -ForegroundColor White
        
        if ($billingInfo -match "True") {
            Write-Host "  Statut: FACTURATION ACTIVEE" -ForegroundColor Green
        } else {
            Write-Host "  Statut: FACTURATION DESACTIVEE" -ForegroundColor Red
            Write-Host "  Action requise: Activez la facturation sur:" -ForegroundColor Yellow
            Write-Host "  https://console.cloud.google.com/billing/linkedaccount?project=webox-482718" -ForegroundColor Cyan
        }
    } else {
        Write-Host "  Impossible de recuperer les informations de facturation" -ForegroundColor Yellow
        Write-Host "  Verifiez manuellement sur:" -ForegroundColor Yellow
        Write-Host "  https://console.cloud.google.com/billing/linkedaccount?project=webox-482718" -ForegroundColor Cyan
    }
} else {
    Write-Host "  gcloud CLI non trouve - verification manuelle requise" -ForegroundColor Yellow
}

Write-Host ""

# 2. Verifier les APIs activees
Write-Host "[2/8] Verification des APIs..." -ForegroundColor Green
Write-Host ""

if (Test-Path "$gcloudPath\gcloud.cmd") {
    $apis = & "$gcloudPath\gcloud.cmd" services list --enabled --filter="name:(aiplatform.googleapis.com OR generativelanguage.googleapis.com)" --format="value(name)" 2>$null
    
    if ($apis -match "aiplatform") {
        Write-Host "  Vertex AI API (aiplatform.googleapis.com): ACTIVEE" -ForegroundColor Green
    } else {
        Write-Host "  Vertex AI API (aiplatform.googleapis.com): DESACTIVEE" -ForegroundColor Red
        Write-Host "  Activation..." -ForegroundColor Yellow
        & "$gcloudPath\gcloud.cmd" services enable aiplatform.googleapis.com 2>&1 | Out-Null
        Write-Host "  API activee" -ForegroundColor Green
    }
}

Write-Host ""

# 3. Verifier le service account et ses roles
Write-Host "[3/8] Verification du service account..." -ForegroundColor Green
Write-Host ""

$serviceAccount = "webox-468@webox-482718.iam.gserviceaccount.com"
Write-Host "  Service Account: $serviceAccount" -ForegroundColor Cyan

if (Test-Path "$gcloudPath\gcloud.cmd") {
    Write-Host "  Verification des roles IAM..." -ForegroundColor Yellow
    $roles = & "$gcloudPath\gcloud.cmd" projects get-iam-policy webox-482718 --flatten="bindings[].members" --filter="bindings.members:serviceAccount:$serviceAccount" --format="value(bindings.role)" 2>$null
    
    if ($roles) {
        Write-Host "  Roles attribues:" -ForegroundColor Green
        $roles -split "`n" | ForEach-Object {
            if ($_ -ne "") {
                Write-Host "    - $_" -ForegroundColor White
            }
        }
        
        # Verifier les roles necessaires
        $requiredRoles = @(
            "roles/aiplatform.user",
            "roles/ml.developer",
            "roles/serviceusage.serviceUsageConsumer"
        )
        
        Write-Host ""
        Write-Host "  Verification des roles necessaires:" -ForegroundColor Yellow
        foreach ($role in $requiredRoles) {
            if ($roles -match $role) {
                Write-Host "    $role : OK" -ForegroundColor Green
            } else {
                Write-Host "    $role : MANQUANT" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "  AUCUN ROLE ATTRIBUE" -ForegroundColor Red
        Write-Host "  Le service account n'a pas de permissions!" -ForegroundColor Red
    }
}

Write-Host ""

# 4. Verifier le fichier de credentials
Write-Host "[4/8] Verification du fichier de credentials..." -ForegroundColor Green
Write-Host ""

$credFile = "C:\Users\Anthony\CascadeProjects\webox\webox-482718-f86837e5ce03.json"
if (Test-Path $credFile) {
    Write-Host "  Fichier: $credFile" -ForegroundColor Cyan
    Write-Host "  Statut: EXISTE" -ForegroundColor Green
    
    # Lire le contenu
    $credContent = Get-Content $credFile -Raw | ConvertFrom-Json
    Write-Host "  Type: $($credContent.type)" -ForegroundColor White
    Write-Host "  Project ID: $($credContent.project_id)" -ForegroundColor White
    Write-Host "  Client Email: $($credContent.client_email)" -ForegroundColor White
    
    if ($credContent.client_email -eq $serviceAccount) {
        Write-Host "  Correspondance service account: OK" -ForegroundColor Green
    } else {
        Write-Host "  ATTENTION: Le client_email ne correspond pas!" -ForegroundColor Red
        Write-Host "  Attendu: $serviceAccount" -ForegroundColor Yellow
        Write-Host "  Trouve: $($credContent.client_email)" -ForegroundColor Yellow
    }
} else {
    Write-Host "  Fichier: $credFile" -ForegroundColor Cyan
    Write-Host "  Statut: INTROUVABLE" -ForegroundColor Red
}

Write-Host ""

# 5. Verifier le fichier .env
Write-Host "[5/8] Verification du fichier .env..." -ForegroundColor Green
Write-Host ""

if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    
    # Verifier VERTEX_AI_PROJECT_ID
    if ($envContent -match "VERTEX_AI_PROJECT_ID=(.+)") {
        $projectId = $matches[1].Trim()
        Write-Host "  VERTEX_AI_PROJECT_ID: $projectId" -ForegroundColor Cyan
        if ($projectId -eq "webox-482718") {
            Write-Host "    Status: OK" -ForegroundColor Green
        } else {
            Write-Host "    Status: INCORRECT (devrait etre webox-482718)" -ForegroundColor Red
        }
    } else {
        Write-Host "  VERTEX_AI_PROJECT_ID: NON CONFIGURE" -ForegroundColor Red
    }
    
    # Verifier VERTEX_AI_LOCATION
    if ($envContent -match "VERTEX_AI_LOCATION=(.+)") {
        $location = $matches[1].Trim()
        Write-Host "  VERTEX_AI_LOCATION: $location" -ForegroundColor Cyan
    } else {
        Write-Host "  VERTEX_AI_LOCATION: NON CONFIGURE" -ForegroundColor Red
    }
    
    # Verifier GOOGLE_APPLICATION_CREDENTIALS
    if ($envContent -match "^GOOGLE_APPLICATION_CREDENTIALS=(.+)" -and $envContent -notmatch "^#.*GOOGLE_APPLICATION_CREDENTIALS") {
        $credPath = $matches[1].Trim()
        Write-Host "  GOOGLE_APPLICATION_CREDENTIALS: $credPath" -ForegroundColor Cyan
        Write-Host "    Status: ACTIVE" -ForegroundColor Green
    } elseif ($envContent -match "^#.*GOOGLE_APPLICATION_CREDENTIALS=(.+)") {
        Write-Host "  GOOGLE_APPLICATION_CREDENTIALS: COMMENTE" -ForegroundColor Yellow
        Write-Host "    Le systeme utilisera gcloud auth" -ForegroundColor Cyan
    } else {
        Write-Host "  GOOGLE_APPLICATION_CREDENTIALS: NON CONFIGURE" -ForegroundColor Yellow
        Write-Host "    Le systeme utilisera gcloud auth" -ForegroundColor Cyan
    }
}

Write-Host ""

# 6. Tester l'authentification gcloud
Write-Host "[6/8] Test authentification gcloud..." -ForegroundColor Green
Write-Host ""

if (Test-Path "$gcloudPath\gcloud.cmd") {
    $authAccount = & "$gcloudPath\gcloud.cmd" auth list --filter="status:ACTIVE" --format="value(account)" 2>$null
    if ($authAccount) {
        Write-Host "  Compte actif: $authAccount" -ForegroundColor Green
        
        # Verifier application-default
        $credPath = "$env:APPDATA\gcloud\application_default_credentials.json"
        if (Test-Path $credPath) {
            Write-Host "  Application-default credentials: OK" -ForegroundColor Green
        } else {
            Write-Host "  Application-default credentials: MANQUANT" -ForegroundColor Red
        }
    } else {
        Write-Host "  Aucun compte authentifie" -ForegroundColor Red
    }
}

Write-Host ""

# 7. Test de connexion Python
Write-Host "[7/8] Test de connexion Python..." -ForegroundColor Green
Write-Host ""

$testScript = @"
import os
from dotenv import load_dotenv
load_dotenv()

print('Variables d environnement:')
print(f'  PROJECT_ID: {os.getenv("VERTEX_AI_PROJECT_ID")}')
print(f'  LOCATION: {os.getenv("VERTEX_AI_LOCATION")}')
cred = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print(f'  CREDENTIALS: {cred if cred else "gcloud auth"}')
print()

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    
    project_id = os.getenv('VERTEX_AI_PROJECT_ID')
    location = os.getenv('VERTEX_AI_LOCATION', 'us-central1')
    
    print(f'Initialisation Vertex AI...')
    print(f'  Projet: {project_id}')
    print(f'  Region: {location}')
    
    vertexai.init(project=project_id, location=location)
    print('  Status: OK')
    print()
    
    print('Creation du modele gemini-1.0-pro...')
    model = GenerativeModel('gemini-1.0-pro')
    print('  Status: OK')
    print()
    
    print('Test de generation...')
    response = model.generate_content('Dis bonjour en un mot')
    print(f'  Reponse: {response.text}')
    print('  Status: SUCCES!')
    
except Exception as e:
    print(f'ERREUR: {e}')
    import traceback
    traceback.print_exc()
"@

python -c $testScript

Write-Host ""

# 8. Recommandations
Write-Host "[8/8] Recommandations..." -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ACTIONS A EFFECTUER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Si la facturation n'est pas activee:" -ForegroundColor Yellow
Write-Host "   https://console.cloud.google.com/billing/linkedaccount?project=webox-482718" -ForegroundColor Cyan
Write-Host ""

Write-Host "2. Verifier les roles IAM du service account:" -ForegroundColor Yellow
Write-Host "   https://console.cloud.google.com/iam-admin/iam?project=webox-482718" -ForegroundColor Cyan
Write-Host "   Roles necessaires:" -ForegroundColor White
Write-Host "   - Vertex AI User (roles/aiplatform.user)" -ForegroundColor White
Write-Host "   - ML Developer (roles/ml.developer)" -ForegroundColor White
Write-Host ""

Write-Host "3. Dans le fichier .env, decommentez:" -ForegroundColor Yellow
Write-Host "   GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Anthony\CascadeProjects\webox\webox-482718-f86837e5ce03.json" -ForegroundColor Cyan
Write-Host ""

Write-Host "4. Testez a nouveau:" -ForegroundColor Yellow
Write-Host "   python test_vertex_connection.py" -ForegroundColor Cyan
Write-Host ""
