"""Base de connaissances vectorielle pour les agents IA"""
import json
import os
from typing import List, Dict, Optional, Any
from datetime import datetime
import numpy as np
from dataclasses import dataclass, asdict


@dataclass
class KnowledgeEntry:
    """Entrée dans la base de connaissances"""
    entry_id: str
    domain: str
    title: str
    content: str
    tags: List[str]
    created_at: str
    updated_at: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class AgentKnowledgeBase:
    """Base de connaissances pour les agents IA"""
    
    def __init__(self, storage_path: str = "agent_knowledge_base.json"):
        """
        Initialise la base de connaissances
        
        Args:
            storage_path: Chemin du fichier de stockage
        """
        self.storage_path = storage_path
        self.entries: Dict[str, KnowledgeEntry] = {}
        self.domain_index: Dict[str, List[str]] = {}  # domain -> entry_ids
        self.tag_index: Dict[str, List[str]] = {}  # tag -> entry_ids
        self.load()
    
    def add_entry(
        self,
        domain: str,
        title: str,
        content: str,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> KnowledgeEntry:
        """
        Ajoute une entrée à la base de connaissances
        
        Args:
            domain: Domaine de connaissance
            title: Titre de l'entrée
            content: Contenu
            tags: Tags pour la recherche
            metadata: Métadonnées additionnelles
            
        Returns:
            Entrée créée
        """
        entry_id = f"kb_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        entry = KnowledgeEntry(
            entry_id=entry_id,
            domain=domain,
            title=title,
            content=content,
            tags=tags or [],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            metadata=metadata or {}
        )
        
        self.entries[entry_id] = entry
        
        # Mettre à jour les index
        if domain not in self.domain_index:
            self.domain_index[domain] = []
        self.domain_index[domain].append(entry_id)
        
        for tag in entry.tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = []
            self.tag_index[tag].append(entry_id)
        
        self.save()
        return entry
    
    def search_by_domain(self, domain: str) -> List[KnowledgeEntry]:
        """Recherche par domaine"""
        entry_ids = self.domain_index.get(domain, [])
        return [self.entries[eid] for eid in entry_ids if eid in self.entries]
    
    def search_by_tag(self, tag: str) -> List[KnowledgeEntry]:
        """Recherche par tag"""
        entry_ids = self.tag_index.get(tag, [])
        return [self.entries[eid] for eid in entry_ids if eid in self.entries]
    
    def search_by_keywords(self, keywords: str) -> List[KnowledgeEntry]:
        """Recherche par mots-clés dans le titre et le contenu"""
        keywords_lower = keywords.lower()
        results = []
        
        for entry in self.entries.values():
            if (keywords_lower in entry.title.lower() or 
                keywords_lower in entry.content.lower()):
                results.append(entry)
        
        return results
    
    def get_entry(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """Récupère une entrée par son ID"""
        return self.entries.get(entry_id)
    
    def update_entry(
        self,
        entry_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Met à jour une entrée"""
        entry = self.entries.get(entry_id)
        if not entry:
            return False
        
        if title:
            entry.title = title
        if content:
            entry.content = content
        if tags is not None:
            # Mettre à jour l'index des tags
            for old_tag in entry.tags:
                if old_tag in self.tag_index and entry_id in self.tag_index[old_tag]:
                    self.tag_index[old_tag].remove(entry_id)
            
            entry.tags = tags
            for new_tag in tags:
                if new_tag not in self.tag_index:
                    self.tag_index[new_tag] = []
                if entry_id not in self.tag_index[new_tag]:
                    self.tag_index[new_tag].append(entry_id)
        
        if metadata:
            entry.metadata.update(metadata)
        
        entry.updated_at = datetime.now().isoformat()
        self.save()
        return True
    
    def delete_entry(self, entry_id: str) -> bool:
        """Supprime une entrée"""
        entry = self.entries.get(entry_id)
        if not entry:
            return False
        
        # Supprimer des index
        if entry.domain in self.domain_index:
            if entry_id in self.domain_index[entry.domain]:
                self.domain_index[entry.domain].remove(entry_id)
        
        for tag in entry.tags:
            if tag in self.tag_index and entry_id in self.tag_index[tag]:
                self.tag_index[tag].remove(entry_id)
        
        # Supprimer l'entrée
        del self.entries[entry_id]
        self.save()
        return True
    
    def get_all_domains(self) -> List[str]:
        """Retourne tous les domaines"""
        return list(self.domain_index.keys())
    
    def get_all_tags(self) -> List[str]:
        """Retourne tous les tags"""
        return list(self.tag_index.keys())
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne des statistiques sur la base de connaissances"""
        return {
            'total_entries': len(self.entries),
            'domains': len(self.domain_index),
            'tags': len(self.tag_index),
            'entries_by_domain': {
                domain: len(entries) 
                for domain, entries in self.domain_index.items()
            }
        }
    
    def save(self):
        """Sauvegarde la base de connaissances"""
        data = {
            'entries': {eid: asdict(entry) for eid, entry in self.entries.items()},
            'domain_index': self.domain_index,
            'tag_index': self.tag_index,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self):
        """Charge la base de connaissances"""
        if not os.path.exists(self.storage_path):
            return
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.entries = {
                eid: KnowledgeEntry(**entry_data)
                for eid, entry_data in data.get('entries', {}).items()
            }
            self.domain_index = data.get('domain_index', {})
            self.tag_index = data.get('tag_index', {})
        except Exception as e:
            print(f"Erreur lors du chargement de la base de connaissances: {e}")


def initialize_knowledge_base_with_defaults():
    """Initialise la base de connaissances avec des entrées par défaut"""
    kb = AgentKnowledgeBase()
    
    # Connaissances Ventes
    kb.add_entry(
        domain="ventes",
        title="Techniques de Closing Efficaces",
        content="""Les meilleures techniques de closing:
        1. Assumptive Close: Agir comme si la vente était déjà conclue
        2. Alternative Close: Proposer deux options positives
        3. Urgency Close: Créer un sentiment d'urgence
        4. Summary Close: Récapituler les bénéfices
        5. Question Close: Poser une question qui mène à la vente""",
        tags=["ventes", "closing", "techniques", "conversion"]
    )
    
    kb.add_entry(
        domain="ventes",
        title="Qualification de Leads - Méthode BANT",
        content="""BANT pour qualifier les prospects:
        - Budget: Le prospect a-t-il le budget?
        - Authority: Est-ce le décideur?
        - Need: A-t-il un besoin réel?
        - Timeline: Quel est le timing d'achat?""",
        tags=["ventes", "prospection", "qualification", "leads"]
    )
    
    # Connaissances Marketing
    kb.add_entry(
        domain="marketing",
        title="Framework AIDA pour le Copywriting",
        content="""AIDA - Structure de copywriting efficace:
        - Attention: Capter l'attention avec un titre accrocheur
        - Interest: Susciter l'intérêt avec des bénéfices
        - Desire: Créer le désir avec des preuves sociales
        - Action: Inciter à l'action avec un CTA clair""",
        tags=["marketing", "copywriting", "contenu", "conversion"]
    )
    
    kb.add_entry(
        domain="marketing",
        title="Métriques Marketing Essentielles",
        content="""KPIs marketing à suivre:
        - CAC (Customer Acquisition Cost)
        - LTV (Lifetime Value)
        - ROI des campagnes
        - Taux de conversion
        - Engagement rate
        - CTR (Click-Through Rate)""",
        tags=["marketing", "métriques", "analytics", "kpi"]
    )
    
    # Connaissances Finance
    kb.add_entry(
        domain="finance",
        title="Ratios Financiers Clés",
        content="""Ratios financiers essentiels:
        - Marge brute = (CA - Coûts directs) / CA
        - Marge nette = Bénéfice net / CA
        - ROI = (Gain - Coût) / Coût
        - Cash burn rate = Dépenses mensuelles
        - Runway = Trésorerie / Burn rate""",
        tags=["finance", "ratios", "analyse", "métriques"]
    )
    
    # Connaissances Opérations
    kb.add_entry(
        domain="operations",
        title="Principes Lean Management",
        content="""5 principes du Lean:
        1. Définir la valeur du point de vue client
        2. Identifier la chaîne de valeur
        3. Créer un flux continu
        4. Mettre en place un système tiré (pull)
        5. Viser la perfection (amélioration continue)""",
        tags=["operations", "lean", "processus", "efficacité"]
    )
    
    # Connaissances RH
    kb.add_entry(
        domain="ressources_humaines",
        title="Méthode STAR pour les Entretiens",
        content="""STAR - Structure d'entretien:
        - Situation: Contexte de l'expérience
        - Task: Tâche ou défi à relever
        - Action: Actions entreprises
        - Result: Résultats obtenus""",
        tags=["rh", "recrutement", "entretien", "évaluation"]
    )
    
    # Connaissances Produit
    kb.add_entry(
        domain="produit",
        title="Framework RICE pour Priorisation",
        content="""RICE - Prioriser les fonctionnalités:
        - Reach: Nombre d'utilisateurs impactés
        - Impact: Niveau d'impact (0.25 à 3)
        - Confidence: Niveau de confiance (%)
        - Effort: Effort nécessaire (jours/personne)
        Score RICE = (Reach × Impact × Confidence) / Effort""",
        tags=["produit", "priorisation", "roadmap", "features"]
    )
    
    return kb


# Instance globale
knowledge_base = AgentKnowledgeBase()
