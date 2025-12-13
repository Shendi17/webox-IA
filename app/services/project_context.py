"""
Service pour analyser et enrichir le contexte du projet
"""
import os
from pathlib import Path
from typing import Dict, List, Optional
import json


class ProjectAnalyzer:
    """Analyseur de projet pour enrichir le contexte IA"""
    
    # Extensions de fichiers à ignorer
    IGNORE_EXTENSIONS = {
        '.pyc', '.pyo', '.pyd', '.so', '.dll', '.dylib',
        '.exe', '.bin', '.dat', '.db', '.sqlite', '.sqlite3',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg',
        '.mp3', '.mp4', '.avi', '.mov', '.wav',
        '.zip', '.tar', '.gz', '.rar', '.7z',
        '.log', '.tmp', '.cache'
    }
    
    # Dossiers à ignorer
    IGNORE_DIRS = {
        '__pycache__', 'node_modules', '.git', '.venv', 'venv',
        'env', 'dist', 'build', '.next', '.nuxt', 'coverage',
        '.pytest_cache', '.mypy_cache', 'vendor', 'bower_components'
    }
    
    # Fichiers importants à toujours inclure
    IMPORTANT_FILES = {
        'package.json', 'requirements.txt', 'composer.json',
        'Gemfile', 'Cargo.toml', 'go.mod', 'pom.xml',
        'README.md', 'README.txt', '.env.example',
        'docker-compose.yml', 'Dockerfile', 'Makefile',
        'tsconfig.json', 'webpack.config.js', 'vite.config.js'
    }
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def analyze(self, max_files: int = 50, max_file_size: int = 50000) -> Dict:
        """
        Analyser le projet et générer un contexte enrichi
        
        Args:
            max_files: Nombre maximum de fichiers à analyser
            max_file_size: Taille maximale d'un fichier en octets
        
        Returns:
            Contexte enrichi du projet
        """
        context = {
            "structure": self.get_structure(),
            "technologies": self.detect_technologies(),
            "important_files": self.get_important_files(),
            "file_tree": self.get_file_tree(max_depth=3),
            "statistics": self.get_statistics(),
            "dependencies": self.get_dependencies()
        }
        
        return context
    
    def get_structure(self) -> Dict:
        """Obtenir la structure du projet"""
        structure = {
            "root": str(self.project_path),
            "directories": [],
            "files": []
        }
        
        try:
            for item in self.project_path.iterdir():
                if item.is_dir() and item.name not in self.IGNORE_DIRS:
                    structure["directories"].append(item.name)
                elif item.is_file():
                    structure["files"].append(item.name)
        except Exception as e:
            structure["error"] = str(e)
        
        return structure
    
    def detect_technologies(self) -> List[str]:
        """Détecter les technologies utilisées"""
        technologies = set()
        
        # Détecter via les fichiers de configuration
        tech_files = {
            'package.json': ['Node.js', 'npm'],
            'requirements.txt': ['Python', 'pip'],
            'composer.json': ['PHP', 'Composer'],
            'Gemfile': ['Ruby', 'Bundler'],
            'Cargo.toml': ['Rust', 'Cargo'],
            'go.mod': ['Go'],
            'pom.xml': ['Java', 'Maven'],
            'build.gradle': ['Java', 'Gradle'],
            'tsconfig.json': ['TypeScript'],
            'webpack.config.js': ['Webpack'],
            'vite.config.js': ['Vite'],
            'next.config.js': ['Next.js'],
            'nuxt.config.js': ['Nuxt.js'],
            'vue.config.js': ['Vue.js'],
            'angular.json': ['Angular'],
            'svelte.config.js': ['Svelte'],
            'tailwind.config.js': ['Tailwind CSS'],
            'docker-compose.yml': ['Docker'],
            'Dockerfile': ['Docker']
        }
        
        for file_name, techs in tech_files.items():
            if (self.project_path / file_name).exists():
                technologies.update(techs)
        
        # Détecter via package.json
        package_json = self.project_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                    
                    if 'react' in deps:
                        technologies.add('React')
                    if 'vue' in deps:
                        technologies.add('Vue.js')
                    if 'angular' in deps or '@angular/core' in deps:
                        technologies.add('Angular')
                    if 'svelte' in deps:
                        technologies.add('Svelte')
                    if 'express' in deps:
                        technologies.add('Express.js')
                    if 'fastify' in deps:
                        technologies.add('Fastify')
                    if 'next' in deps:
                        technologies.add('Next.js')
                    if 'nuxt' in deps:
                        technologies.add('Nuxt.js')
                    if 'tailwindcss' in deps:
                        technologies.add('Tailwind CSS')
                    if 'sass' in deps or 'node-sass' in deps:
                        technologies.add('SASS')
                    if 'typescript' in deps:
                        technologies.add('TypeScript')
            except:
                pass
        
        return sorted(list(technologies))
    
    def get_important_files(self, max_size: int = 50000) -> Dict[str, str]:
        """Lire le contenu des fichiers importants"""
        important_content = {}
        
        for file_name in self.IMPORTANT_FILES:
            file_path = self.project_path / file_name
            if file_path.exists() and file_path.stat().st_size < max_size:
                try:
                    content = file_path.read_text(encoding='utf-8')
                    important_content[file_name] = content
                except:
                    pass
        
        return important_content
    
    def get_file_tree(self, max_depth: int = 3) -> Dict:
        """Générer un arbre des fichiers"""
        def build_tree(path: Path, current_depth: int = 0) -> Dict:
            if current_depth >= max_depth:
                return {}
            
            tree = {}
            
            try:
                for item in sorted(path.iterdir()):
                    if item.name.startswith('.') and item.name not in {'.env.example', '.gitignore'}:
                        continue
                    
                    if item.is_dir():
                        if item.name not in self.IGNORE_DIRS:
                            tree[item.name + '/'] = build_tree(item, current_depth + 1)
                    else:
                        if item.suffix not in self.IGNORE_EXTENSIONS:
                            tree[item.name] = None
            except:
                pass
            
            return tree
        
        return build_tree(self.project_path)
    
    def get_statistics(self) -> Dict:
        """Obtenir des statistiques sur le projet"""
        stats = {
            "total_files": 0,
            "total_directories": 0,
            "total_lines": 0,
            "file_types": {}
        }
        
        try:
            for root, dirs, files in os.walk(self.project_path):
                # Filtrer les dossiers ignorés
                dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]
                
                stats["total_directories"] += len(dirs)
                
                for file in files:
                    file_path = Path(root) / file
                    
                    if file_path.suffix in self.IGNORE_EXTENSIONS:
                        continue
                    
                    stats["total_files"] += 1
                    
                    # Compter par type
                    ext = file_path.suffix or 'no_extension'
                    stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1
                    
                    # Compter les lignes pour les fichiers texte
                    if file_path.suffix in {'.py', '.js', '.jsx', '.ts', '.tsx', '.vue', '.html', '.css', '.scss'}:
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                stats["total_lines"] += sum(1 for _ in f)
                        except:
                            pass
        except:
            pass
        
        return stats
    
    def get_dependencies(self) -> Dict:
        """Extraire les dépendances du projet"""
        dependencies = {}
        
        # Node.js
        package_json = self.project_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    dependencies['npm'] = {
                        'dependencies': data.get('dependencies', {}),
                        'devDependencies': data.get('devDependencies', {})
                    }
            except:
                pass
        
        # Python
        requirements = self.project_path / 'requirements.txt'
        if requirements.exists():
            try:
                content = requirements.read_text(encoding='utf-8')
                deps = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
                dependencies['pip'] = deps
            except:
                pass
        
        return dependencies
    
    def get_relevant_files(self, query: str, max_files: int = 5) -> List[Dict]:
        """
        Trouver les fichiers pertinents pour une requête
        
        Args:
            query: Requête de l'utilisateur
            max_files: Nombre maximum de fichiers à retourner
        
        Returns:
            Liste des fichiers pertinents avec leur contenu
        """
        relevant_files = []
        query_lower = query.lower()
        
        # Mots-clés pour détecter les types de fichiers recherchés
        keywords = {
            'component': ['.jsx', '.tsx', '.vue', '.svelte'],
            'style': ['.css', '.scss', '.sass', '.less'],
            'config': ['config.js', 'config.json', '.config.js'],
            'route': ['route', 'router', 'routes'],
            'api': ['api', 'endpoint', 'controller'],
            'model': ['model', 'schema', 'entity'],
            'test': ['test', 'spec', '.test.', '.spec.'],
            'util': ['util', 'helper', 'lib'],
        }
        
        # Détecter le type de fichier recherché
        target_extensions = set()
        target_patterns = []
        
        for keyword, patterns in keywords.items():
            if keyword in query_lower:
                for pattern in patterns:
                    if pattern.startswith('.'):
                        target_extensions.add(pattern)
                    else:
                        target_patterns.append(pattern)
        
        # Si aucun pattern détecté, chercher dans tous les fichiers de code
        if not target_extensions and not target_patterns:
            target_extensions = {'.js', '.jsx', '.ts', '.tsx', '.py', '.vue', '.html', '.css'}
        
        try:
            for root, dirs, files in os.walk(self.project_path):
                dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]
                
                for file in files:
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(self.project_path)
                    
                    # Vérifier l'extension
                    if target_extensions and file_path.suffix not in target_extensions:
                        continue
                    
                    # Vérifier les patterns
                    if target_patterns:
                        if not any(pattern in str(relative_path).lower() for pattern in target_patterns):
                            continue
                    
                    # Lire le contenu
                    try:
                        if file_path.stat().st_size > 100000:  # Ignorer les gros fichiers
                            continue
                        
                        content = file_path.read_text(encoding='utf-8')
                        
                        relevant_files.append({
                            'path': str(relative_path),
                            'name': file,
                            'content': content,
                            'lines': len(content.split('\n'))
                        })
                        
                        if len(relevant_files) >= max_files:
                            break
                    except:
                        pass
                
                if len(relevant_files) >= max_files:
                    break
        except:
            pass
        
        return relevant_files


def build_context_prompt(project_context: Dict, user_query: str = "") -> str:
    """
    Construire un prompt enrichi avec le contexte du projet
    
    Args:
        project_context: Contexte du projet analysé
        user_query: Requête de l'utilisateur (optionnel)
    
    Returns:
        Prompt enrichi
    """
    prompt_parts = []
    
    # Structure du projet
    if 'structure' in project_context:
        structure = project_context['structure']
        prompt_parts.append(f"📁 **Structure du projet** :")
        prompt_parts.append(f"- Racine : {structure.get('root', 'N/A')}")
        prompt_parts.append(f"- Dossiers : {', '.join(structure.get('directories', [])[:10])}")
        prompt_parts.append(f"- Fichiers racine : {', '.join(structure.get('files', [])[:10])}")
    
    # Technologies
    if 'technologies' in project_context and project_context['technologies']:
        prompt_parts.append(f"\n🔧 **Technologies** : {', '.join(project_context['technologies'])}")
    
    # Statistiques
    if 'statistics' in project_context:
        stats = project_context['statistics']
        prompt_parts.append(f"\n📊 **Statistiques** :")
        prompt_parts.append(f"- Fichiers : {stats.get('total_files', 0)}")
        prompt_parts.append(f"- Lignes de code : {stats.get('total_lines', 0)}")
    
    # Fichiers importants
    if 'important_files' in project_context:
        for file_name, content in project_context['important_files'].items():
            if len(content) < 1000:  # Inclure seulement les petits fichiers
                prompt_parts.append(f"\n📄 **{file_name}** :")
                prompt_parts.append(f"```\n{content[:500]}\n```")
    
    return "\n".join(prompt_parts)
