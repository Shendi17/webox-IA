"""Test direct de l'API"""
import requests
import json

# Test 1: Liste des projets
print("=" * 50)
print("TEST 1: Liste des projets")
print("=" * 50)
try:
    response = requests.get("http://localhost:8000/api/projects")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Projets trouvés: {len(data.get('projects', []))}")
        for p in data.get('projects', [])[:3]:
            print(f"  - {p['name']} (ID: {p['id']})")
    else:
        print(f"Erreur: {response.text}")
except Exception as e:
    print(f"Exception: {e}")

# Test 2: Fichiers du projet 1
print("\n" + "=" * 50)
print("TEST 2: Fichiers du projet 1")
print("=" * 50)
try:
    response = requests.get("http://localhost:8000/api/projects/1/files")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Fichiers trouvés: {len(data.get('files', []))}")
        for f in data.get('files', [])[:5]:
            print(f"  - {f['name']} ({'dossier' if f.get('is_directory') else 'fichier'})")
    else:
        print(f"Erreur: {response.text[:200]}")
except Exception as e:
    print(f"Exception: {e}")

# Test 3: Fichiers du projet 2
print("\n" + "=" * 50)
print("TEST 3: Fichiers du projet 2")
print("=" * 50)
try:
    response = requests.get("http://localhost:8000/api/projects/2/files")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Fichiers trouvés: {len(data.get('files', []))}")
        for f in data.get('files', [])[:5]:
            print(f"  - {f['name']} ({'dossier' if f.get('is_directory') else 'fichier'})")
    else:
        print(f"Erreur: {response.text[:200]}")
except Exception as e:
    print(f"Exception: {e}")
