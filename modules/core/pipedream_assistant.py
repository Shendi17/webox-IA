"""Assistant IA spécialisé pour Pipedream - Automatisation"""

# Templates de workflows Pipedream
PIPEDREAM_TEMPLATES = {
    "webhook_to_email": {
        "name": "Webhook vers Email",
        "description": "Recevoir un webhook et envoyer un email",
        "category": "Communication",
        "steps": [
            {
                "type": "trigger",
                "app": "http",
                "name": "webhook",
                "description": "Trigger HTTP/Webhook"
            },
            {
                "type": "action",
                "app": "email",
                "name": "send_email",
                "description": "Envoyer un email",
                "params": {
                    "subject": "{{ steps.webhook.body.subject }}",
                    "text": "{{ steps.webhook.body.message }}",
                    "to": "votre@email.com"
                }
            }
        ],
        "code_example": """
export default defineComponent({
  async run({ steps, $ }) {
    await require("@pipedream/platform").axios($, {
      method: "POST",
      url: "https://api.sendgrid.com/v3/mail/send",
      headers: {
        "Authorization": `Bearer ${this.sendgrid.$auth.api_key}`,
      },
      data: {
        personalizations: [{
          to: [{ email: "votre@email.com" }],
          subject: steps.webhook.body.subject
        }],
        from: { email: "noreply@example.com" },
        content: [{
          type: "text/plain",
          value: steps.webhook.body.message
        }]
      }
    });
  }
});
"""
    },
    
    "schedule_slack": {
        "name": "Rappel Slack Planifié",
        "description": "Envoyer un message Slack à intervalles réguliers",
        "category": "Productivité",
        "steps": [
            {
                "type": "trigger",
                "app": "schedule",
                "name": "cron",
                "description": "Déclencheur planifié (Cron)",
                "params": {
                    "cron": "0 9 * * 1-5"  # Tous les jours de semaine à 9h
                }
            },
            {
                "type": "action",
                "app": "slack",
                "name": "send_message",
                "description": "Envoyer un message Slack",
                "params": {
                    "channel": "#general",
                    "text": "Bonjour ! N'oubliez pas votre réunion quotidienne."
                }
            }
        ],
        "code_example": """
export default defineComponent({
  async run({ steps, $ }) {
    await require("@pipedreamhq/platform").axios($, {
      method: "POST",
      url: "https://slack.com/api/chat.postMessage",
      headers: {
        "Authorization": `Bearer ${this.slack.$auth.oauth_access_token}`,
      },
      data: {
        channel: "#general",
        text: "Bonjour ! N'oubliez pas votre réunion quotidienne."
      }
    });
  }
});
"""
    },
    
    "form_to_sheets": {
        "name": "Formulaire vers Google Sheets",
        "description": "Sauvegarder les soumissions de formulaire dans Google Sheets",
        "category": "Data",
        "steps": [
            {
                "type": "trigger",
                "app": "http",
                "name": "webhook",
                "description": "Recevoir les données du formulaire"
            },
            {
                "type": "action",
                "app": "google_sheets",
                "name": "add_row",
                "description": "Ajouter une ligne dans Google Sheets",
                "params": {
                    "spreadsheet_id": "VOTRE_SPREADSHEET_ID",
                    "sheet_name": "Réponses",
                    "values": [
                        "{{ steps.webhook.body.name }}",
                        "{{ steps.webhook.body.email }}",
                        "{{ steps.webhook.body.message }}",
                        "{{ new Date().toISOString() }}"
                    ]
                }
            }
        ],
        "code_example": """
export default defineComponent({
  async run({ steps, $ }) {
    await require("@pipedreamhq/platform").axios($, {
      method: "POST",
      url: `https://sheets.googleapis.com/v4/spreadsheets/${this.google_sheets.$auth.spreadsheet_id}/values/Réponses:append`,
      headers: {
        "Authorization": `Bearer ${this.google_sheets.$auth.oauth_access_token}`,
      },
      params: {
        valueInputOption: "USER_ENTERED"
      },
      data: {
        values: [[
          steps.webhook.body.name,
          steps.webhook.body.email,
          steps.webhook.body.message,
          new Date().toISOString()
        ]]
      }
    });
  }
});
"""
    },
    
    "ai_content_moderator": {
        "name": "Modération de Contenu avec IA",
        "description": "Analyser et modérer du contenu avec OpenAI",
        "category": "IA",
        "steps": [
            {
                "type": "trigger",
                "app": "http",
                "name": "webhook",
                "description": "Recevoir le contenu à modérer"
            },
            {
                "type": "action",
                "app": "openai",
                "name": "moderate_content",
                "description": "Analyser avec OpenAI Moderation API",
                "params": {
                    "input": "{{ steps.webhook.body.content }}"
                }
            },
            {
                "type": "action",
                "app": "code",
                "name": "check_result",
                "description": "Vérifier le résultat et agir"
            }
        ],
        "code_example": """
export default defineComponent({
  async run({ steps, $ }) {
    // Modération avec OpenAI
    const moderation = await require("@pipedreamhq/platform").axios($, {
      method: "POST",
      url: "https://api.openai.com/v1/moderations",
      headers: {
        "Authorization": `Bearer ${this.openai.$auth.api_key}`,
      },
      data: {
        input: steps.webhook.body.content
      }
    });
    
    const isFlagged = moderation.results[0].flagged;
    
    if (isFlagged) {
      // Envoyer une alerte
      await $.send.http({
        method: "POST",
        url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
        data: {
          text: `⚠️ Contenu inapproprié détecté: ${steps.webhook.body.content.substring(0, 100)}...`
        }
      });
    }
    
    return { flagged: isFlagged, categories: moderation.results[0].categories };
  }
});
"""
    },
    
    "rss_to_social": {
        "name": "RSS vers Réseaux Sociaux",
        "description": "Publier automatiquement les nouveaux articles RSS sur les réseaux sociaux",
        "category": "Marketing",
        "steps": [
            {
                "type": "trigger",
                "app": "rss",
                "name": "new_item",
                "description": "Nouveau article RSS",
                "params": {
                    "feed_url": "https://example.com/feed.xml"
                }
            },
            {
                "type": "action",
                "app": "twitter",
                "name": "post_tweet",
                "description": "Publier sur Twitter",
                "params": {
                    "text": "{{ steps.new_item.title }} {{ steps.new_item.link }}"
                }
            },
            {
                "type": "action",
                "app": "linkedin",
                "name": "share_post",
                "description": "Publier sur LinkedIn",
                "params": {
                    "text": "{{ steps.new_item.title }}",
                    "url": "{{ steps.new_item.link }}"
                }
            }
        ],
        "code_example": """
export default defineComponent({
  async run({ steps, $ }) {
    // Twitter
    await require("@pipedreamhq/platform").axios($, {
      method: "POST",
      url: "https://api.twitter.com/2/tweets",
      headers: {
        "Authorization": `Bearer ${this.twitter.$auth.oauth_access_token}`,
      },
      data: {
        text: `${steps.new_item.title} ${steps.new_item.link}`
      }
    });
    
    // LinkedIn
    await require("@pipedreamhq/platform").axios($, {
      method: "POST",
      url: "https://api.linkedin.com/v2/ugcPosts",
      headers: {
        "Authorization": `Bearer ${this.linkedin.$auth.oauth_access_token}`,
      },
      data: {
        author: `urn:li:person:${this.linkedin.$auth.person_id}`,
        lifecycleState: "PUBLISHED",
        specificContent: {
          "com.linkedin.ugc.ShareContent": {
            shareCommentary: {
              text: steps.new_item.title
            },
            shareMediaCategory: "ARTICLE",
            media: [{
              status: "READY",
              originalUrl: steps.new_item.link
            }]
          }
        }
      }
    });
  }
});
"""
    },
    
    "ai_email_responder": {
        "name": "Répondeur Email avec IA",
        "description": "Répondre automatiquement aux emails avec GPT-4",
        "category": "IA",
        "steps": [
            {
                "type": "trigger",
                "app": "gmail",
                "name": "new_email",
                "description": "Nouveau email reçu"
            },
            {
                "type": "action",
                "app": "openai",
                "name": "generate_response",
                "description": "Générer une réponse avec GPT-4",
                "params": {
                    "model": "gpt-4",
                    "prompt": "Rédige une réponse professionnelle à cet email: {{ steps.new_email.body }}"
                }
            },
            {
                "type": "action",
                "app": "gmail",
                "name": "send_reply",
                "description": "Envoyer la réponse",
                "params": {
                    "to": "{{ steps.new_email.from }}",
                    "subject": "Re: {{ steps.new_email.subject }}",
                    "body": "{{ steps.generate_response.choices[0].message.content }}"
                }
            }
        ],
        "code_example": """
export default defineComponent({
  async run({ steps, $ }) {
    // Générer la réponse avec GPT-4
    const response = await require("@pipedreamhq/platform").axios($, {
      method: "POST",
      url: "https://api.openai.com/v1/chat/completions",
      headers: {
        "Authorization": `Bearer ${this.openai.$auth.api_key}`,
      },
      data: {
        model: "gpt-4",
        messages: [{
          role: "system",
          content: "Tu es un assistant qui rédige des réponses professionnelles aux emails."
        }, {
          role: "user",
          content: `Rédige une réponse à cet email: ${steps.new_email.body}`
        }]
      }
    });
    
    // Envoyer la réponse
    await require("@pipedreamhq/platform").axios($, {
      method: "POST",
      url: "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
      headers: {
        "Authorization": `Bearer ${this.gmail.$auth.oauth_access_token}`,
      },
      data: {
        raw: Buffer.from(
          `To: ${steps.new_email.from}\\n` +
          `Subject: Re: ${steps.new_email.subject}\\n\\n` +
          response.choices[0].message.content
        ).toString('base64')
      }
    });
  }
});
"""
    }
}


# Prompts système pour l'assistant Pipedream
PIPEDREAM_SYSTEM_PROMPTS = {
    "workflow_generator": """Tu es un expert en automatisation Pipedream. Tu aides les utilisateurs à créer des workflows d'automatisation.

Tes compétences :
- Comprendre les besoins d'automatisation
- Proposer des architectures de workflows
- Générer du code JavaScript/Node.js pour Pipedream
- Expliquer comment connecter différentes applications
- Optimiser les workflows pour la performance

Format de réponse :
1. Résumé du workflow
2. Étapes détaillées
3. Code JavaScript complet
4. Instructions de configuration
5. Conseils et bonnes pratiques

Utilise toujours la syntaxe Pipedream moderne avec defineComponent.""",

    "troubleshooter": """Tu es un expert en débogage de workflows Pipedream. Tu aides à résoudre les problèmes d'automatisation.

Tes compétences :
- Identifier les erreurs dans les workflows
- Proposer des solutions
- Optimiser les performances
- Gérer les erreurs et les retry
- Debugger les problèmes d'API

Sois précis et fournis des solutions concrètes avec du code.""",

    "optimizer": """Tu es un expert en optimisation de workflows Pipedream. Tu aides à améliorer les automatisations existantes.

Tes compétences :
- Réduire le nombre d'étapes
- Optimiser les appels API
- Améliorer la gestion des erreurs
- Ajouter des logs et du monitoring
- Implémenter des retry et fallbacks

Propose toujours des améliorations concrètes avec du code."""
}


def get_template_categories():
    """Retourne les catégories de templates"""
    categories = set()
    for template in PIPEDREAM_TEMPLATES.values():
        categories.add(template["category"])
    return sorted(list(categories))


def get_templates_by_category(category):
    """Retourne les templates d'une catégorie"""
    return {
        name: template 
        for name, template in PIPEDREAM_TEMPLATES.items() 
        if template["category"] == category
    }


def search_templates(query):
    """Recherche des templates par mot-clé"""
    results = []
    query_lower = query.lower()
    
    for name, template in PIPEDREAM_TEMPLATES.items():
        if (query_lower in name.lower() or 
            query_lower in template["name"].lower() or 
            query_lower in template["description"].lower()):
            results.append({
                "id": name,
                "name": template["name"],
                "description": template["description"],
                "category": template["category"]
            })
    
    return results


def generate_workflow_prompt(description, apps=None):
    """Génère un prompt pour créer un workflow personnalisé"""
    prompt = f"""Crée un workflow Pipedream complet pour : {description}

"""
    
    if apps:
        prompt += f"Applications à utiliser : {', '.join(apps)}\n\n"
    
    prompt += """Fournis :
1. Architecture du workflow (étapes)
2. Code JavaScript complet avec defineComponent
3. Configuration des triggers et actions
4. Gestion des erreurs
5. Instructions de déploiement

Utilise les meilleures pratiques Pipedream."""
    
    return prompt
