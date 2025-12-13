"""Fonctionnalités de collaboration et partage"""
import json
import os
from datetime import datetime
from typing import Dict, List
import base64


class CollaborationManager:
    """Gestionnaire de collaboration et partage"""
    
    def __init__(self, export_dir="exports"):
        self.export_dir = export_dir
        os.makedirs(export_dir, exist_ok=True)
    
    def export_conversation(self, messages: List[Dict], title: str, format: str = "json") -> str:
        """Exporte une conversation dans différents formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{title}_{timestamp}"
        
        if format == "json":
            return self._export_json(messages, filename)
        elif format == "markdown":
            return self._export_markdown(messages, filename, title)
        elif format == "html":
            return self._export_html(messages, filename, title)
        elif format == "txt":
            return self._export_txt(messages, filename)
        
        return None
    
    def _export_json(self, messages: List[Dict], filename: str) -> str:
        """Exporte en JSON"""
        filepath = os.path.join(self.export_dir, f"{filename}.json")
        
        data = {
            "export_date": datetime.now().isoformat(),
            "messages": messages,
            "version": "1.0"
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def _export_markdown(self, messages: List[Dict], filename: str, title: str) -> str:
        """Exporte en Markdown"""
        filepath = os.path.join(self.export_dir, f"{filename}.md")
        
        md_content = f"# {title}\n\n"
        md_content += f"*Exporté le {datetime.now().strftime('%d/%m/%Y à %H:%M')}*\n\n"
        md_content += "---\n\n"
        
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            
            if role == "user":
                md_content += f"## 👤 Utilisateur\n\n{content}\n\n"
            elif role == "assistant":
                md_content += f"## 🤖 Assistant\n\n"
                if isinstance(content, dict):
                    for provider, response in content.items():
                        md_content += f"### {provider}\n\n{response}\n\n"
                else:
                    md_content += f"{content}\n\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return filepath
    
    def _export_html(self, messages: List[Dict], filename: str, title: str) -> str:
        """Exporte en HTML"""
        filepath = os.path.join(self.export_dir, f"{filename}.html")
        
        html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }}
        .message {{
            background: white;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .user {{
            border-left: 4px solid #667eea;
        }}
        .assistant {{
            border-left: 4px solid #764ba2;
        }}
        .role {{
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: #667eea;
        }}
        .provider {{
            font-weight: bold;
            color: #764ba2;
            margin-top: 1rem;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p class="timestamp">Exporté le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
    </div>
"""
        
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            
            if role == "user":
                html_content += f"""
    <div class="message user">
        <div class="role">👤 Utilisateur</div>
        <div>{content}</div>
    </div>
"""
            elif role == "assistant":
                html_content += f"""
    <div class="message assistant">
        <div class="role">🤖 Assistant</div>
"""
                if isinstance(content, dict):
                    for provider, response in content.items():
                        html_content += f"""
        <div class="provider">{provider}</div>
        <div>{response}</div>
"""
                else:
                    html_content += f"""
        <div>{content}</div>
"""
                html_content += """
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def _export_txt(self, messages: List[Dict], filename: str) -> str:
        """Exporte en TXT"""
        filepath = os.path.join(self.export_dir, f"{filename}.txt")
        
        txt_content = f"Conversation - {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n"
        txt_content += "=" * 80 + "\n\n"
        
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            
            if role == "user":
                txt_content += f"UTILISATEUR:\n{content}\n\n"
            elif role == "assistant":
                txt_content += f"ASSISTANT:\n"
                if isinstance(content, dict):
                    for provider, response in content.items():
                        txt_content += f"\n[{provider}]\n{response}\n"
                else:
                    txt_content += f"{content}\n"
                txt_content += "\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        
        return filepath
    
    def generate_share_link(self, conversation_data: Dict) -> str:
        """Génère un lien de partage (encodé en base64)"""
        json_str = json.dumps(conversation_data, ensure_ascii=False)
        encoded = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        return f"webox://share/{encoded}"
    
    def decode_share_link(self, share_link: str) -> Dict:
        """Décode un lien de partage"""
        if share_link.startswith("webox://share/"):
            encoded = share_link.replace("webox://share/", "")
            decoded = base64.b64decode(encoded.encode('utf-8')).decode('utf-8')
            return json.loads(decoded)
        return None


# Instance globale
collaboration_manager = CollaborationManager()
