# 📋 Cahier des Charges Fonctionnel — Plateforme Scolaire Intégrée (PSI)

> **Version :** 1.0.0  
> **Date :** Juin 2025  
> **Business Analyst :** Claude (IA)  
> **Développeur :** Abdoulaye Mahamane Nour  
> **Statut :** Draft — En révision  

---

## Table des Matières

1. [Présentation du projet](#1-présentation-du-projet)
2. [Périmètre fonctionnel](#2-périmètre-fonctionnel)
3. [Acteurs du système](#3-acteurs-du-système)
4. [User Stories](#4-user-stories)
   - [4.1 Module Administration](#41-module-administration)
   - [4.2 Module Pédagogique](#42-module-pédagogique)
   - [4.3 Module Financier](#43-module-financier)
   - [4.4 Espace Parents](#44-espace-parents)
5. [Matrice de priorités MoSCoW](#5-matrice-de-priorités-moscow)
6. [Règles de Gestion](#6-règles-de-gestion)
7. [Exigences Non-Fonctionnelles](#7-exigences-non-fonctionnelles)
8. [Contraintes contexte togolais](#8-contraintes-contexte-togolais)
9. [Architecture technique synthèse](#9-architecture-technique-synthèse)

---

## 1. Présentation du Projet

### 1.1 Contexte

Les écoles privées au Togo gèrent encore majoritairement leurs activités scolaires (inscriptions, notes, paiements, communications parents) via des supports papier ou des outils non intégrés. Ce cloisonnement génère des pertes de données, des retards dans la communication avec les familles et une opacité financière préjudiciable à la bonne gouvernance des établissements.

La **Plateforme Scolaire Intégrée (PSI)** est une solution numérique complète — web + mobile — conçue pour digitaliser l'intégralité des processus administratifs, pédagogiques et financiers des écoles privées togolaises, dans le strict respect des normes du **Ministère de l'Éducation Nationale (MEN) du Togo**.

### 1.2 Objectifs

| # | Objectif | Indicateur de succès |
|---|----------|----------------------|
| O1 | Centraliser la gestion scolaire | 100 % des données dans une seule plateforme |
| O2 | Générer des bulletins conformes MEN Togo | Bulletins acceptés sans retouche par les chefs d'établissement |
| O3 | Automatiser les alertes financières | Taux de recouvrement de scolarité amélioré de 20 % |
| O4 | Connecter les parents en temps réel | 80 % des parents actifs sur l'app ou notifiés par SMS |
| O5 | Réduire la charge administrative | Réduction de 50 % du temps de saisie vs. méthode papier |

### 1.3 Stack Technique

| Couche | Technologie |
|--------|-------------|
| Backend | Django (Python) + Django REST Framework |
| Frontend Web | React.js |
| Application Mobile | Flutter (iOS + Android) |
| Base de données | PostgreSQL |
| Paiements | Kkiapay (Mobile Money) |
| SMS | Africa's Talking API |
| Génération PDF | WeasyPrint / ReportLab |

---

## 2. Périmètre Fonctionnel

```
┌─────────────────────────────────────────────────────────┐
│              PLATEFORME SCOLAIRE INTÉGRÉE (PSI)         │
│                                                         │
│  ┌──────────────────┐     ┌──────────────────────────┐  │
│  │  MODULE ADMIN     │     │   MODULE PÉDAGOGIQUE     │  │
│  │  - Élèves         │     │   - Notes coefficientées │  │
│  │  - Classes        │     │   - Bulletins PDF MEN    │  │
│  │  - Enseignants    │     │   - Absences + alertes   │  │
│  │  - Établissement  │     │   - Calendrier scolaire  │  │
│  └──────────────────┘     └──────────────────────────┘  │
│                                                         │
│  ┌──────────────────┐     ┌──────────────────────────┐  │
│  │  MODULE FINANCIER │     │   ESPACE PARENTS         │  │
│  │  - Scolarité      │     │   - App Flutter          │  │
│  │  - Kkiapay MoMo   │     │   - Notes / Bulletins    │  │
│  │  - SMS impayés    │     │   - Paiements MoMo       │  │
│  │  - Tableaux bord  │     │   - Messagerie           │  │
│  └──────────────────┘     └──────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Acteurs du Système

| Acteur | Rôle | Interface | Droits |
|--------|------|-----------|--------|
| **Directeur** | Administration totale de l'établissement | Web (React) | CRUD complet sur tous les modules |
| **Enseignant** | Saisie des notes et des absences | Web (React) | Lecture classes assignées, écriture notes/absences |
| **Secrétaire** | Inscriptions et gestion des paiements | Web (React) | CRUD élèves, inscriptions, paiements |
| **Parent (smartphone)** | Suivi enfant, paiement scolarité | Flutter (mobile) | Lecture seule + paiement Mobile Money |
| **Parent (sans smartphone)** | Réception d'informations critiques | SMS | Notifications automatiques uniquement |

---

## 4. User Stories

> **Format :** En tant que `[acteur]` / Je veux `[action]` / Afin de `[bénéfice]`  
> **Critères d'acceptation :** Format GIVEN / WHEN / THEN

---

### 4.1 Module Administration

---

#### US-01 — Inscription d'un élève

> **En tant que** Secrétaire  
> **Je veux** inscrire un nouvel élève en renseignant ses informations personnelles et en l'affectant à une classe  
> **Afin de** créer son dossier numérique complet dès son entrée dans l'établissement

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-01-1 | GIVEN un formulaire d'inscription ouvert, WHEN la secrétaire saisit nom, prénom, date de naissance, sexe, classe, contacts parents et valide, THEN le dossier est créé avec un identifiant unique et apparaît dans la liste de la classe |
| CA-01-2 | GIVEN un formulaire incomplet (champ obligatoire manquant), WHEN la secrétaire clique "Valider", THEN le système affiche une erreur ciblée par champ sans effacer les données saisies |
| CA-01-3 | GIVEN un élève inscrit, WHEN la secrétaire consulte sa fiche, THEN elle voit les informations complètes, la classe affectée, le statut financier (solde dû) et l'historique de paiements |
| CA-01-4 | GIVEN une classe déjà au maximum d'élèves configuré, WHEN la secrétaire tente d'y inscrire un élève supplémentaire, THEN un avertissement est affiché (dépassement de capacité) mais l'inscription reste possible avec confirmation explicite |
| CA-01-5 | GIVEN un élève nouvellement inscrit, WHEN l'inscription est validée, THEN les créances de scolarité (3 tranches) sont automatiquement générées selon la grille tarifaire de la classe |

---

#### US-02 — Gestion des classes et affectation des enseignants

> **En tant que** Directeur  
> **Je veux** créer des classes et affecter des enseignants à des matières par classe  
> **Afin de** structurer l'organisation pédagogique de l'établissement pour l'année scolaire

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-02-1 | GIVEN le module administration, WHEN le directeur crée une classe (niveau, libellé, effectif max, titulaire), THEN la classe est disponible pour les inscriptions et dans les emplois du temps |
| CA-02-2 | GIVEN une classe créée, WHEN le directeur affecte un enseignant à une matière avec un coefficient, THEN l'enseignant voit cette classe/matière dans son tableau de bord |
| CA-02-3 | GIVEN un enseignant affecté à plusieurs classes, WHEN il se connecte, THEN il ne voit QUE les classes et matières qui lui sont assignées |
| CA-02-4 | GIVEN une affectation en cours d'année scolaire, WHEN le directeur la modifie, THEN l'historique de l'ancienne affectation est conservé et les notes déjà saisies restent intactes |

---

#### US-03 — Tableau de bord de direction

> **En tant que** Directeur  
> **Je veux** accéder à un tableau de bord synthétique de l'établissement  
> **Afin de** piloter en temps réel les indicateurs clés (effectifs, finances, assiduité, performances)

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-03-1 | GIVEN le tableau de bord, WHEN le directeur s'y connecte, THEN il voit : effectif total, taux de recouvrement de scolarité, nombre d'absences non justifiées du jour, et moyenne générale par classe |
| CA-03-2 | GIVEN le tableau de bord, WHEN le directeur clique sur un indicateur, THEN il accède au détail complet filtrable par classe, trimestre, période |
| CA-03-3 | GIVEN la fin d'un trimestre, WHEN le directeur consulte le tableau de bord, THEN il peut exporter un rapport PDF de synthèse de l'établissement |
| CA-03-4 | GIVEN un indicateur critique (ex. taux impayés > 30 %), THEN il est signalé visuellement par une alerte colorée sur le tableau de bord |

---

#### US-04 — Gestion du profil établissement

> **En tant que** Directeur  
> **Je veux** configurer les paramètres de mon établissement (nom, logo, grilles tarifaires, année scolaire)  
> **Afin de** personnaliser la plateforme et générer des documents officiels conformes à mon école

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-04-1 | GIVEN le module paramètres, WHEN le directeur renseigne le nom officiel, l'adresse, le logo et le numéro d'autorisation MEN, THEN ces informations apparaissent sur tous les documents générés (bulletins, reçus) |
| CA-04-2 | GIVEN la configuration des tranches, WHEN le directeur définit 3 tranches avec leurs montants et échéances, THEN ces tranches sont automatiquement appliquées à tous les nouveaux inscrits |
| CA-04-3 | GIVEN un changement d'année scolaire, WHEN le directeur initialise la nouvelle année, THEN les classes sont recréées, les élèves peuvent être réaffectés et l'historique de l'année précédente est archivé |
| CA-04-4 | GIVEN la configuration des matières, WHEN le directeur définit les coefficients par matière par niveau, THEN ces coefficients sont appliqués automatiquement dans le calcul des moyennes |

---

### 4.2 Module Pédagogique

---

#### US-05 — Saisie des notes par l'enseignant

> **En tant que** Enseignant  
> **Je veux** saisir les notes de mes élèves par matière, par trimestre et par type d'évaluation  
> **Afin de** alimenter les bulletins scolaires et permettre le suivi des performances

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-05-1 | GIVEN la liste des élèves d'une classe/matière, WHEN l'enseignant saisit une note (0–20) et son coefficient, THEN la note est enregistrée avec la date, le type d'évaluation et le trimestre |
| CA-05-2 | GIVEN une note hors plage [0–20], WHEN l'enseignant tente de valider, THEN un message d'erreur bloquant s'affiche |
| CA-05-3 | GIVEN des notes saisies, WHEN l'enseignant consulte le récapitulatif, THEN la moyenne automatique de chaque élève pour la matière est calculée en temps réel selon la formule Σ(note × coeff) / Σ(coeff) |
| CA-05-4 | GIVEN des notes validées et le trimestre clôturé, WHEN l'enseignant tente de les modifier, THEN une demande d'autorisation au directeur est requise avec justification |
| CA-05-5 | GIVEN une saisie en cours, WHEN la connexion internet est perdue, THEN les notes sont sauvegardées localement (mode offline) et synchronisées à la reconnexion |

---

#### US-06 — Génération des bulletins scolaires PDF

> **En tant que** Directeur ou Secrétaire  
> **Je veux** générer les bulletins trimestriels en PDF conformes au modèle officiel MEN Togo  
> **Afin de** les distribuer aux familles et remplir l'obligation légale de l'établissement

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-06-1 | GIVEN toutes les notes du trimestre saisies, WHEN le directeur lance la génération des bulletins, THEN un PDF conforme au modèle MEN est généré pour chaque élève avec : en-tête établissement, notes par matière, coefficients, moyennes, mention, classement, et signature |
| CA-06-2 | GIVEN un bulletin généré, THEN la mention est calculée automatiquement selon les seuils officiels (TB ≥16, B ≥14, AB ≥12, P ≥10, I <10) |
| CA-06-3 | GIVEN plusieurs élèves dans une classe, WHEN la génération est lancée, THEN le classement est calculé et affiché sur chaque bulletin (rang / effectif) |
| CA-06-4 | GIVEN un bulletin généré, WHEN un parent y accède via l'app Flutter, THEN il peut le visualiser et le télécharger au format PDF |
| CA-06-5 | GIVEN la génération d'un lot de bulletins, THEN elle s'effectue en arrière-plan et l'utilisateur est notifié par une alerte lorsque tous les PDF sont disponibles |

---

#### US-07 — Gestion des absences et alertes automatiques

> **En tant que** Enseignant  
> **Je veux** enregistrer les absences de mes élèves à chaque cours  
> **Afin de** déclencher des alertes automatiques aux parents en cas d'absences répétées non justifiées

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-07-1 | GIVEN une liste de classe, WHEN l'enseignant marque un élève absent, THEN l'absence est horodatée, associée à la matière et au créneau horaire |
| CA-07-2 | GIVEN une absence enregistrée, WHEN le parent ou la secrétaire fournit un justificatif, THEN l'absence est marquée "justifiée" et ne compte pas dans le décompte d'alertes |
| CA-07-3 | GIVEN un élève atteignant 3 absences non justifiées sur la période, WHEN ce seuil est atteint, THEN un SMS d'alerte est automatiquement envoyé au(x) parent(s) via Africa's Talking |
| CA-07-4 | GIVEN un SMS d'alerte envoyé, THEN il est journalisé dans le système avec la date, le numéro destinataire et le statut de livraison (succès/échec) |
| CA-07-5 | GIVEN un rapport d'absences, WHEN le directeur le consulte, THEN il peut filtrer par élève, classe, période et voir le ratio absences justifiées / non justifiées |

---

#### US-08 — Consultation du carnet de notes par l'enseignant

> **En tant que** Enseignant  
> **Je veux** consulter l'historique complet des notes de mes élèves sur l'année  
> **Afin de** identifier les élèves en difficulté et adapter ma pédagogie

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-08-1 | GIVEN le carnet de notes, WHEN l'enseignant sélectionne une classe et un trimestre, THEN il voit la liste de tous les élèves avec leurs notes par évaluation et leur moyenne calculée |
| CA-08-2 | GIVEN le carnet de notes, WHEN l'enseignant active la vue "évolution", THEN un graphique montre la progression de chaque élève sur les trimestres saisis |
| CA-08-3 | GIVEN le carnet de notes, WHEN l'enseignant l'exporte, THEN un fichier CSV ou PDF est généré avec toutes les données |
| CA-08-4 | GIVEN des notes manquantes (élève non noté), THEN ces cases sont signalées visuellement pour éviter les bulletins incomplets |

---

### 4.3 Module Financier

---

#### US-09 — Enregistrement des paiements de scolarité

> **En tant que** Secrétaire  
> **Je veux** enregistrer les paiements de scolarité (espèces ou Mobile Money) par élève et par tranche  
> **Afin de** suivre en temps réel le recouvrement des frais scolaires

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-09-1 | GIVEN la fiche financière d'un élève, WHEN la secrétaire enregistre un paiement (montant, mode, date), THEN le solde restant est mis à jour en temps réel et un reçu PDF est généré automatiquement |
| CA-09-2 | GIVEN un paiement Mobile Money via Kkiapay, WHEN la transaction est confirmée par l'API, THEN le paiement est enregistré automatiquement sans saisie manuelle |
| CA-09-3 | GIVEN un reçu généré, THEN il comporte : n° de reçu unique, nom élève, classe, montant payé, tranche concernée, solde restant, date, tampon établissement |
| CA-09-4 | GIVEN un paiement enregistré, THEN il ne peut pas être supprimé mais peut être annulé avec justification et traçabilité complète |
| CA-09-5 | GIVEN un paiement partiel, WHEN il est enregistré, THEN le système calcule et affiche la tranche concernée, le montant restant dû sur cette tranche et le total annuel restant |

---

#### US-10 — Alertes SMS pour impayés

> **En tant que** Système automatique (planificateur)  
> **Je veux** envoyer des rappels SMS aux parents d'élèves dont la scolarité est impayée après échéance  
> **Afin de** améliorer le taux de recouvrement sans mobiliser constamment la secrétaire

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-10-1 | GIVEN une tranche de scolarité dont la date d'échéance est dépassée de 7 jours, WHEN le planificateur s'exécute (tâche quotidienne), THEN un SMS de rappel est envoyé au(x) contact(s) parent(s) de l'élève concerné |
| CA-10-2 | GIVEN un SMS d'impayé envoyé, THEN le message inclut : nom de l'élève, montant dû, tranche concernée, et un contact pour paiement |
| CA-10-3 | GIVEN un parent ayant reçu une alerte et effectuant un paiement, WHEN le paiement est validé, THEN plus aucun SMS de rappel n'est envoyé pour cette tranche |
| CA-10-4 | GIVEN le tableau de bord financier, WHEN le directeur le consulte, THEN il voit le nombre de SMS envoyés, le taux de réponse (paiement suivant SMS) et les coûts Africa's Talking |

---

#### US-11 — Tableau de bord financier

> **En tant que** Directeur  
> **Je veux** consulter un tableau de bord financier complet par classe, par tranche et par période  
> **Afin de** piloter la santé financière de l'établissement et anticiper les déficits de trésorerie

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-11-1 | GIVEN le tableau de bord financier, THEN il affiche : total attendu vs. total encaissé, taux de recouvrement (%), liste des élèves débiteurs, et top 10 des montants les plus élevés |
| CA-11-2 | GIVEN le tableau de bord, WHEN le directeur filtre par classe, THEN les indicateurs se recalculent pour la sélection |
| CA-11-3 | GIVEN le tableau de bord, WHEN le directeur clique sur un élève débiteur, THEN il accède à son historique de paiements complet et peut envoyer manuellement un SMS de rappel |
| CA-11-4 | GIVEN le tableau de bord, WHEN le directeur exporte les données, THEN un fichier Excel avec tous les paiements et soldes est généré |

---

#### US-12 — Paiement Mobile Money depuis l'app parent

> **En tant que** Parent (avec smartphone)  
> **Je veux** payer la scolarité de mon enfant directement depuis l'application mobile via Mobile Money  
> **Afin de** régler les frais sans me déplacer à l'école et recevoir une confirmation immédiate

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-12-1 | GIVEN l'espace financier de l'app Flutter, WHEN le parent consulte l'écran "Scolarité", THEN il voit les 3 tranches avec leur statut (payé / dû / en retard) et les montants |
| CA-12-2 | GIVEN une tranche impayée, WHEN le parent clique "Payer", THEN la widget Kkiapay s'ouvre avec le montant pré-renseigné et le parent finalise via son opérateur Mobile Money |
| CA-12-3 | GIVEN un paiement Kkiapay confirmé, WHEN le callback est reçu, THEN le statut de la tranche passe à "payé" dans l'app, un reçu est généré et la secrétaire est notifiée |
| CA-12-4 | GIVEN un paiement échoué ou annulé, WHEN l'erreur est retournée par Kkiapay, THEN un message d'erreur explicite est affiché au parent et aucune donnée financière erronée n'est enregistrée |
| CA-12-5 | GIVEN un paiement réussi, THEN le parent reçoit un SMS de confirmation automatique via Africa's Talking |

---

### 4.4 Espace Parents

---

#### US-13 — Consultation des notes et bulletins par le parent

> **En tant que** Parent  
> **Je veux** consulter les notes et le bulletin trimestriel de mon enfant depuis l'application mobile  
> **Afin de** suivre ses performances scolaires en temps réel sans attendre la remise physique du bulletin

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-13-1 | GIVEN l'app Flutter connectée, WHEN le parent accède à l'onglet "Notes", THEN il voit les notes de son enfant regroupées par matière et par trimestre avec la moyenne calculée |
| CA-13-2 | GIVEN un bulletin trimestriel généré, WHEN le parent accède à l'onglet "Bulletins", THEN il peut le visualiser en PDF et le télécharger sur son appareil |
| CA-13-3 | GIVEN un parent avec plusieurs enfants dans l'école, WHEN il est connecté, THEN il peut basculer entre les profils de ses enfants via un sélecteur |
| CA-13-4 | GIVEN une nouvelle note saisie, WHEN l'enseignant valide, THEN le parent reçoit une notification push sur l'app |

---

#### US-14 — Messagerie parent-école

> **En tant que** Parent  
> **Je veux** envoyer et recevoir des messages depuis l'administration et les enseignants de l'école  
> **Afin de** communiquer sans me déplacer et rester informé des actualités de l'établissement

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-14-1 | GIVEN l'onglet "Messages", WHEN le parent compose et envoie un message à l'école, THEN le message est reçu dans l'interface web de la secrétaire ou du directeur |
| CA-14-2 | GIVEN un message envoyé par l'école, THEN une notification push est envoyée au parent et le message s'affiche dans sa boîte de réception |
| CA-14-3 | GIVEN un message non lu, THEN un badge numérique est visible sur l'icône de messagerie |
| CA-14-4 | GIVEN la messagerie, THEN les échanges sont conservés avec horodatage, identifiant de l'émetteur et statut lu/non lu |

---

#### US-15 — Notifications et consultation pour parents sans smartphone

> **En tant que** Parent sans smartphone  
> **Je veux** recevoir les informations importantes sur mon téléphone basique (SMS)  
> **Afin de** ne pas être exclu du suivi scolaire de mon enfant faute d'accès à internet

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-15-1 | GIVEN un parent identifié comme "SMS uniquement" dans le système, WHEN un bulletin est publié, THEN il reçoit un SMS résumé avec la moyenne générale et la mention de son enfant |
| CA-15-2 | GIVEN un SMS envoyé via Africa's Talking, THEN son statut de livraison est tracé (delivered / failed) dans le système |
| CA-15-3 | GIVEN une alerte d'absence, THEN le SMS est envoyé quelle que soit la catégorie du parent (smartphone ou SMS uniquement) |
| CA-15-4 | GIVEN un parent SMS-only et un parent connecté pour le même élève, THEN les deux reçoivent les notifications adaptées à leur canal |

---

#### US-16 — Authentification sécurisée (parent)

> **En tant que** Parent  
> **Je veux** me connecter à l'application via un code personnel sécurisé  
> **Afin de** protéger les données scolaires et financières de mon enfant

**Critères d'acceptation :**

| # | Critère |
|---|---------|
| CA-16-1 | GIVEN l'écran de connexion, WHEN le parent saisit ses identifiants corrects, THEN il accède à son espace en moins de 3 secondes |
| CA-16-2 | GIVEN 3 tentatives de connexion échouées, THEN le compte est temporairement bloqué 15 minutes et le parent en est notifié par SMS |
| CA-16-3 | GIVEN un parent souhaitant réinitialiser son mot de passe, WHEN il demande la réinitialisation, THEN un SMS avec un code OTP est envoyé sur son numéro enregistré |
| CA-16-4 | GIVEN une session active, WHEN l'app est inactive 30 minutes, THEN la session expire et la reconnexion est requise |

---

## 5. Matrice de Priorités MoSCoW

### 5.1 Module Administration

| Feature | MoSCoW | Justification |
|---------|--------|---------------|
| Inscription et gestion des élèves | **MUST** | Fonctionnalité centrale sans laquelle rien ne fonctionne |
| Gestion des classes et affectations | **MUST** | Prérequis aux modules pédagogique et financier |
| Tableau de bord de direction | **SHOULD** | Forte valeur ajoutée pour la gouvernance |
| Gestion du profil établissement | **MUST** | Nécessaire pour la conformité MEN des documents |
| Import en masse des données (CSV) | **COULD** | Utile pour les migrations, non critique au lancement |
| Gestion multi-établissements | **WON'T** | Hors périmètre v1.0 |

### 5.2 Module Pédagogique

| Feature | MoSCoW | Justification |
|---------|--------|---------------|
| Saisie des notes coefficientées | **MUST** | Cœur du module pédagogique |
| Génération bulletins PDF MEN Togo | **MUST** | Obligation réglementaire non négociable |
| Gestion des absences | **MUST** | Requis pour les alertes automatiques parents |
| Alertes SMS absences (x3) | **MUST** | Engagement contractuel avec écoles pilotes |
| Calcul automatique des moyennes | **MUST** | Déduit directement des règles de gestion |
| Graphiques de progression | **SHOULD** | Améliore l'expérience enseignant |
| Cahier de textes numérique | **COULD** | Valeur ajoutée v1.1 |
| Emploi du temps interactif | **WON'T** | Complexité élevée, v2.0 |

### 5.3 Module Financier

| Feature | MoSCoW | Justification |
|---------|--------|---------------|
| Gestion des tranches de scolarité | **MUST** | Fondation du module financier |
| Enregistrement paiements (espèces) | **MUST** | Mode de paiement dominant au Togo |
| Intégration Kkiapay (Mobile Money) | **MUST** | Différenciateur fort, demande marché |
| Alertes SMS impayés (Africa's Talking) | **MUST** | ROI démontrable pour les écoles |
| Génération reçus PDF | **MUST** | Obligatoire pour la comptabilité |
| Tableau de bord financier | **SHOULD** | Valeur pilotage direction |
| Export Excel comptable | **SHOULD** | Attendu par les comptables |
| Intégration logiciel comptable tiers | **WON'T** | Hors périmètre v1.0 |

### 5.4 Espace Parents (Flutter)

| Feature | MoSCoW | Justification |
|---------|--------|---------------|
| Authentification sécurisée | **MUST** | Sécurité des données |
| Consultation notes et bulletins | **MUST** | Raison d'être de l'app |
| Paiement Mobile Money (Kkiapay) | **MUST** | Fonctionnalité à fort impact |
| Notifications SMS (sans smartphone) | **MUST** | Inclusion numérique |
| Messagerie parent-école | **SHOULD** | Améliore la communication |
| Notifications push (avec smartphone) | **SHOULD** | UX moderne |
| Multi-enfants | **SHOULD** | Cas d'usage fréquent au Togo |
| Mode offline complet | **COULD** | Complexité technique élevée |

---

## 6. Règles de Gestion

---

### RG-01 — Calcul de la moyenne

> **Domaine :** Module Pédagogique

La moyenne d'un élève pour une matière sur un trimestre est calculée selon la formule :

```
Moyenne = Σ(note_i × coefficient_i) / Σ(coefficient_i)
```

- Les notes sont comprises entre 0 et 20 (valeurs décimales acceptées avec 2 chiffres après la virgule)
- Un élève sans aucune note pour une matière ne génère pas de moyenne (champ vide, non comptabilisé dans la moyenne générale)
- La moyenne générale trimestrielle est calculée de la même façon en utilisant les coefficients des matières

---

### RG-02 — Attribution des mentions

> **Domaine :** Module Pédagogique — Bulletins

L'attribution des mentions suit strictement la table officielle du MEN Togo :

| Moyenne | Mention |
|---------|---------|
| ≥ 16/20 | Très Bien |
| ≥ 14/20 | Bien |
| ≥ 12/20 | Assez Bien |
| ≥ 10/20 | Passable |
| < 10/20 | Insuffisant |

---

### RG-03 — Trimestres scolaires

> **Domaine :** Tous les modules

L'année scolaire est découpée en 3 trimestres fixes :

| Trimestre | Période |
|-----------|---------|
| T1 | Octobre → Décembre |
| T2 | Janvier → Mars |
| T3 | Avril → Juin |

Les dates exactes sont configurables par établissement dans les paramètres, mais doivent respecter les fourchettes ci-dessus. Aucune note ne peut être saisie hors de la période du trimestre actif.

---

### RG-04 — Tranches de scolarité

> **Domaine :** Module Financier

Chaque établissement définit 3 tranches de scolarité par an. Chaque tranche comporte :
- Un libellé (ex. "1ère tranche")
- Un montant (en FCFA, entier)
- Une date d'échéance

Les montants peuvent varier par niveau de classe. Un paiement est toujours affecté à une tranche spécifique. Un paiement partiel est accepté mais la tranche reste à l'état "partiellement payé" jusqu'au solde complet.

---

### RG-05 — Déclenchement des alertes absences

> **Domaine :** Module Pédagogique / Notifications

Un SMS d'alerte est automatiquement envoyé au(x) parent(s) d'un élève lorsque celui-ci cumule **3 absences non justifiées** sur le trimestre en cours. Le compteur est réinitialisé à chaque nouveau trimestre. Les absences justifiées (avec pièce ou saisie par la secrétaire) ne sont pas comptabilisées dans ce seuil.

---

### RG-06 — Conformité bulletins MEN Togo

> **Domaine :** Module Pédagogique — Bulletins

Tout bulletin généré doit obligatoirement contenir les éléments suivants conformément au modèle officiel du MEN Togo :

1. En-tête établissement (nom, adresse, n° autorisation)
2. Identité de l'élève (nom, prénom, classe, année scolaire)
3. Tableau des matières avec : note(s), coefficient, moyenne matière, rang matière
4. Moyenne générale du trimestre
5. Mention officielle
6. Rang dans la classe (ex. 3e / 45)
7. Effectif de la classe
8. Appréciation générale (saisie par le directeur ou titulaire)
9. Signature et cachet de direction

---

### RG-07 — Droits d'accès et confidentialité

> **Domaine :** Transverse — Sécurité

| Acteur | Peut voir | Ne peut pas voir |
|--------|-----------|-----------------|
| Directeur | Tout | — |
| Enseignant | Notes/absences de SES classes | Notes des autres enseignants, données financières |
| Secrétaire | Inscriptions, paiements | Notes, bulletins |
| Parent | Données de SES enfants uniquement | Données des autres élèves |

Un enseignant ne peut modifier que les notes qu'il a lui-même saisies. Toute modification de note sur un trimestre clôturé nécessite l'autorisation explicite du directeur (workflow d'approbation).

---

### RG-08 — Traçabilité des transactions financières

> **Domaine :** Module Financier

Toute opération financière (encaissement, annulation, remboursement) est immuable et auditée. Chaque enregistrement conserve :
- L'identifiant de l'utilisateur ayant effectué l'opération
- L'horodatage précis (UTC+1, fuseau Lomé)
- Le montant initial et final
- Le mode de paiement (espèces / Mobile Money / chèque)
- La référence de transaction Kkiapay le cas échéant

Aucune suppression physique d'un paiement n'est autorisée dans le système. Une annulation crée une ligne de "contre-passation" avec justification obligatoire.

---

## 7. Exigences Non-Fonctionnelles

### 7.1 Performance

| Exigence | Cible |
|----------|-------|
| Temps de réponse API standard | < 800 ms (P95) |
| Génération d'un bulletin PDF | < 3 secondes par bulletin |
| Génération lot (classe entière) | < 60 secondes pour 60 élèves |
| Synchronisation offline → online | < 5 secondes à la reconnexion |
| Capacité simultanée | 50 utilisateurs connectés sans dégradation |

### 7.2 Sécurité

| Exigence | Détail |
|----------|--------|
| Authentification | JWT avec refresh token (expiration 1h / refresh 7j) |
| Mots de passe | Hachage bcrypt, complexité minimale imposée |
| Transport | HTTPS obligatoire (TLS 1.2+) sur toutes les routes API |
| Données sensibles | Numéros de téléphone et données financières chiffrées at-rest |
| Logs d'accès | Journalisation de toutes les connexions et actions sensibles |
| Conformité RGPD-like | Collecte minimale, droit de modification, pas de revente de données |
| Accès admin | Authentification 2FA obligatoire pour le compte Directeur |

### 7.3 Disponibilité & Fiabilité

| Exigence | Cible |
|----------|-------|
| Disponibilité | 99,5 % uptime hors maintenance planifiée |
| Sauvegarde données | Backup quotidien automatique (PostgreSQL dump) |
| Rétention des backups | 30 jours glissants |
| Recovery Time Objective (RTO) | < 4 heures en cas d'incident majeur |
| Recovery Point Objective (RPO) | < 24 heures |

### 7.4 Offline & Mobile (contexte Togo)

| Exigence | Détail |
|----------|--------|
| Mode offline enseignant | Saisie des notes possible sans connexion, synchronisation à la reconnexion |
| Mode offline parent | Consultation des dernières notes et bulletins téléchargés |
| Consommation data | Optimisation des appels API pour connexions 2G/3G (payloads légers, compression gzip) |
| Taille de l'app Flutter | < 30 MB téléchargement initial |
| Compatibilité Android | API level 21+ (Android 5.0 Lollipop) |
| Compatibilité iOS | iOS 12+ |

### 7.5 Accessibilité & UX

| Exigence | Détail |
|----------|--------|
| Langue interface | Français uniquement (v1.0) |
| Messages d'erreur | En français, compréhensibles sans jargon technique |
| Design responsive | Web React adapté tablette + desktop |
| Accessibilité | Contraste AA minimum (WCAG 2.1) |

---

## 8. Contraintes Contexte Togolais

| # | Contrainte | Impact technique |
|---|-----------|-----------------|
| C1 | **Coupures électriques fréquentes** | L'app Flutter doit gérer les interruptions réseau gracieusement avec cache local |
| C2 | **Connexion internet instable (2G/3G dominant)** | API REST paginée, compression des réponses JSON, images compressées |
| C3 | **Paiements en FCFA uniquement** | Kkiapay configuré en FCFA, aucune conversion de devise |
| C4 | **Mobile Money dominant** (MTN, Moov) | Kkiapay supporte MTN MoMo Togo et Moov Money — double opérateur requis |
| C5 | **Numéros de téléphone togolais** | Format : +228 XX XX XX XX (8 chiffres hors indicatif) — validation regex obligatoire |
| C6 | **Faible taux de smartphones chez certains parents** | SMS (Africa's Talking) obligatoire comme canal de communication de secours |
| C7 | **Modèle MEN Togo non négociable** | Template PDF figé conforme aux circulaires MEN, non personnalisable sur la structure |
| C8 | **Absence d'adresses email généralisée** | Pas d'authentification par email pour les parents, SMS OTP uniquement |
| C9 | **Fuseaux horaires** | UTC+1 (Lomé, pas de changement d'heure saisonnier) — toutes les heures stockées en UTC |
| C10 | **Coût SMS limité** | Groupage des notifications pour minimiser les appels Africa's Talking (facturation à l'unité) |

---

## 9. Architecture Technique Synthèse

```
┌──────────────────────────────────────────────────────────┐
│                    CLIENTS                               │
│  ┌─────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │ React.js    │  │ Flutter App   │  │ SMS Feature   │   │
│  │ (Web Admin) │  │ (iOS/Android) │  │ (Parents GSM) │   │
│  └──────┬──────┘  └──────┬────────┘  └───────┬───────┘   │
└─────────┼────────────────┼───────────────────┼───────────┘
          │                │                   │
          ▼                ▼                   ▼
┌─────────────────────────────────────────────────────────┐
│              DJANGO REST FRAMEWORK (API)                 │
│  Authentification JWT | CORS | Rate Limiting            │
│                                                         │
│  ┌────────┐ ┌──────────┐ ┌───────────┐ ┌───────────┐   │
│  │ Admin  │ │  Pedago  │ │ Financier │ │  Parents  │   │
│  │  App   │ │   App    │ │    App    │ │   App     │   │
│  └────────┘ └──────────┘ └───────────┘ └───────────┘   │
└──────────────────────────┬──────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
  ┌──────────────┐  ┌────────────┐  ┌────────────────┐
  │  PostgreSQL  │  │  Kkiapay   │  │ Africa's       │
  │  (Primary)   │  │  MoMo API  │  │ Talking (SMS)  │
  └──────────────┘  └────────────┘  └────────────────┘
          │
  ┌──────────────┐
  │  WeasyPrint  │
  │  (PDF Gen)   │
  └──────────────┘
```

---

*Document produit par Claude (Business Analyst IA) — PSI v1.0.0*  
*À relire et valider par Abdoulaye Mahamane Nour (Développeur) avant implémentation*