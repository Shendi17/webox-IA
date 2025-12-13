"""Test de l'API sur le port 8001"""
import requests

# Test fichiers du projet 1
print("=" * 50)
print("TEST: Fichiers du projet 1 (port 8001)")
print("=" * 50)
try:
    response = requests.get("http://localhost:8001/api/projects/1/files")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Fichiers trouvés: {len(data.get('files', []))}")
        for f in data.get('files', [])[:10]:
            icon = "📁" if f.get('is_directory') else "📄"
            print(f"  {icon} {f['name']}")
            if f.get('children'):
                for child in f['children'][:3]:
                    icon2 = "📁" if child.get('is_directory') else "📄"
                    print(f"     {icon2} {child['name']}")
    else:
        print(f"❌ Erreur: {response.text[:200]}")
except Exception as e:
    print(f"❌ Exception: {e}")

# Test fichiers du projet 2
print("\n" + "=" * 50)
print("TEST: Fichiers du projet 2 (port 8001)")
print("=" * 50)
try:
    response = requests.get("http://localhost:8001/api/projects/2/files")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Fichiers trouvés: {len(data.get('files', []))}")
        for f in data.get('files', [])[:10]:
            icon = "📁" if f.get('is_directory') else "📄"
            print(f"  {icon} {f['name']}")
    else:
        print(f"❌ Erreur: {response.text[:200]}")
except Exception as e:
    print(f"❌ Exception: {e}")
