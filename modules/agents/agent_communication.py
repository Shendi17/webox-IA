"""Système de communication et collaboration entre agents IA"""
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from modules.agents.ai_agent_framework import agent_orchestrator, AgentTask


@dataclass
class AgentMessage:
    """Message entre agents"""
    message_id: str
    from_agent: str
    to_agent: str
    subject: str
    content: str
    timestamp: str
    priority: int = 3
    requires_response: bool = False
    response_to: Optional[str] = None


class AgentCommunicationHub:
    """Hub de communication entre agents"""
    
    def __init__(self):
        """Initialise le hub de communication"""
        self.messages: List[AgentMessage] = []
        self.conversations: Dict[str, List[AgentMessage]] = {}
    
    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        subject: str,
        content: str,
        priority: int = 3,
        requires_response: bool = False,
        response_to: Optional[str] = None
    ) -> AgentMessage:
        """
        Envoie un message d'un agent à un autre
        
        Args:
            from_agent: ID de l'agent émetteur
            to_agent: ID de l'agent destinataire
            subject: Sujet du message
            content: Contenu du message
            priority: Priorité (1-5)
            requires_response: Si une réponse est requise
            response_to: ID du message auquel on répond
            
        Returns:
            Message créé
        """
        message_id = f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        message = AgentMessage(
            message_id=message_id,
            from_agent=from_agent,
            to_agent=to_agent,
            subject=subject,
            content=content,
            timestamp=datetime.now().isoformat(),
            priority=priority,
            requires_response=requires_response,
            response_to=response_to
        )
        
        self.messages.append(message)
        
        # Créer ou mettre à jour la conversation
        conv_key = f"{from_agent}_{to_agent}"
        if conv_key not in self.conversations:
            self.conversations[conv_key] = []
        self.conversations[conv_key].append(message)
        
        return message
    
    def get_messages_for_agent(self, agent_id: str) -> List[AgentMessage]:
        """Récupère tous les messages pour un agent"""
        return [msg for msg in self.messages if msg.to_agent == agent_id]
    
    def get_unread_messages(self, agent_id: str) -> List[AgentMessage]:
        """Récupère les messages non lus pour un agent"""
        # Pour simplifier, on considère tous les messages récents comme non lus
        return self.get_messages_for_agent(agent_id)
    
    def get_conversation(self, agent1: str, agent2: str) -> List[AgentMessage]:
        """Récupère la conversation entre deux agents"""
        conv_key1 = f"{agent1}_{agent2}"
        conv_key2 = f"{agent2}_{agent1}"
        
        messages = []
        if conv_key1 in self.conversations:
            messages.extend(self.conversations[conv_key1])
        if conv_key2 in self.conversations:
            messages.extend(self.conversations[conv_key2])
        
        # Trier par timestamp
        messages.sort(key=lambda m: m.timestamp)
        return messages


class AgentCollaborationManager:
    """Gestionnaire de collaboration entre agents"""
    
    def __init__(self):
        """Initialise le gestionnaire de collaboration"""
        self.communication_hub = AgentCommunicationHub()
        self.collaboration_sessions: Dict[str, Dict] = {}
    
    async def create_collaboration_task(
        self,
        task_description: str,
        involved_agents: List[str],
        coordinator_agent: str
    ) -> Dict[str, Any]:
        """
        Crée une tâche collaborative impliquant plusieurs agents
        
        Args:
            task_description: Description de la tâche globale
            involved_agents: Liste des IDs des agents impliqués
            coordinator_agent: Agent coordinateur
            
        Returns:
            Résultat de la collaboration
        """
        session_id = f"collab_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Créer la session de collaboration
        self.collaboration_sessions[session_id] = {
            'session_id': session_id,
            'task_description': task_description,
            'involved_agents': involved_agents,
            'coordinator': coordinator_agent,
            'status': 'in_progress',
            'start_time': datetime.now().isoformat(),
            'results': {}
        }
        
        # Décomposer la tâche pour chaque agent
        subtasks = await self._decompose_task(
            task_description,
            involved_agents,
            coordinator_agent
        )
        
        # Créer les tâches pour chaque agent
        task_results = {}
        for agent_id, subtask_desc in subtasks.items():
            task = agent_orchestrator.create_task(
                agent_id=agent_id,
                description=subtask_desc,
                priority=4
            )
            
            # Exécuter la tâche
            agent = agent_orchestrator.agents.get(agent_id)
            if agent:
                result = await agent.execute_task(task)
                task_results[agent_id] = result
        
        # Synthétiser les résultats
        synthesis = await self._synthesize_results(
            task_description,
            task_results,
            coordinator_agent
        )
        
        # Mettre à jour la session
        self.collaboration_sessions[session_id]['status'] = 'completed'
        self.collaboration_sessions[session_id]['end_time'] = datetime.now().isoformat()
        self.collaboration_sessions[session_id]['results'] = task_results
        self.collaboration_sessions[session_id]['synthesis'] = synthesis
        
        return {
            'session_id': session_id,
            'success': True,
            'synthesis': synthesis,
            'individual_results': task_results
        }
    
    async def _decompose_task(
        self,
        task_description: str,
        involved_agents: List[str],
        coordinator_agent: str
    ) -> Dict[str, str]:
        """Décompose une tâche en sous-tâches pour chaque agent"""
        from modules.core.ai_providers import ai_manager
        
        # Obtenir les domaines des agents
        agent_domains = {}
        for agent_id in involved_agents:
            agent = agent_orchestrator.agents.get(agent_id)
            if agent:
                agent_domains[agent_id] = agent.config.domain
        
        # Demander à l'IA de décomposer la tâche
        prompt = f"""Tâche globale: {task_description}

Agents disponibles et leurs domaines:
{json.dumps(agent_domains, indent=2, ensure_ascii=False)}

Décompose cette tâche en sous-tâches spécifiques pour chaque agent selon leur domaine d'expertise.
Retourne un JSON avec le format: {{"agent_id": "description de la sous-tâche"}}"""
        
        messages = [
            {"role": "system", "content": "Tu es un coordinateur d'agents IA. Décompose les tâches de manière optimale."},
            {"role": "user", "content": prompt}
        ]
        
        response = await ai_manager.get_response(
            provider_name="openai",
            messages=messages,
            model="gpt-4"
        )
        
        # Parser la réponse JSON
        try:
            subtasks = json.loads(response)
            return subtasks
        except:
            # Fallback: créer des sous-tâches simples
            return {agent_id: f"{task_description} (perspective {domain})" 
                    for agent_id, domain in agent_domains.items()}
    
    async def _synthesize_results(
        self,
        task_description: str,
        task_results: Dict[str, Any],
        coordinator_agent: str
    ) -> str:
        """Synthétise les résultats de plusieurs agents"""
        from modules.core.ai_providers import ai_manager
        
        # Préparer les résultats pour la synthèse
        results_text = []
        for agent_id, result in task_results.items():
            agent = agent_orchestrator.agents.get(agent_id)
            domain = agent.config.domain if agent else "inconnu"
            result_content = result.get('result', 'Aucun résultat')
            results_text.append(f"**{domain.upper()}:**\n{result_content}")
        
        prompt = f"""Tâche initiale: {task_description}

Résultats des différents agents:

{chr(10).join(results_text)}

Synthétise ces résultats en une recommandation cohérente et actionnaire."""
        
        messages = [
            {"role": "system", "content": "Tu es un coordinateur qui synthétise les analyses de plusieurs experts."},
            {"role": "user", "content": prompt}
        ]
        
        synthesis = await ai_manager.get_response(
            provider_name="openai",
            messages=messages,
            model="gpt-4"
        )
        
        return synthesis
    
    def get_collaboration_history(self) -> List[Dict]:
        """Retourne l'historique des collaborations"""
        return list(self.collaboration_sessions.values())
    
    def get_collaboration_session(self, session_id: str) -> Optional[Dict]:
        """Récupère une session de collaboration"""
        return self.collaboration_sessions.get(session_id)


# Instances globales
communication_hub = AgentCommunicationHub()
collaboration_manager = AgentCollaborationManager()
