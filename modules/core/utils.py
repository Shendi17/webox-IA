"""Fonctions utilitaires pour WeBox Multi-IA"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any


class ConversationManager:
    """Gestionnaire de conversations et historique"""
    
    def __init__(self, storage_path: str = "data/conversations"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
    
    def save_conversation(self, conv_id: str, messages: List[Dict], metadata: Dict = None):
        """Sauvegarde une conversation"""
        data = {
            "id": conv_id,
            "messages": messages,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        
        filepath = os.path.join(self.storage_path, f"{conv_id}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_conversation(self, conv_id: str) -> Dict:
        """Charge une conversation"""
        filepath = os.path.join(self.storage_path, f"{conv_id}.json")
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def list_conversations(self) -> List[str]:
        """Liste toutes les conversations"""
        if not os.path.exists(self.storage_path):
            return []
        
        return [
            f.replace('.json', '') 
            for f in os.listdir(self.storage_path) 
            if f.endswith('.json')
        ]
    
    def delete_conversation(self, conv_id: str):
        """Supprime une conversation"""
        filepath = os.path.join(self.storage_path, f"{conv_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)


class PromptBuilder:
    """Constructeur de prompts avancés"""
    
    @staticmethod
    def build_system_prompt(role: str, context: str = "", constraints: List[str] = None) -> str:
        """Construit un system prompt structuré"""
        prompt = f"Tu es {role}.\n\n"
        
        if context:
            prompt += f"Contexte: {context}\n\n"
        
        if constraints:
            prompt += "Contraintes:\n"
            for constraint in constraints:
                prompt += f"- {constraint}\n"
        
        return prompt.strip()
    
    @staticmethod
    def build_few_shot_prompt(task: str, examples: List[Dict[str, str]]) -> str:
        """Construit un prompt few-shot avec exemples"""
        prompt = f"Tâche: {task}\n\nExemples:\n\n"
        
        for i, example in enumerate(examples, 1):
            prompt += f"Exemple {i}:\n"
            prompt += f"Input: {example['input']}\n"
            prompt += f"Output: {example['output']}\n\n"
        
        prompt += "Maintenant, à ton tour:\n"
        return prompt
    
    @staticmethod
    def build_chain_of_thought_prompt(question: str) -> str:
        """Construit un prompt avec raisonnement étape par étape"""
        return f"""{question}

Réponds en suivant ces étapes:
1. Analyse du problème
2. Identification des éléments clés
3. Raisonnement étape par étape
4. Conclusion et réponse finale

Détaille ton raisonnement à chaque étape."""


class ResponseAnalyzer:
    """Analyseur de réponses IA"""
    
    @staticmethod
    def compare_responses(responses: Dict[str, str]) -> Dict[str, Any]:
        """Compare plusieurs réponses d'IA"""
        analysis = {
            "count": len(responses),
            "providers": list(responses.keys()),
            "lengths": {provider: len(response) for provider, response in responses.items()},
            "average_length": sum(len(r) for r in responses.values()) / len(responses) if responses else 0
        }
        
        return analysis
    
    @staticmethod
    def extract_key_points(text: str, max_points: int = 5) -> List[str]:
        """Extrait les points clés d'un texte"""
        # Simple extraction basée sur les phrases
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        return sentences[:max_points]
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """Calcule une similarité simple entre deux textes"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0


class ExportManager:
    """Gestionnaire d'export de conversations"""
    
    @staticmethod
    def export_to_markdown(messages: List[Dict], title: str = "Conversation") -> str:
        """Exporte une conversation en Markdown"""
        md = f"# {title}\n\n"
        md += f"*Exporté le {datetime.now().strftime('%d/%m/%Y à %H:%M')}*\n\n"
        md += "---\n\n"
        
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            
            if role == "user":
                md += f"## 👤 Utilisateur\n\n{content}\n\n"
            elif role == "assistant":
                md += f"## 🤖 Assistant\n\n"
                if isinstance(content, dict):
                    for provider, response in content.items():
                        md += f"### {provider}\n\n{response}\n\n"
                else:
                    md += f"{content}\n\n"
            elif role == "system":
                md += f"*System: {content}*\n\n"
        
        return md
    
    @staticmethod
    def export_to_json(messages: List[Dict], metadata: Dict = None) -> str:
        """Exporte une conversation en JSON"""
        data = {
            "messages": messages,
            "metadata": metadata or {},
            "exported_at": datetime.now().isoformat()
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    @staticmethod
    def export_to_txt(messages: List[Dict]) -> str:
        """Exporte une conversation en texte simple"""
        txt = f"Conversation - {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n"
        txt += "=" * 50 + "\n\n"
        
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            
            if role == "user":
                txt += f"UTILISATEUR:\n{content}\n\n"
            elif role == "assistant":
                txt += f"ASSISTANT:\n"
                if isinstance(content, dict):
                    for provider, response in content.items():
                        txt += f"\n[{provider}]\n{response}\n"
                else:
                    txt += f"{content}\n"
                txt += "\n"
        
        return txt


# Instances globales
conversation_manager = ConversationManager()
prompt_builder = PromptBuilder()
response_analyzer = ResponseAnalyzer()
export_manager = ExportManager()
