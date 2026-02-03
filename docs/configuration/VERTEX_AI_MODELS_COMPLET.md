# 📋 LISTE COMPLÈTE DES MODÈLES VERTEX AI DISPONIBLES (2026)

Source officielle : https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models

---

## 💬 MODÈLES TEXTE - GEMINI

### **Gemini 2.5 (Generally Available)**
| Modèle | ID Vertex AI | Description |
|--------|--------------|-------------|
| Gemini 2.5 Pro | `gemini-2.5-pro` | Haute performance pour raisonnement complexe |
| Gemini 2.5 Flash | `gemini-2.5-flash` | Rapide et performant (recommandé) |
| Gemini 2.5 Flash Lite | `gemini-2.5-flash-lite` | Version légère pour grande échelle |
| Gemini 2.5 Flash Image | `gemini-2.5-flash-image` | Génération et édition d'images |
| Gemini Live 2.5 Flash | `gemini-live-2.5-flash-native-audio` | Audio natif en temps réel |

### **Gemini 2.0 (Generally Available)**
| Modèle | ID Vertex AI | Description |
|--------|--------------|-------------|
| Gemini 2.0 Flash | `gemini-2.0-flash-001` | Flash version 2.0 |
| Gemini 2.0 Flash Lite | `gemini-2.0-flash-lite-001` | Version légère 2.0 |

### **Gemini 3 (Preview)**
| Modèle | ID Vertex AI | Description |
|--------|--------------|-------------|
| Gemini 3 Pro | `gemini-3-pro` | Compréhension multimodale avancée |
| Gemini 3 Flash | `gemini-3-flash` | Modèle agentique et coding puissant |
| Gemini 3 Pro Image | `gemini-3-pro-image` | Génération d'images avec Gemini 3 |

---

## 🎨 MODÈLES IMAGES - IMAGEN

### **Imagen 4 (Latest)**
| Modèle | ID Vertex AI | Description |
|--------|--------------|-------------|
| Imagen 4 Generate | `imagen-4.0-generate-001` | Génération d'images haute qualité |
| Imagen 4 Fast Generate | `imagen-4.0-fast-generate-001` | Génération rapide |
| Imagen 4 Ultra Generate | `imagen-4.0-ultra-generate-001` | Qualité ultra (meilleure) |

### **Imagen 3 (Stable)**
| Modèle | ID Vertex AI | Description |
|--------|--------------|-------------|
| Imagen 3 Generate 002 | `imagen-3.0-generate-002` | Génération v2 |
| Imagen 3 Generate 001 | `imagen-3.0-generate-001` | Génération v1 |
| Imagen 3 Fast Generate | `imagen-3.0-fast-generate-001` | Génération rapide |
| Imagen 3 Capability | `imagen-3.0-capability-001` | Édition et personnalisation |

### **Imagen Spécialisés (Preview)**
| Modèle | ID Vertex AI | Description |
|--------|--------------|-------------|
| Product Recontext | `imagen-product-recontext-preview-06-30` | Recontext produits |
| Virtual Try-On | (Preview) | Essayage virtuel |

---

## 🎬 MODÈLES VIDÉO - VEO

### **Veo 3.1 (Latest)**
| Modèle | ID Vertex AI | Description |
|--------|--------------|-------------|
| Veo 3.1 Generate | `veo-3.1-generate-001` | Génération vidéo haute qualité |
| Veo 3.1 Fast Generate | `veo-3.1-fast-generate-001` | Génération vidéo rapide |

### **Veo 3.0**
| Modèle | ID Vertex AI | Description |
|--------|--------------|-------------|
| Veo 3.0 Generate | `veo-3.0-generate-001` | Génération vidéo v3.0 |
| Veo 3.0 Fast Generate | `veo-3.0-fast-generate-001` | Génération rapide v3.0 |

### **Veo 2.0**
| Modèle | ID Vertex AI | Description |
|--------|--------------|-------------|
| Veo 2.0 Generate | `veo-2.0-generate-001` | Génération vidéo v2.0 |

---

## 🔤 MODÈLES EMBEDDINGS

| Modèle | ID Vertex AI | Description |
|--------|--------------|-------------|
| Gemini Embedding | `gemini-embedding-001` | Embeddings Gemini |
| Text Embedding 005 | `text-embedding-005` | Embeddings texte v5 (latest) |
| Text Embedding 004 | `text-embedding-004` | Embeddings texte v4 |
| Text Multilingual | `text-multilingual-embedding-002` | Embeddings multilingue |
| Multimodal Embedding | `multimodalembedding@001` | Embeddings multimodaux |

---

## 🧬 MODÈLES GEMMA (Open Source)

| Modèle | Description |
|--------|-------------|
| Gemma 3n | Dernière version nano |
| Gemma 3 | Dernière version |
| Gemma 2 | Version 2 |
| ShieldGemma 2 | Modération de contenu |
| PaliGemma | Vision-language |
| CodeGemma | Spécialisé code |
| TxGemma | Traduction |
| MedGemma | Médical |
| MedSigLIP | Médical vision |
| T5Gemma | Text-to-text |

---

## 🏥 MODÈLES MÉDICAUX - MEDLM

| Modèle | Description |
|--------|-------------|
| MedLM | Modèles spécialisés médecine |

---

## 📊 RÉSUMÉ PAR CATÉGORIE

| Catégorie | Nombre de modèles | Recommandé |
|-----------|-------------------|------------|
| **Texte (Gemini)** | 11 modèles | `gemini-2.5-flash` |
| **Images (Imagen)** | 9 modèles | `imagen-4.0-generate-001` |
| **Vidéo (Veo)** | 5 modèles | `veo-3.1-generate-001` |
| **Embeddings** | 5 modèles | `text-embedding-005` |
| **Gemma (Open)** | 10+ modèles | `gemma-3` |

---

## 🎯 MODÈLES RECOMMANDÉS PAR USAGE

### **Chat & Conversation**
- `gemini-2.5-flash` - Meilleur rapport qualité/vitesse
- `gemini-2.5-pro` - Tâches complexes

### **Génération d'Images**
- `imagen-4.0-ultra-generate-001` - Meilleure qualité
- `imagen-4.0-fast-generate-001` - Rapide

### **Génération de Vidéos**
- `veo-3.1-generate-001` - Dernière version
- `veo-3.1-fast-generate-001` - Rapide

### **Embeddings**
- `text-embedding-005` - Texte (latest)
- `multimodalembedding@001` - Multimodal

---

## ⚠️ NOTES IMPORTANTES

1. **Modèles Preview** : Les modèles Gemini 3 et certains Imagen sont en preview (peuvent changer)
2. **Disponibilité régionale** : Tous les modèles ne sont pas disponibles dans toutes les régions
3. **Facturation** : Vertex AI nécessite une facturation active
4. **Région recommandée** : `us-central1` pour la meilleure disponibilité

---

## 🔗 DOCUMENTATION OFFICIELLE

- **Gemini** : https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini
- **Imagen** : https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/imagen
- **Veo** : https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/veo
- **Model Versions** : https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions

---

**Dernière mise à jour : Janvier 2026**
