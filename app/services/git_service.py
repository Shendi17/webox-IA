"""
Service pour gérer les opérations Git
"""
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class GitService:
    """Service pour les opérations Git"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
    
    def _run_command(self, command: List[str]) -> Tuple[bool, str, str]:
        """
        Exécuter une commande Git
        
        Returns:
            Tuple (success, stdout, stderr)
        """
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Timeout: La commande a pris trop de temps"
        except Exception as e:
            return False, "", str(e)
    
    def is_git_repo(self) -> bool:
        """Vérifier si c'est un dépôt Git"""
        git_dir = self.repo_path / '.git'
        return git_dir.exists() and git_dir.is_dir()
    
    def init(self) -> Dict:
        """Initialiser un dépôt Git"""
        if self.is_git_repo():
            return {"success": False, "error": "Dépôt Git déjà initialisé"}
        
        success, stdout, stderr = self._run_command(['git', 'init'])
        
        if success:
            # Configurer le nom et l'email par défaut
            self._run_command(['git', 'config', 'user.name', 'WeBox User'])
            self._run_command(['git', 'config', 'user.email', 'user@webox.local'])
            
            return {"success": True, "message": "Dépôt Git initialisé"}
        else:
            return {"success": False, "error": stderr}
    
    def status(self) -> Dict:
        """Obtenir le statut Git"""
        if not self.is_git_repo():
            return {"success": False, "error": "Pas un dépôt Git"}
        
        success, stdout, stderr = self._run_command(['git', 'status', '--porcelain'])
        
        if not success:
            return {"success": False, "error": stderr}
        
        # Parser le statut
        files = {
            "modified": [],
            "added": [],
            "deleted": [],
            "untracked": []
        }
        
        for line in stdout.strip().split('\n'):
            if not line:
                continue
            
            status_code = line[:2]
            file_path = line[3:]
            
            if status_code == '??':
                files["untracked"].append(file_path)
            elif 'M' in status_code:
                files["modified"].append(file_path)
            elif 'A' in status_code:
                files["added"].append(file_path)
            elif 'D' in status_code:
                files["deleted"].append(file_path)
        
        # Obtenir la branche actuelle
        success_branch, branch, _ = self._run_command(['git', 'branch', '--show-current'])
        current_branch = branch.strip() if success_branch else "main"
        
        return {
            "success": True,
            "branch": current_branch,
            "files": files,
            "has_changes": any(files.values())
        }
    
    def add(self, files: List[str] = None) -> Dict:
        """Ajouter des fichiers au staging"""
        if not self.is_git_repo():
            return {"success": False, "error": "Pas un dépôt Git"}
        
        if files is None or len(files) == 0:
            # Ajouter tous les fichiers
            command = ['git', 'add', '.']
        else:
            command = ['git', 'add'] + files
        
        success, stdout, stderr = self._run_command(command)
        
        if success:
            return {"success": True, "message": f"{len(files) if files else 'Tous les'} fichier(s) ajouté(s)"}
        else:
            return {"success": False, "error": stderr}
    
    def commit(self, message: str, author_name: str = None, author_email: str = None) -> Dict:
        """Créer un commit"""
        if not self.is_git_repo():
            return {"success": False, "error": "Pas un dépôt Git"}
        
        if not message:
            return {"success": False, "error": "Message de commit requis"}
        
        # Configurer l'auteur si fourni
        if author_name:
            self._run_command(['git', 'config', 'user.name', author_name])
        if author_email:
            self._run_command(['git', 'config', 'user.email', author_email])
        
        success, stdout, stderr = self._run_command(['git', 'commit', '-m', message])
        
        if success:
            return {"success": True, "message": "Commit créé", "output": stdout}
        else:
            return {"success": False, "error": stderr}
    
    def push(self, remote: str = "origin", branch: str = None) -> Dict:
        """Pousser vers le dépôt distant"""
        if not self.is_git_repo():
            return {"success": False, "error": "Pas un dépôt Git"}
        
        if branch is None:
            # Obtenir la branche actuelle
            success_branch, current_branch, _ = self._run_command(['git', 'branch', '--show-current'])
            branch = current_branch.strip() if success_branch else "main"
        
        success, stdout, stderr = self._run_command(['git', 'push', remote, branch])
        
        if success:
            return {"success": True, "message": f"Poussé vers {remote}/{branch}"}
        else:
            return {"success": False, "error": stderr}
    
    def pull(self, remote: str = "origin", branch: str = None) -> Dict:
        """Tirer depuis le dépôt distant"""
        if not self.is_git_repo():
            return {"success": False, "error": "Pas un dépôt Git"}
        
        if branch is None:
            success_branch, current_branch, _ = self._run_command(['git', 'branch', '--show-current'])
            branch = current_branch.strip() if success_branch else "main"
        
        success, stdout, stderr = self._run_command(['git', 'pull', remote, branch])
        
        if success:
            return {"success": True, "message": f"Tiré depuis {remote}/{branch}", "output": stdout}
        else:
            return {"success": False, "error": stderr}
    
    def branches(self) -> Dict:
        """Lister les branches"""
        if not self.is_git_repo():
            return {"success": False, "error": "Pas un dépôt Git"}
        
        success, stdout, stderr = self._run_command(['git', 'branch', '-a'])
        
        if not success:
            return {"success": False, "error": stderr}
        
        branches = []
        current_branch = None
        
        for line in stdout.strip().split('\n'):
            if not line:
                continue
            
            is_current = line.startswith('*')
            branch_name = line.replace('*', '').strip()
            
            if is_current:
                current_branch = branch_name
            
            branches.append({
                "name": branch_name,
                "current": is_current,
                "remote": branch_name.startswith('remotes/')
            })
        
        return {
            "success": True,
            "branches": branches,
            "current": current_branch
        }
    
    def create_branch(self, branch_name: str, checkout: bool = True) -> Dict:
        """Créer une nouvelle branche"""
        if not self.is_git_repo():
            return {"success": False, "error": "Pas un dépôt Git"}
        
        if checkout:
            command = ['git', 'checkout', '-b', branch_name]
        else:
            command = ['git', 'branch', branch_name]
        
        success, stdout, stderr = self._run_command(command)
        
        if success:
            return {"success": True, "message": f"Branche '{branch_name}' créée"}
        else:
            return {"success": False, "error": stderr}
    
    def checkout(self, branch_name: str) -> Dict:
        """Changer de branche"""
        if not self.is_git_repo():
            return {"success": False, "error": "Pas un dépôt Git"}
        
        success, stdout, stderr = self._run_command(['git', 'checkout', branch_name])
        
        if success:
            return {"success": True, "message": f"Basculé sur '{branch_name}'"}
        else:
            return {"success": False, "error": stderr}
    
    def log(self, limit: int = 20) -> Dict:
        """Obtenir l'historique des commits"""
        if not self.is_git_repo():
            return {"success": False, "error": "Pas un dépôt Git"}
        
        format_string = '%H|%an|%ae|%at|%s'
        success, stdout, stderr = self._run_command([
            'git', 'log', f'--max-count={limit}', f'--format={format_string}'
        ])
        
        if not success:
            return {"success": False, "error": stderr}
        
        commits = []
        for line in stdout.strip().split('\n'):
            if not line:
                continue
            
            parts = line.split('|')
            if len(parts) == 5:
                commits.append({
                    "hash": parts[0],
                    "author_name": parts[1],
                    "author_email": parts[2],
                    "timestamp": int(parts[3]),
                    "message": parts[4]
                })
        
        return {
            "success": True,
            "commits": commits
        }
    
    def diff(self, file_path: str = None) -> Dict:
        """Obtenir les différences"""
        if not self.is_git_repo():
            return {"success": False, "error": "Pas un dépôt Git"}
        
        command = ['git', 'diff']
        if file_path:
            command.append(file_path)
        
        success, stdout, stderr = self._run_command(command)
        
        if success:
            return {"success": True, "diff": stdout}
        else:
            return {"success": False, "error": stderr}
    
    def clone(self, url: str, destination: str = None) -> Dict:
        """Cloner un dépôt"""
        command = ['git', 'clone', url]
        if destination:
            command.append(destination)
        
        success, stdout, stderr = self._run_command(command)
        
        if success:
            return {"success": True, "message": "Dépôt cloné"}
        else:
            return {"success": False, "error": stderr}
    
    def remote_add(self, name: str, url: str) -> Dict:
        """Ajouter un dépôt distant"""
        if not self.is_git_repo():
            return {"success": False, "error": "Pas un dépôt Git"}
        
        success, stdout, stderr = self._run_command(['git', 'remote', 'add', name, url])
        
        if success:
            return {"success": True, "message": f"Remote '{name}' ajouté"}
        else:
            return {"success": False, "error": stderr}
    
    def remotes(self) -> Dict:
        """Lister les dépôts distants"""
        if not self.is_git_repo():
            return {"success": False, "error": "Pas un dépôt Git"}
        
        success, stdout, stderr = self._run_command(['git', 'remote', '-v'])
        
        if not success:
            return {"success": False, "error": stderr}
        
        remotes = {}
        for line in stdout.strip().split('\n'):
            if not line:
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                url = parts[1]
                if name not in remotes:
                    remotes[name] = url
        
        return {
            "success": True,
            "remotes": remotes
        }
    
    def generate_commit_message(self, changes: Dict) -> str:
        """Générer un message de commit intelligent"""
        # Simple génération basée sur les changements
        files = changes.get("files", {})
        
        modified = len(files.get("modified", []))
        added = len(files.get("added", []))
        deleted = len(files.get("deleted", []))
        
        parts = []
        if added > 0:
            parts.append(f"Add {added} file(s)")
        if modified > 0:
            parts.append(f"Update {modified} file(s)")
        if deleted > 0:
            parts.append(f"Delete {deleted} file(s)")
        
        if not parts:
            return "Update project"
        
        return " | ".join(parts)
