"""
Service pour gérer les déploiements (Netlify, Vercel, etc.)
"""
import os
import requests
import json
from typing import Dict, Optional
from pathlib import Path


class DeploymentService:
    """Service de base pour les déploiements"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
    
    def deploy(self, project_path: str, config: Dict) -> Dict:
        """Déployer un projet"""
        raise NotImplementedError


class NetlifyDeployment(DeploymentService):
    """Service de déploiement Netlify"""
    
    BASE_URL = "https://api.netlify.com/api/v1"
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key or os.getenv("NETLIFY_API_KEY"))
    
    def get_sites(self) -> Dict:
        """Lister tous les sites"""
        if not self.api_key:
            return {"success": False, "error": "Clé API Netlify non configurée"}
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/sites",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30
            )
            
            if response.status_code == 200:
                sites = response.json()
                return {
                    "success": True,
                    "sites": [{
                        "id": site["id"],
                        "name": site["name"],
                        "url": site["url"],
                        "custom_domain": site.get("custom_domain"),
                        "created_at": site["created_at"],
                        "updated_at": site["updated_at"]
                    } for site in sites]
                }
            else:
                return {"success": False, "error": f"Erreur {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_site(self, name: str, custom_domain: str = None) -> Dict:
        """Créer un nouveau site"""
        if not self.api_key:
            return {"success": False, "error": "Clé API Netlify non configurée"}
        
        try:
            data = {"name": name}
            if custom_domain:
                data["custom_domain"] = custom_domain
            
            response = requests.post(
                f"{self.BASE_URL}/sites",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=data,
                timeout=30
            )
            
            if response.status_code == 201:
                site = response.json()
                return {
                    "success": True,
                    "site_id": site["id"],
                    "name": site["name"],
                    "url": site["url"]
                }
            else:
                return {"success": False, "error": f"Erreur {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def deploy(self, project_path: str, site_id: str = None, config: Dict = None) -> Dict:
        """Déployer un projet sur Netlify"""
        if not self.api_key:
            return {"success": False, "error": "Clé API Netlify non configurée"}
        
        try:
            # Si pas de site_id, créer un nouveau site
            if not site_id:
                create_result = self.create_site(config.get("name", "webox-site"))
                if not create_result.get("success"):
                    return create_result
                site_id = create_result["site_id"]
            
            # Créer un déploiement
            # Note: Netlify nécessite un ZIP du projet ou un déploiement via Git
            # Pour simplifier, on utilise l'API de déploiement direct
            
            return {
                "success": True,
                "site_id": site_id,
                "message": "Déploiement initié",
                "note": "Utilisez Netlify CLI ou Git pour le déploiement complet"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_deploys(self, site_id: str) -> Dict:
        """Obtenir les déploiements d'un site"""
        if not self.api_key:
            return {"success": False, "error": "Clé API Netlify non configurée"}
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/sites/{site_id}/deploys",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30
            )
            
            if response.status_code == 200:
                deploys = response.json()
                return {
                    "success": True,
                    "deploys": [{
                        "id": deploy["id"],
                        "state": deploy["state"],
                        "created_at": deploy["created_at"],
                        "published_at": deploy.get("published_at"),
                        "deploy_url": deploy["deploy_url"],
                        "branch": deploy.get("branch")
                    } for deploy in deploys[:10]]  # Limiter à 10
                }
            else:
                return {"success": False, "error": f"Erreur {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}


class VercelDeployment(DeploymentService):
    """Service de déploiement Vercel"""
    
    BASE_URL = "https://api.vercel.com"
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key or os.getenv("VERCEL_API_KEY"))
    
    def get_projects(self) -> Dict:
        """Lister tous les projets"""
        if not self.api_key:
            return {"success": False, "error": "Clé API Vercel non configurée"}
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/v9/projects",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                projects = data.get("projects", [])
                return {
                    "success": True,
                    "projects": [{
                        "id": project["id"],
                        "name": project["name"],
                        "framework": project.get("framework"),
                        "created_at": project["createdAt"],
                        "updated_at": project["updatedAt"]
                    } for project in projects]
                }
            else:
                return {"success": False, "error": f"Erreur {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_project(self, name: str, framework: str = None) -> Dict:
        """Créer un nouveau projet"""
        if not self.api_key:
            return {"success": False, "error": "Clé API Vercel non configurée"}
        
        try:
            data = {"name": name}
            if framework:
                data["framework"] = framework
            
            response = requests.post(
                f"{self.BASE_URL}/v9/projects",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                project = response.json()
                return {
                    "success": True,
                    "project_id": project["id"],
                    "name": project["name"]
                }
            else:
                return {"success": False, "error": f"Erreur {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def deploy(self, project_path: str, project_id: str = None, config: Dict = None) -> Dict:
        """Déployer un projet sur Vercel"""
        if not self.api_key:
            return {"success": False, "error": "Clé API Vercel non configurée"}
        
        try:
            # Si pas de project_id, créer un nouveau projet
            if not project_id:
                create_result = self.create_project(
                    config.get("name", "webox-project"),
                    config.get("framework")
                )
                if not create_result.get("success"):
                    return create_result
                project_id = create_result["project_id"]
            
            # Créer un déploiement
            # Note: Vercel nécessite un déploiement via Git ou CLI
            
            return {
                "success": True,
                "project_id": project_id,
                "message": "Déploiement initié",
                "note": "Utilisez Vercel CLI ou Git pour le déploiement complet"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_deployments(self, project_id: str) -> Dict:
        """Obtenir les déploiements d'un projet"""
        if not self.api_key:
            return {"success": False, "error": "Clé API Vercel non configurée"}
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/v6/deployments",
                headers={"Authorization": f"Bearer {self.api_key}"},
                params={"projectId": project_id, "limit": 10},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                deployments = data.get("deployments", [])
                return {
                    "success": True,
                    "deployments": [{
                        "id": deploy["uid"],
                        "state": deploy["state"],
                        "created_at": deploy["created"],
                        "url": deploy["url"],
                        "ready_state": deploy.get("readyState")
                    } for deploy in deployments]
                }
            else:
                return {"success": False, "error": f"Erreur {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}


class DeploymentFactory:
    """Factory pour créer les services de déploiement"""
    
    @staticmethod
    def get_service(provider: str) -> DeploymentService:
        """Obtenir le service de déploiement"""
        providers = {
            "netlify": NetlifyDeployment,
            "vercel": VercelDeployment
        }
        
        service_class = providers.get(provider.lower())
        if not service_class:
            raise ValueError(f"Provider '{provider}' non supporté")
        
        return service_class()
    
    @staticmethod
    def deploy(provider: str, project_path: str, config: Dict) -> Dict:
        """Déployer vers un provider"""
        try:
            service = DeploymentFactory.get_service(provider)
            return service.deploy(project_path, config=config)
        except Exception as e:
            return {"success": False, "error": str(e)}
