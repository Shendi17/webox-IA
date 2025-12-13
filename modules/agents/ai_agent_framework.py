"""Framework d'orchestration des agents IA spécialisés"""
import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio


class AgentStatus(Enum):
    """Statuts possibles d'un agent"""
    IDLE = "idle"
    WORKING = "working"
    COMPLETED = "completed"
    ERROR = "error"
    WAITING = "waiting"


class AgentDomain(Enum):
    """Domaines d'expertise des agents"""
    SALES = "ventes"
    MARKETING = "marketing"
    FINANCE = "finance"
    OPERATIONS = "operations"
    HR = "ressources_humaines"
    CUSTOMER_SERVICE = "service_client"
    PRODUCT = "produit"
    STRATEGY = "strategie"


@dataclass
class AgentTask:
    """Représente une tâche assignée à un agent"""
    task_id: str
    agent_id: str
    description: str
    priority: int  # 1-5, 5 étant le plus prioritaire
    status: str
    created_at: str
    completed_at: Optional[str] = None
    result: Optional[str] = None
    dependencies: List[str] = None  # IDs des tâches dont celle-ci dépend
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class AgentConfig:
    """Configuration d'un agent IA"""
    agent_id: str
    name: str
    domain: str
    description: str
    system_prompt: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    tools: List[str] = None
    
    def __post_init__(self):
        if self.tools is None:
            self.tools = []


class AIAgent:
    """Agent IA spécialisé"""
    
    def __init__(self, config: AgentConfig):
        """
        Initialise un agent IA
        
        Args:
            config: Configuration de l'agent
        """
        self.config = config
        self.status = AgentStatus.IDLE
        self.current_task: Optional[AgentTask] = None
        self.task_history: List[AgentTask] = []
        self.memory: List[Dict] = []
        self.metrics = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'total_execution_time': 0,
            'success_rate': 0.0
        }
    
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Exécute une tâche
        
        Args:
            task: Tâche à exécuter
            
        Returns:
            Résultat de l'exécution
        """
        self.status = AgentStatus.WORKING
        self.current_task = task
        task.status = "in_progress"
        
        start_time = datetime.now()
        
        try:
            # Construire le contexte
            context = self._build_context(task)
            
            # Appeler l'IA
            from modules.core.ai_providers import ai_manager
            
            messages = [
                {"role": "system", "content": self.config.system_prompt},
                {"role": "user", "content": f"Tâche: {task.description}\n\nContexte: {context}"}
            ]
            
            result = await ai_manager.get_response(
                provider_name="openai",
                messages=messages,
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Mettre à jour la tâche
            task.status = "completed"
            task.completed_at = datetime.now().isoformat()
            task.result = result
            
            # Mettre à jour les métriques
            execution_time = (datetime.now() - start_time).total_seconds()
            self.metrics['tasks_completed'] += 1
            self.metrics['total_execution_time'] += execution_time
            self._update_success_rate()
            
            # Ajouter à l'historique
            self.task_history.append(task)
            
            # Ajouter à la mémoire
            self.memory.append({
                'task': task.description,
                'result': result,
                'timestamp': datetime.now().isoformat()
            })
            
            self.status = AgentStatus.COMPLETED
            
            return {
                'success': True,
                'result': result,
                'execution_time': execution_time,
                'task_id': task.task_id
            }
            
        except Exception as e:
            task.status = "error"
            task.result = f"Erreur: {str(e)}"
            self.metrics['tasks_failed'] += 1
            self._update_success_rate()
            self.status = AgentStatus.ERROR
            
            return {
                'success': False,
                'error': str(e),
                'task_id': task.task_id
            }
        
        finally:
            self.current_task = None
    
    def _build_context(self, task: AgentTask) -> str:
        """Construit le contexte pour la tâche"""
        context_parts = []
        
        # Ajouter les dernières tâches de la mémoire
        if self.memory:
            recent_memory = self.memory[-3:]  # 3 dernières tâches
            context_parts.append("Tâches récentes:")
            for mem in recent_memory:
                context_parts.append(f"- {mem['task']}: {mem['result'][:100]}...")
        
        # Ajouter le domaine d'expertise
        context_parts.append(f"\nDomaine d'expertise: {self.config.domain}")
        
        return "\n".join(context_parts)
    
    def _update_success_rate(self):
        """Met à jour le taux de succès"""
        total = self.metrics['tasks_completed'] + self.metrics['tasks_failed']
        if total > 0:
            self.metrics['success_rate'] = self.metrics['tasks_completed'] / total
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut de l'agent"""
        return {
            'agent_id': self.config.agent_id,
            'name': self.config.name,
            'domain': self.config.domain,
            'status': self.status.value,
            'current_task': asdict(self.current_task) if self.current_task else None,
            'metrics': self.metrics,
            'memory_size': len(self.memory)
        }


class AgentOrchestrator:
    """Orchestrateur d'agents IA"""
    
    def __init__(self):
        """Initialise l'orchestrateur"""
        self.agents: Dict[str, AIAgent] = {}
        self.task_queue: List[AgentTask] = []
        self.completed_tasks: List[AgentTask] = []
        self.task_graph: Dict[str, List[str]] = {}  # Graphe de dépendances
    
    def register_agent(self, config: AgentConfig) -> AIAgent:
        """
        Enregistre un nouvel agent
        
        Args:
            config: Configuration de l'agent
            
        Returns:
            Agent créé
        """
        agent = AIAgent(config)
        self.agents[config.agent_id] = agent
        return agent
    
    def create_task(
        self,
        agent_id: str,
        description: str,
        priority: int = 3,
        dependencies: List[str] = None
    ) -> AgentTask:
        """
        Crée une nouvelle tâche
        
        Args:
            agent_id: ID de l'agent assigné
            description: Description de la tâche
            priority: Priorité (1-5)
            dependencies: IDs des tâches dépendantes
            
        Returns:
            Tâche créée
        """
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        task = AgentTask(
            task_id=task_id,
            agent_id=agent_id,
            description=description,
            priority=priority,
            status="pending",
            created_at=datetime.now().isoformat(),
            dependencies=dependencies or []
        )
        
        self.task_queue.append(task)
        
        # Mettre à jour le graphe de dépendances
        if dependencies:
            self.task_graph[task_id] = dependencies
        
        return task
    
    def _can_execute_task(self, task: AgentTask) -> bool:
        """Vérifie si une tâche peut être exécutée"""
        if not task.dependencies:
            return True
        
        # Vérifier que toutes les dépendances sont complétées
        for dep_id in task.dependencies:
            dep_task = next((t for t in self.completed_tasks if t.task_id == dep_id), None)
            if not dep_task or dep_task.status != "completed":
                return False
        
        return True
    
    async def execute_next_task(self) -> Optional[Dict[str, Any]]:
        """
        Exécute la prochaine tâche disponible
        
        Returns:
            Résultat de l'exécution ou None
        """
        if not self.task_queue:
            return None
        
        # Trier par priorité
        self.task_queue.sort(key=lambda t: t.priority, reverse=True)
        
        # Trouver la première tâche exécutable
        for task in self.task_queue:
            if self._can_execute_task(task):
                # Retirer de la queue
                self.task_queue.remove(task)
                
                # Récupérer l'agent
                agent = self.agents.get(task.agent_id)
                if not agent:
                    return {'success': False, 'error': f"Agent {task.agent_id} introuvable"}
                
                # Exécuter
                result = await agent.execute_task(task)
                
                # Ajouter aux tâches complétées
                self.completed_tasks.append(task)
                
                return result
        
        return None
    
    async def execute_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Exécute toutes les tâches en queue
        
        Returns:
            Liste des résultats
        """
        results = []
        
        while self.task_queue:
            result = await self.execute_next_task()
            if result:
                results.append(result)
            else:
                # Aucune tâche exécutable, attendre ou sortir
                break
        
        return results
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Retourne le statut d'un agent"""
        agent = self.agents.get(agent_id)
        return agent.get_status() if agent else None
    
    def get_all_agents_status(self) -> List[Dict[str, Any]]:
        """Retourne le statut de tous les agents"""
        return [agent.get_status() for agent in self.agents.values()]
    
    def get_task_queue_status(self) -> Dict[str, Any]:
        """Retourne le statut de la queue de tâches"""
        return {
            'pending_tasks': len(self.task_queue),
            'completed_tasks': len(self.completed_tasks),
            'tasks': [asdict(task) for task in self.task_queue]
        }
    
    def save_state(self, filepath: str = "agent_orchestrator_state.json"):
        """Sauvegarde l'état de l'orchestrateur"""
        state = {
            'agents': {
                agent_id: {
                    'config': asdict(agent.config),
                    'metrics': agent.metrics,
                    'memory': agent.memory
                }
                for agent_id, agent in self.agents.items()
            },
            'task_queue': [asdict(task) for task in self.task_queue],
            'completed_tasks': [asdict(task) for task in self.completed_tasks],
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def load_state(self, filepath: str = "agent_orchestrator_state.json"):
        """Charge l'état de l'orchestrateur"""
        if not os.path.exists(filepath):
            return
        
        with open(filepath, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        # Restaurer les agents
        for agent_id, agent_data in state.get('agents', {}).items():
            config = AgentConfig(**agent_data['config'])
            agent = self.register_agent(config)
            agent.metrics = agent_data['metrics']
            agent.memory = agent_data['memory']
        
        # Restaurer les tâches
        self.task_queue = [AgentTask(**task) for task in state.get('task_queue', [])]
        self.completed_tasks = [AgentTask(**task) for task in state.get('completed_tasks', [])]


# Instance globale
agent_orchestrator = AgentOrchestrator()
