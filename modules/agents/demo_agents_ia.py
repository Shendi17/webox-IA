"""Script de démonstration du système d'agents IA"""
import asyncio
from modules.agents.ai_agent_framework import agent_orchestrator
from modules.agents.specialized_agents import initialize_all_agents
from modules.agents.agent_communication import collaboration_manager
from modules.agents.agent_knowledge_base import knowledge_base, initialize_knowledge_base_with_defaults


async def demo_tache_simple():
    """Démonstration d'une tâche simple"""
    print("\n" + "="*60)
    print("DÉMONSTRATION 1 : TÂCHE SIMPLE")
    print("="*60)
    
    # Créer une tâche pour l'agent Ventes
    print("\n📋 Création d'une tâche pour l'Agent Ventes...")
    task = agent_orchestrator.create_task(
        agent_id="agent_ventes",
        description="Analyser les performances commerciales du dernier trimestre et proposer 3 actions pour améliorer le taux de conversion",
        priority=4
    )
    
    print(f"✅ Tâche créée : {task.task_id}")
    print(f"   Description : {task.description}")
    print(f"   Priorité : {task.priority}")
    
    # Exécuter la tâche
    print("\n🚀 Exécution de la tâche...")
    result = await agent_orchestrator.execute_next_task()
    
    if result and result.get('success'):
        print("\n✅ RÉSULTAT :")
        print("-" * 60)
        print(result.get('result'))
        print("-" * 60)
        print(f"\n⏱️  Temps d'exécution : {result.get('execution_time', 0):.2f}s")
    else:
        print(f"\n❌ Erreur : {result.get('error', 'Erreur inconnue')}")


async def demo_collaboration():
    """Démonstration de la collaboration multi-agents"""
    print("\n" + "="*60)
    print("DÉMONSTRATION 2 : COLLABORATION MULTI-AGENTS")
    print("="*60)
    
    print("\n🤝 Création d'une tâche collaborative...")
    print("   Tâche : Créer une stratégie de lancement produit")
    print("   Agents impliqués : Produit, Marketing, Ventes")
    print("   Coordinateur : Stratégie")
    
    result = await collaboration_manager.create_collaboration_task(
        task_description="""Créer une stratégie complète de lancement pour un nouveau produit SaaS.
        
        Contexte:
        - Produit : Plateforme de gestion de projet IA
        - Public cible : PME et startups
        - Budget marketing : 50 000€
        - Timeline : 3 mois
        
        Fournir :
        1. Positionnement produit
        2. Stratégie go-to-market
        3. Plan de vente et pricing
        4. Vision long terme""",
        involved_agents=["agent_produit", "agent_marketing", "agent_ventes"],
        coordinator_agent="agent_strategie"
    )
    
    if result.get('success'):
        print("\n✅ SYNTHÈSE DE LA COLLABORATION :")
        print("="*60)
        print(result.get('synthesis'))
        print("="*60)
        
        print("\n📊 RÉSULTATS INDIVIDUELS :")
        for agent_id, agent_result in result.get('individual_results', {}).items():
            agent = agent_orchestrator.agents.get(agent_id)
            if agent:
                print(f"\n🤖 {agent.config.name} ({agent.config.domain}):")
                print("-" * 60)
                print(agent_result.get('result', 'Aucun résultat')[:300] + "...")
    else:
        print(f"\n❌ Erreur : {result.get('error', 'Erreur inconnue')}")


def demo_knowledge_base():
    """Démonstration de la base de connaissances"""
    print("\n" + "="*60)
    print("DÉMONSTRATION 3 : BASE DE CONNAISSANCES")
    print("="*60)
    
    # Statistiques
    stats = knowledge_base.get_stats()
    print(f"\n📊 Statistiques :")
    print(f"   Entrées totales : {stats['total_entries']}")
    print(f"   Domaines : {stats['domains']}")
    print(f"   Tags : {stats['tags']}")
    
    # Recherche par domaine
    print("\n🔍 Recherche dans le domaine 'ventes' :")
    results = knowledge_base.search_by_domain("ventes")
    for entry in results:
        print(f"\n   📄 {entry.title}")
        print(f"      {entry.content[:150]}...")
        print(f"      Tags : {', '.join(entry.tags)}")
    
    # Ajouter une nouvelle entrée
    print("\n➕ Ajout d'une nouvelle connaissance...")
    new_entry = knowledge_base.add_entry(
        domain="marketing",
        title="Growth Hacking - Stratégies Virales",
        content="""Stratégies de growth hacking pour croissance virale:
        1. Referral Program (parrainage)
        2. Product-Led Growth
        3. Content Marketing viral
        4. Social Proof et FOMO
        5. Gamification""",
        tags=["marketing", "growth", "viral", "acquisition"]
    )
    print(f"   ✅ Entrée ajoutée : {new_entry.title}")


def demo_metriques():
    """Démonstration des métriques"""
    print("\n" + "="*60)
    print("DÉMONSTRATION 4 : MÉTRIQUES ET MONITORING")
    print("="*60)
    
    print("\n📊 Performance des Agents :")
    print("-" * 60)
    
    for agent in agent_orchestrator.agents.values():
        print(f"\n🤖 {agent.config.name} ({agent.config.domain})")
        print(f"   Tâches complétées : {agent.metrics['tasks_completed']}")
        print(f"   Tâches échouées : {agent.metrics['tasks_failed']}")
        print(f"   Taux de succès : {agent.metrics['success_rate']:.1%}")
        print(f"   Temps total : {agent.metrics['total_execution_time']:.2f}s")
        print(f"   Mémoire : {len(agent.memory)} entrées")
    
    # Métriques globales
    all_status = agent_orchestrator.get_all_agents_status()
    total_tasks = sum(s['metrics']['tasks_completed'] for s in all_status)
    total_failed = sum(s['metrics']['tasks_failed'] for s in all_status)
    avg_success = sum(s['metrics']['success_rate'] for s in all_status) / len(all_status) if all_status else 0
    
    print("\n📈 MÉTRIQUES GLOBALES :")
    print("-" * 60)
    print(f"   Agents actifs : {len(agent_orchestrator.agents)}")
    print(f"   Total tâches complétées : {total_tasks}")
    print(f"   Total tâches échouées : {total_failed}")
    print(f"   Taux de succès moyen : {avg_success:.1%}")


async def main():
    """Fonction principale de démonstration"""
    print("\n" + "="*60)
    print("🤖 DÉMONSTRATION DU SYSTÈME D'AGENTS IA")
    print("="*60)
    
    # Initialiser les agents
    print("\n⚙️  Initialisation des agents...")
    initialize_all_agents()
    print(f"✅ {len(agent_orchestrator.agents)} agents initialisés")
    
    # Initialiser la base de connaissances
    if len(knowledge_base.entries) == 0:
        print("\n📚 Initialisation de la base de connaissances...")
        initialize_knowledge_base_with_defaults()
        print(f"✅ {len(knowledge_base.entries)} connaissances chargées")
    
    # Démonstrations
    try:
        # 1. Tâche simple
        await demo_tache_simple()
        
        # 2. Collaboration (commenté pour éviter les coûts API)
        # await demo_collaboration()
        
        # 3. Base de connaissances
        demo_knowledge_base()
        
        # 4. Métriques
        demo_metriques()
        
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
    
    # Sauvegarder l'état
    print("\n💾 Sauvegarde de l'état...")
    agent_orchestrator.save_state()
    print("✅ État sauvegardé dans 'agent_orchestrator_state.json'")
    
    print("\n" + "="*60)
    print("✅ DÉMONSTRATION TERMINÉE !")
    print("="*60)
    print("\n💡 Pour utiliser le système complet, lancez :")
    print("   streamlit run app.py")
    print("\n   Puis accédez à : 🤖 Agents IA")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Exécuter la démonstration
    asyncio.run(main())
