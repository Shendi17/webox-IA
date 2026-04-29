# 📥 INSTALLATION MANUELLE DE FFMPEG

L'installation automatique via Chocolatey a échoué à cause d'un problème de permissions.

---

## 🔧 MÉTHODE MANUELLE (RECOMMANDÉE)

### Étape 1: Télécharger FFmpeg

1. Ouvrez votre navigateur
2. Allez sur: **https://www.gyan.dev/ffmpeg/builds/**
3. Téléchargez: **ffmpeg-release-essentials.zip** (version la plus récente)

### Étape 2: Extraire l'archive

1. Extrayez le fichier ZIP téléchargé
2. Vous obtiendrez un dossier comme `ffmpeg-7.0-essentials_build`
3. Déplacez ce dossier vers `C:\ffmpeg`

### Étape 3: Ajouter FFmpeg au PATH

**Méthode PowerShell (ADMIN REQUIS):**

```powershell
# Ouvrir PowerShell en tant qu'Administrateur
# Puis exécuter:

$ffmpegPath = "C:\ffmpeg\bin"
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$ffmpegPath", [EnvironmentVariableTarget]::Machine)
```

**Méthode Manuelle:**

1. Appuyez sur `Windows + R`
2. Tapez: `sysdm.cpl` et appuyez sur Entrée
3. Allez dans l'onglet **Avancé**
4. Cliquez sur **Variables d'environnement**
5. Dans **Variables système**, trouvez `Path` et cliquez sur **Modifier**
6. Cliquez sur **Nouveau**
7. Ajoutez: `C:\ffmpeg\bin`
8. Cliquez sur **OK** partout

### Étape 4: Vérifier l'installation

**Fermez et rouvrez PowerShell**, puis:

```powershell
ffmpeg -version
```

Si vous voyez la version de FFmpeg, c'est installé ! ✅

---

## 🚀 ALTERNATIVE: Installation avec Chocolatey (Admin)

Si vous avez des droits administrateur:

```powershell
# Ouvrir PowerShell en tant qu'Administrateur
choco install ffmpeg -y
```

---

## ✅ APRÈS L'INSTALLATION

Une fois FFmpeg installé:

1. **Redémarrez le serveur WeBox**
   ```powershell
   # Arrêter le serveur (Ctrl+C dans le terminal)
   # Puis relancer:
   python -m uvicorn app.main:app --reload
   ```

2. **Testez la génération vidéo**
   - Allez sur http://webox.local:8000/generation
   - Onglet 🎬 Vidéos
   - Générez une vidéo
   - Vous devriez obtenir un fichier MP4 réel !

---

## 📊 ÉTAT ACTUEL

### ✅ Déjà Corrigé

- **Audio:** Modèle `openai-tts` maintenant supporté
- **Code vidéo:** Restauré pour générer des MP4 avec FFmpeg
- **Fallback:** Si FFmpeg manque, génère des PNG (temporaire)

### ⏳ En Attente

- **FFmpeg:** Installation manuelle requise
- **Format vidéo:** Sera MP4 une fois FFmpeg installé

---

## 🎯 RÉSULTAT ATTENDU

**Avec FFmpeg installé:**
- ✅ Vidéos: Vrais fichiers MP4 (pas PNG)
- ✅ Shorts: Vrais fichiers MP4
- ✅ Publicités: Vrais fichiers MP4
- ✅ Audio: Fichiers MP3 (déjà fonctionnel)

**Sans FFmpeg (actuellement):**
- ⚠️ Vidéos: Images PNG (fallback)
- ⚠️ Shorts: Images PNG (fallback)
- ⚠️ Publicités: Images PNG (fallback)
- ✅ Audio: Fichiers MP3 (fonctionne)
