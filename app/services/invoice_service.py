"""
Service de génération de factures PDF
Génère des factures professionnelles pour les commandes
"""
import os
from datetime import datetime
from typing import Dict, Any, Optional


class InvoiceService:
    """Service de génération de factures PDF"""
    
    def __init__(self):
        self.output_dir = "generated/invoices"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_invoice(
        self,
        order_id: int,
        order_data: Dict[str, Any],
        user_data: Dict[str, Any]
    ) -> str:
        """
        Générer une facture PDF pour une commande
        
        Args:
            order_id: ID de la commande
            order_data: Données de la commande
            user_data: Données du client
            
        Returns:
            Chemin vers le fichier PDF généré
        """
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import cm
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
            from reportlab.lib import colors
            
            # Nom du fichier
            invoice_number = f"INV-{order_id:06d}"
            filename = f"facture_{invoice_number}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # Créer le document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            # Styles
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=20,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#34495e'),
                spaceAfter=10
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#2c3e50')
            )
            
            # Contenu
            story = []
            
            # En-tête
            story.append(Paragraph("FACTURE", title_style))
            story.append(Spacer(1, 0.5*cm))
            
            # Informations entreprise
            company_info = """
            <b>WeBox Multi-IA</b><br/>
            123 Avenue de l'Innovation<br/>
            75001 Paris, France<br/>
            SIRET: 123 456 789 00012<br/>
            TVA: FR12345678900
            """
            story.append(Paragraph(company_info, normal_style))
            story.append(Spacer(1, 0.5*cm))
            
            # Informations facture et client côte à côte
            invoice_info = [
                [
                    Paragraph("<b>Numéro de facture:</b>", normal_style),
                    Paragraph(invoice_number, normal_style)
                ],
                [
                    Paragraph("<b>Date:</b>", normal_style),
                    Paragraph(datetime.utcnow().strftime("%d/%m/%Y"), normal_style)
                ],
                [
                    Paragraph("<b>Commande N°:</b>", normal_style),
                    Paragraph(f"CMD-{order_id:06d}", normal_style)
                ]
            ]
            
            invoice_table = Table(invoice_info, colWidths=[5*cm, 10*cm])
            invoice_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ]))
            
            story.append(invoice_table)
            story.append(Spacer(1, 0.5*cm))
            
            # Informations client
            story.append(Paragraph("<b>Facturé à:</b>", heading_style))
            client_info = f"""
            {user_data.get('name', 'Client')}<br/>
            {user_data.get('email', '')}<br/>
            {user_data.get('address', 'Adresse non renseignée')}
            """
            story.append(Paragraph(client_info, normal_style))
            story.append(Spacer(1, 1*cm))
            
            # Tableau des articles
            story.append(Paragraph("<b>Détail de la commande:</b>", heading_style))
            story.append(Spacer(1, 0.3*cm))
            
            # En-tête du tableau
            items_data = [
                [
                    Paragraph("<b>Article</b>", normal_style),
                    Paragraph("<b>Quantité</b>", normal_style),
                    Paragraph("<b>Prix unitaire</b>", normal_style),
                    Paragraph("<b>Total</b>", normal_style)
                ]
            ]
            
            # Articles
            items = order_data.get('items', [])
            subtotal = 0
            
            for item in items:
                item_name = item.get('name', 'Article')
                quantity = item.get('quantity', 1)
                price = item.get('price', 0)
                total = quantity * price
                subtotal += total
                
                items_data.append([
                    Paragraph(item_name, normal_style),
                    Paragraph(str(quantity), normal_style),
                    Paragraph(f"{price:.2f}€", normal_style),
                    Paragraph(f"{total:.2f}€", normal_style)
                ])
            
            items_table = Table(items_data, colWidths=[8*cm, 2*cm, 3*cm, 3*cm])
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(items_table)
            story.append(Spacer(1, 0.5*cm))
            
            # Totaux
            discount = order_data.get('discount', 0)
            shipping = order_data.get('shipping', 0)
            total = subtotal - discount + shipping
            
            totals_data = [
                [Paragraph("<b>Sous-total:</b>", normal_style), Paragraph(f"{subtotal:.2f}€", normal_style)]
            ]
            
            if discount > 0:
                totals_data.append([
                    Paragraph("<b>Réduction:</b>", normal_style),
                    Paragraph(f"-{discount:.2f}€", normal_style)
                ])
            
            if shipping > 0:
                totals_data.append([
                    Paragraph("<b>Frais de port:</b>", normal_style),
                    Paragraph(f"{shipping:.2f}€", normal_style)
                ])
            
            totals_data.append([
                Paragraph("<b>TOTAL TTC:</b>", heading_style),
                Paragraph(f"<b>{total:.2f}€</b>", heading_style)
            ])
            
            totals_table = Table(totals_data, colWidths=[13*cm, 3*cm])
            totals_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
                ('TOPPADDING', (0, -1), (-1, -1), 12),
            ]))
            
            story.append(totals_table)
            story.append(Spacer(1, 1*cm))
            
            # Pied de page
            footer = """
            <b>Conditions de paiement:</b> Paiement à réception<br/>
            <b>Méthode de paiement:</b> {}<br/>
            <br/>
            Merci pour votre commande!<br/>
            Pour toute question, contactez-nous à support@webox.com
            """.format(order_data.get('payment_method', 'Carte bancaire'))
            
            story.append(Paragraph(footer, normal_style))
            
            # Générer le PDF
            doc.build(story)
            
            return filepath
            
        except ImportError:
            # Fallback: créer un fichier texte
            print("ReportLab non installé, création d'un fichier texte")
            txt_path = os.path.join(self.output_dir, f"facture_{order_id}.txt")
            
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"FACTURE N° INV-{order_id:06d}\n")
                f.write(f"Date: {datetime.utcnow().strftime('%d/%m/%Y')}\n\n")
                f.write(f"Client: {user_data.get('name', 'Client')}\n")
                f.write(f"Email: {user_data.get('email', '')}\n\n")
                f.write("Articles:\n")
                
                for item in order_data.get('items', []):
                    f.write(f"- {item.get('name')}: {item.get('quantity')} x {item.get('price')}€\n")
                
                f.write(f"\nTotal: {order_data.get('total', 0):.2f}€\n")
            
            return txt_path
            
        except Exception as e:
            print(f"Erreur lors de la génération de la facture: {e}")
            return None


# Instance globale
invoice_service = InvoiceService()
