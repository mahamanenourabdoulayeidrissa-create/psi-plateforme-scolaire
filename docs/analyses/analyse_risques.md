# ⚠️ Analyse des Risques — Plateforme Scolaire Intégrée (PSI)

> **Version :** 1.0.0  
> **Date :** Juin 2025  
> **Méthode :** Matrice Probabilité × Impact  
> **Business Analyst :** Claude (IA)  
> **Développeur :** Abdoulaye Mahamane Nour

---

## Légende

| Notation | Probabilité | Notation | Impact |
|----------|-------------|----------|--------|
| **F** | Faible (< 30%) | **F** | Faible — Perturbation mineure, corrigible facilement |
| **M** | Moyen (30–60%) | **M** | Moyen — Retard ou perte partielle de fonctionnalité |
| **H** | Haute (> 60%) | **H** | Haut — Blocage critique, perte de données ou abandon |

**Criticité** = Probabilité × Impact

| P\I | F | M | H |
|-----|---|---|---|
| **F** | 🟢 Faible | 🟡 Modéré | 🟠 Élevé |
| **M** | 🟡 Modéré | 🟠 Élevé | 🔴 Critique |
| **H** | 🟠 Élevé | 🔴 Critique | 🔴 Critique |

---

## Registre des Risques

---

### R-01 — Non-conformité du bulletin PDF au modèle officiel MEN Togo

| Attribut | Valeur |
|----------|--------|
| **Catégorie** | Réglementaire / Pédagogique |
| **Probabilité** | **M** (Moyen) |
| **Impact** | **H** (Haut) |
| **Criticité** | 🔴 **Critique** |

**Description :**  
Le MEN Togo impose un modèle précis pour les bulletins scolaires (structure, champs obligatoires, emplacement des signatures et cachets). Si le PDF généré par WeasyPrint ne correspond pas exactement au modèle officiel, les établissements partenaires ne pourront pas l'utiliser officiellement, ce qui invalide une fonctionnalité centrale de la PSI.

**Causes potentielles :**
- Absence d'un exemplaire officiel du modèle MEN entre les mains du développeur au moment de l'implémentation
- Variabilité régionale du modèle (Lomé vs régions intérieures)
- Évolution du modèle MEN non répercutée dans le système

**Plan de mitigation :**

| # | Action | Responsable | Échéance |
|---|--------|-------------|----------|
| M1 | Obtenir le modèle officiel MEN Togo auprès d'au moins 2 directeurs d'école pilotes | Dev + BA | Avant sprint pédagogique |
| M2 | Soumettre un premier prototype de bulletin pour validation par un directeur avant la mise en prod | Dev | Sprint 3 |
| M3 | Créer le template PDF en HTML/CSS (WeasyPrint) avec pixels-perfect matching du modèle | Dev | Sprint 3 |
| M4 | Paramétrer le modèle comme configurable (champs position, logo, signature) pour absorber les variations | Dev | Sprint 4 |

**Indicateur de suivi :** Validation écrite d'un directeur pilote sur le bulletin généré.

---

### R-02 — Instabilité de la connectivité internet dans les écoles togolaises

| Attribut | Valeur |
|----------|--------|
| **Catégorie** | Infrastructure / Technique |
| **Probabilité** | **H** (Haute) |
| **Impact** | **M** (Moyen) |
| **Criticité** | 🔴 **Critique** |

**Description :**  
La majorité des écoles privées togolaises opère sur des connexions mobiles 3G/4G instables ou des connexions ADSL de faible débit. Une application web-only sans gestion de l'offline exposera les enseignants à des pertes de saisie de notes, une frustration utilisateur élevée et un rejet de la solution.

**Causes potentielles :**
- Réseau mobile dégradé pendant les périodes de forte utilisation scolaire (fin de trimestre)
- Coupures électriques qui désactivent les routeurs WiFi des établissements
- Coût des données mobile limitant l'utilisation prolongée de l'app

**Plan de mitigation :**

| # | Action | Responsable | Échéance |
|---|--------|-------------|----------|
| M1 | Implémenter un mode offline via Service Worker (PWA) pour la saisie des notes sur React | Dev | Sprint 2 |
| M2 | Utiliser IndexedDB pour le stockage local et une queue de synchronisation | Dev | Sprint 2 |
| M3 | Afficher un indicateur de statut réseau visible en permanence dans l'UI | Dev | Sprint 2 |
| M4 | Optimiser toutes les réponses API (pagination, gzip, images lazy-load) | Dev | Sprint 1 |
| M5 | Tester l'application sur connexion simulée 2G (Chrome DevTools throttling) | Dev | Chaque sprint |

**Indicateur de suivi :** Tests d'intégration offline passants sur 100 % des scénarios de saisie de notes.

---

### R-03 — Échecs d'intégration Kkiapay (Mobile Money)

| Attribut | Valeur |
|----------|--------|
| **Catégorie** | Technique / Financier |
| **Probabilité** | **M** (Moyen) |
| **Impact** | **H** (Haut) |
| **Criticité** | 🔴 **Critique** |

**Description :**  
L'intégration Kkiapay est un pilier différenciateur de la PSI. Des problèmes d'API (timeouts, callbacks non reçus, bascule sandbox → production), des pannes Kkiapay, ou des litiges sur les transactions peuvent créer des incohérences entre le paiement réel effectué par le parent et les données enregistrées dans la plateforme.

**Causes potentielles :**
- Callback webhook Kkiapay non reçu (paiement débité mais non enregistré côté PSI)
- Délais de confirmation Mobile Money (MTN/Moov) supérieurs au timeout applicatif
- Modifications d'API Kkiapay non anticipées
- Erreurs de configuration clé publique/privée en production

**Plan de mitigation :**

| # | Action | Responsable | Échéance |
|---|--------|-------------|----------|
| M1 | Implémenter un mécanisme de vérification de paiement (polling + webhook combiné) | Dev | Sprint financier |
| M2 | Stocker chaque initiation de transaction avec statut "en attente" avant confirmation | Dev | Sprint financier |
| M3 | Créer une page d'administration "transactions en suspens" pour résolution manuelle | Dev | Sprint financier |
| M4 | Tester exhaustivement en sandbox avec tous les scénarios (succès, échec, timeout) | Dev | Sprint financier |
| M5 | Établir un contact support Kkiapay Togo avant le lancement production | Dev + BA | Avant lancement |
| M6 | Ne jamais afficher "paiement réussi" au parent avant confirmation webhook | Dev | Sprint financier |

**Indicateur de suivi :** Zéro transaction orpheline (initiée sans statut final) après 48h en production.

---

### R-04 — Résistance au changement des enseignants et directeurs

| Attribut | Valeur |
|----------|--------|
| **Catégorie** | Humain / Adoption |
| **Probabilité** | **H** (Haute) |
| **Impact** | **M** (Moyen) |
| **Criticité** | 🔴 **Critique** |

**Description :**  
Les enseignants et directeurs togolais ont des pratiques ancrées dans le papier. La PSI représente un changement de workflow significatif. Sans accompagnement, le taux d'adoption sera faible, les données saisies seront incomplètes (bulletins non générables), et les écoles pourraient abandonner la solution.

**Causes potentielles :**
- Faible maîtrise informatique de certains enseignants
- Perception de la saisie numérique comme une charge supplémentaire
- Crainte de perte de données ou de piratage
- Absence de support technique local

**Plan de mitigation :**

| # | Action | Responsable | Échéance |
|---|--------|-------------|----------|
| M1 | Concevoir une UI ultra-simplifiée pour la saisie des notes (max 3 clics pour noter un élève) | Dev | Sprint pédagogique |
| M2 | Créer des guides PDF + vidéos tutoriels en français pour chaque profil utilisateur | BA + Dev | Avant lancement |
| M3 | Organiser une session de formation de 2h en présentiel dans chaque école pilote | Dev | Semaine lancement |
| M4 | Prévoir un numéro WhatsApp de support réactif (< 4h de réponse) | Dev | Lancement |
| M5 | Implémenter des messages d'aide contextuelle dans l'interface (tooltips, tutoriels intégrés) | Dev | Sprint 4 |

**Indicateur de suivi :** 80 % des enseignants des écoles pilotes ont saisi leurs notes T1 via la PSI.

---

### R-05 — Fuite ou perte de données scolaires et financières

| Attribut | Valeur |
|----------|--------|
| **Catégorie** | Sécurité / RGPD |
| **Probabilité** | **F** (Faible) |
| **Impact** | **H** (Haut) |
| **Criticité** | 🟠 **Élevé** |

**Description :**  
La PSI héberge des données personnelles d'élèves mineurs (notes, absences, informations familiales) ainsi que des données financières sensibles (transactions Mobile Money, numéros de téléphone). Une violation de données ou une perte suite à une défaillance d'infrastructure entraînerait des conséquences légales, financières et réputationnelles graves.

**Causes potentielles :**
- Serveur compromis (injection SQL, accès non autorisé)
- Pas de backup configuré en production
- Credentials codés en dur dans le code source
- Accès admin partagé entre plusieurs personnes sans logs

**Plan de mitigation :**

| # | Action | Responsable | Échéance |
|---|--------|-------------|----------|
| M1 | Stocker tous les secrets (clés API, BDD) dans des variables d'environnement / secrets manager | Dev | Sprint 1 |
| M2 | Configurer des sauvegardes automatiques quotidiennes PostgreSQL vers un stockage séparé | Dev | Avant lancement |
| M3 | Activer l'authentification 2FA pour tous les comptes directeurs | Dev | Sprint sécurité |
| M4 | Auditer les permissions Django avec principle of least privilege | Dev | Sprint sécurité |
| M5 | Implémenter un journal d'audit complet pour toutes les opérations financières | Dev | Sprint financier |
| M6 | Effectuer un scan de vulnérabilités (OWASP Top 10) avant mise en production | Dev | Pré-lancement |

**Indicateur de suivi :** Zéro vulnérabilité critique remontée par l'audit OWASP pré-lancement.

---

### R-06 — Dépassement du budget ou des délais de développement

| Attribut | Valeur |
|----------|--------|
| **Catégorie** | Projet / Planning |
| **Probabilité** | **M** (Moyen) |
| **Impact** | **M** (Moyen) |
| **Criticité** | 🟠 **Élevé** |

**Description :**  
La PSI couvre 4 modules, 3 interfaces (React, Flutter, SMS), 2 intégrations tierces (Kkiapay, Africa's Talking) et des contraintes réglementaires. Pour un développeur solo, le risque de sous-estimation est élevé, pouvant conduire à des fonctionnalités livrées avec retard ou partiellement implémentées au moment du lancement avec les écoles pilotes.

**Causes potentielles :**
- Scope creep : les directeurs d'école ajoutent des demandes en cours de projet
- Complexité sous-estimée de l'intégration Kkiapay ou de la génération PDF conforme MEN
- Bugs inattendus sur l'implémentation offline Flutter
- Dépendance à un tiers (Kkiapay, Africa's Talking) qui ralentit les tests

**Plan de mitigation :**

| # | Action | Responsable | Échéance |
|---|--------|-------------|----------|
| M1 | Prioriser rigoureusement les MUST HAVE vs SHOULD HAVE (cf. Matrice MoSCoW du CDC) | Dev + BA | Avant sprint 1 |
| M2 | Découper en sprints de 2 semaines avec livrables démontrables à chaque fin de sprint | Dev | Continu |
| M3 | Geler le scope v1.0 contractuellement avec les écoles pilotes avant le début du développement | BA | Avant démarrage |
| M4 | Développer d'abord le MVP (inscription + notes + bulletins + paiements espèces) avant les intégrations tierces | Dev | Sprint 1-2 |
| M5 | Maintenir un backlog priorisé et visible (GitHub Projects ou Trello) | Dev | Continu |
| M6 | Prévoir un buffer de 20 % sur les estimations de délais pour chaque sprint | Dev | Planification |

**Indicateur de suivi :** Vélocité de sprint stable (pas plus de 20 % d'écart entre estimé et réalisé sur 3 sprints consécutifs).

---

### R-07 — Adoption faible de l'app Flutter par les parents

| Attribut | Valeur |
|----------|--------|
| **Catégorie** | Adoption / Produit |
| **Probabilité** | **M** (Moyen) |
| **Impact** | **M** (Moyen) |
| **Criticité** | 🟠 **Élevé** |

**Description :**  
L'espace parents Flutter est un vecteur de valeur fort (paiements, bulletins). Mais si les parents ne téléchargent pas l'app, ne l'utilisent pas, ou ne la trouvent pas assez fiable, la PSI perd une partie importante de son ROI pour les écoles partenaires.

**Causes potentielles :**
- Smartphone d'entrée de gamme incompatible avec l'app
- Manque de sensibilisation des parents à l'existence de l'app
- Interface trop complexe pour des utilisateurs peu habitués aux apps
- Méfiance vis-à-vis de la sécurité du paiement mobile

**Plan de mitigation :**

| # | Action | Responsable | Échéance |
|---|--------|-------------|----------|
| M1 | Garantir la compatibilité Android 5.0+ (couvre 95 % du parc togolais) | Dev | Sprint Flutter |
| M2 | Concevoir un onboarding de 3 écrans maximum avec une démo interactive | Dev | Sprint Flutter |
| M3 | Permettre aux écoles d'envoyer le lien de téléchargement via SMS (Africa's Talking) à tous les parents | Dev | Sprint lancement |
| M4 | Maintenir le canal SMS comme fallback complet (parents sans smartphone ne perdent rien) | Dev | Sprint 1 |
| M5 | Ajouter un badge "Paiement sécurisé Kkiapay" visible dans l'écran de paiement | Dev | Sprint Flutter |

**Indicateur de suivi :** 50 % des parents d'une école pilote téléchargent et activent l'app dans les 30 jours suivant le lancement.

---

### R-08 — Indisponibilité ou surcoût de l'API Africa's Talking

| Attribut | Valeur |
|----------|--------|
| **Catégorie** | Dépendance tierce / Financier |
| **Probabilité** | **F** (Faible) |
| **Impact** | **M** (Moyen) |
| **Criticité** | 🟡 **Modéré** |

**Description :**  
Africa's Talking est le fournisseur SMS retenu. Une panne, une révision tarifaire ou une limitation des SMS vers les numéros togolais pourrait rendre l'envoi de notifications (absences, impayés) indisponible, ce qui affecte directement la proposition de valeur de la PSI.

**Causes potentielles :**
- Panne de l'infrastructure Africa's Talking en Afrique de l'Ouest
- Changement de tarification SMS Togo (facturation à l'unité)
- Volume de SMS dépassant le budget alloué en fin de mois
- Délai de livraison SMS > 5 minutes rendant les alertes inefficaces

**Plan de mitigation :**

| # | Action | Responsable | Échéance |
|---|--------|-------------|----------|
| M1 | Implémenter une abstraction SMS (service layer) permettant de changer de fournisseur sans modifier le code métier | Dev | Sprint 1 |
| M2 | Implémenter un système de batching des SMS (regrouper plusieurs alertes en un message) pour réduire les coûts | Dev | Sprint notifications |
| M3 | Configurer des alertes de consommation SMS (seuil à 80 % du budget mensuel) | Dev | Avant lancement |
| M4 | Identifier un fournisseur alternatif (ex. Vonage, Twilio Togo) comme backup | BA | Avant lancement |
| M5 | Logger tous les SMS envoyés avec le statut de livraison pour détecter les problèmes opérateurs | Dev | Sprint notifications |

**Indicateur de suivi :** Taux de livraison SMS > 95 % sur les numéros togolais (MTN + Moov).

---

## Synthèse des Risques — Heat Map

```
         IMPACT
              F        M        H
         ┌────────┬────────┬────────┐
    H    │        │  R-04  │  R-02  │
         ├────────┼────────┼────────┤
    M    │        │ R-06   │ R-01   │
 P       │        │ R-07   │ R-03   │
         ├────────┼────────┼────────┤
    F    │        │  R-08  │  R-05  │
         └────────┴────────┴────────┘

🔴 Critique  : R-01, R-02, R-03, R-04
🟠 Élevé     : R-05, R-06, R-07
🟡 Modéré    : R-08
```

---

## Plan d'action prioritaire

| Priorité | Risque | Action immédiate | Délai |
|----------|--------|------------------|-------|
| 🔴 P1 | R-01 Bulletin MEN | Obtenir modèle officiel MEN auprès des écoles pilotes | J+7 |
| 🔴 P2 | R-02 Connexion | Implémenter le mode offline en sprint 1 | Sprint 1 |
| 🔴 P3 | R-03 Kkiapay | Tester tous les scénarios de paiement en sandbox | Sprint financier |
| 🔴 P4 | R-04 Adoption | Planifier sessions de formation et produire les guides | Avant lancement |
| 🟠 P5 | R-05 Sécurité | Audit OWASP Top 10 pré-lancement | Pré-lancement |
| 🟠 P6 | R-06 Planning | Geler le scope MoSCoW MUST avec les pilotes | Avant sprint 1 |
| 🟠 P7 | R-07 App parents | Tester sur devices Android bas de gamme dès sprint Flutter | Sprint Flutter |
| 🟡 P8 | R-08 SMS | Implémenter abstraction SMS + monitoring coût | Sprint 1 |

---

## Matrice de Responsabilités (RACI — Risques)

| Risque | Développeur | Business Analyst | Directeur École |
|--------|-------------|------------------|-----------------|
| R-01 Bulletin MEN | Accountable | Responsible | Consulted |
| R-02 Connectivité | Accountable | Informed | Consulted |
| R-03 Kkiapay | Accountable | Consulted | Informed |
| R-04 Adoption | Accountable | Responsible | Accountable |
| R-05 Sécurité | Accountable | Informed | Informed |
| R-06 Planning | Accountable | Responsible | Consulted |
| R-07 App parents | Accountable | Consulted | Responsible |
| R-08 SMS | Accountable | Consulted | Informed |

---

*Document produit par Claude (Business Analyst IA) — PSI v1.0.0*  
*À réviser à chaque fin de sprint et lors de l'onboarding d'une nouvelle école pilote*