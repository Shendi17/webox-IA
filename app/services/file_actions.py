"""
Service pour gérer les actions sur les fichiers (créer, modifier, supprimer)
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json


class FileActionParser:
    """Parser pour extraire les actions des réponses IA"""
    
    @staticmethod
    def parse_actions(ai_response: str) -> List[Dict]:
        """
        Parse les actions depuis la réponse de l'IA
        
        Format attendu : [ACTION:type:data]
        Exemples :
        - [ACTION:CREATE_FILE:path/to/file.js]
        - [ACTION:MODIFY_FILE:path/to/file.js]
        - [ACTION:DELETE_FILE:path/to/file.js]
        """
        actions = []
        
        # Pattern pour les actions explicites
        action_pattern = r'\[ACTION:(\w+):([^\]]+)\]'
        matches = re.findall(action_pattern, ai_response)
        
        for action_type, action_data in matches:
            actions.append({
                "type": action_type,
                "data": action_data.strip()
            })
        
        # Détecter les blocs de code qui pourraient être des fichiers à créer
        code_blocks = FileActionParser.extract_code_blocks(ai_response)
        
        for code_block in code_blocks:
            # Si un nom de fichier est mentionné avant le bloc de code
            file_match = re.search(
                r'(?:créer?|créé|créons|fichier|file)\s+[`"]?([a-zA-Z0-9_\-./]+\.[a-zA-Z0-9]+)[`"]?',
                ai_response[:ai_response.find(code_block['raw'])],
                re.IGNORECASE
            )
            
            if file_match:
                actions.append({
                    "type": "CREATE_FILE",
                    "data": file_match.group(1),
                    "content": code_block['code'],
                    "language": code_block['language']
                })
        
        return actions
    
    @staticmethod
    def extract_code_blocks(text: str) -> List[Dict]:
        """Extraire les blocs de code de la réponse"""
        code_blocks = []
        
        # Pattern pour les blocs de code avec langue
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.finditer(pattern, text, re.DOTALL)
        
        for match in matches:
            language = match.group(1) or 'text'
            code = match.group(2).strip()
            
            code_blocks.append({
                "language": language,
                "code": code,
                "raw": match.group(0)
            })
        
        return code_blocks


class FileActionExecutor:
    """Exécuteur d'actions sur les fichiers"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def create_file(self, relative_path: str, content: str) -> Dict:
        """
        Créer un fichier
        
        Args:
            relative_path: Chemin relatif du fichier
            content: Contenu du fichier
        
        Returns:
            Résultat de l'action
        """
        try:
            file_path = self.project_path / relative_path
            
            # Créer les dossiers parents si nécessaire
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Vérifier si le fichier existe déjà
            if file_path.exists():
                return {
                    "success": False,
                    "error": "Le fichier existe déjà",
                    "path": str(file_path)
                }
            
            # Créer le fichier
            file_path.write_text(content, encoding='utf-8')
            
            return {
                "success": True,
                "path": str(file_path),
                "relative_path": relative_path,
                "message": f"Fichier créé : {relative_path}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": relative_path
            }
    
    def modify_file(self, relative_path: str, content: str) -> Dict:
        """
        Modifier un fichier
        
        Args:
            relative_path: Chemin relatif du fichier
            content: Nouveau contenu du fichier
        
        Returns:
            Résultat de l'action
        """
        try:
            file_path = self.project_path / relative_path
            
            # Vérifier si le fichier existe
            if not file_path.exists():
                return {
                    "success": False,
                    "error": "Le fichier n'existe pas",
                    "path": str(file_path)
                }
            
            # Sauvegarder l'ancien contenu (backup)
            old_content = file_path.read_text(encoding='utf-8')
            
            # Modifier le fichier
            file_path.write_text(content, encoding='utf-8')
            
            return {
                "success": True,
                "path": str(file_path),
                "relative_path": relative_path,
                "message": f"Fichier modifié : {relative_path}",
                "old_content": old_content
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": relative_path
            }
    
    def delete_file(self, relative_path: str) -> Dict:
        """
        Supprimer un fichier
        
        Args:
            relative_path: Chemin relatif du fichier
        
        Returns:
            Résultat de l'action
        """
        try:
            file_path = self.project_path / relative_path
            
            # Vérifier si le fichier existe
            if not file_path.exists():
                return {
                    "success": False,
                    "error": "Le fichier n'existe pas",
                    "path": str(file_path)
                }
            
            # Sauvegarder le contenu avant suppression
            content = file_path.read_text(encoding='utf-8')
            
            # Supprimer le fichier
            file_path.unlink()
            
            return {
                "success": True,
                "path": str(file_path),
                "relative_path": relative_path,
                "message": f"Fichier supprimé : {relative_path}",
                "deleted_content": content
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": relative_path
            }
    
    def execute_action(self, action: Dict) -> Dict:
        """
        Exécuter une action
        
        Args:
            action: Action à exécuter
        
        Returns:
            Résultat de l'action
        """
        action_type = action.get("type")
        
        if action_type == "CREATE_FILE":
            return self.create_file(
                action.get("data"),
                action.get("content", "")
            )
        
        elif action_type == "MODIFY_FILE":
            return self.modify_file(
                action.get("data"),
                action.get("content", "")
            )
        
        elif action_type == "DELETE_FILE":
            return self.delete_file(action.get("data"))
        
        else:
            return {
                "success": False,
                "error": f"Type d'action inconnu : {action_type}"
            }
    
    def execute_actions(self, actions: List[Dict]) -> List[Dict]:
        """
        Exécuter plusieurs actions
        
        Args:
            actions: Liste des actions à exécuter
        
        Returns:
            Liste des résultats
        """
        results = []
        
        for action in actions:
            result = self.execute_action(action)
            results.append(result)
        
        return results


def process_ai_response(ai_response: str, project_path: str) -> Tuple[str, List[Dict]]:
    """
    Traiter la réponse de l'IA et exécuter les actions
    
    Args:
        ai_response: Réponse de l'IA
        project_path: Chemin du projet
    
    Returns:
        Tuple (réponse nettoyée, résultats des actions)
    """
    # Parser les actions
    parser = FileActionParser()
    actions = parser.parse_actions(ai_response)
    
    # Exécuter les actions
    executor = FileActionExecutor(project_path)
    results = executor.execute_actions(actions)
    
    # Nettoyer la réponse (enlever les tags d'action)
    cleaned_response = re.sub(r'\[ACTION:\w+:[^\]]+\]', '', ai_response)
    
    return cleaned_response, results
