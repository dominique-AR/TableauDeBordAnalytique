# Tableau de Bord Analytique (TBA) - Dashboard Python

## Description
Le **Tableau de Bord Analytique (TBA)** est un outil de visualisation et d'analyse de données financières et opérationnelles développé pour l'AGETIPA.
Il est construit avec **Python** et le framework **Dash**, permettant une interface web interactive pour monitorer des indicateurs clés tels que :
- les marges bénéficiaires,
- les redevances,
- les coûts de processus,
- les évolutions budgétaires sur la période **2017-2022**.

Le dashboard s'appuie sur des données importées depuis des fichiers Excel (`BA_CHARGES.xlsx`, `ANALYTIQUES_17_22.xls`) et utilise des visualisations comme :
- des jauges (*gauges*),
- des histogrammes,
- des camemberts (*pie-charts*),
- des tableaux récapitulatifs.

---

## Fonctionnalités Principales

- **Authentification** :
  Login sécurisé via `Dash-Authentification`.

- **Page d'Accueil** :
  Point d'entrée principal du dashboard.

- **Analyses des Marges** :
  - Marge bénéficiaire actuelle (exercice en cours) avec jauge (% par rapport à 35%).
  -Histogramme par projet.
  - Analyse cumulée de 2017 à 2022.

- **Redevances** :
  -Histogramme comparatif cumul : Redevances *vs.* Coûts de revient.
  - Écarts : Coûts de revient *vs.* Redevance.
  - Évolution par an : Budget *vs.* Redevance.

- **Coûts de Processus** :
  - Ventilation des coûts de processus.
  - Ventilation des redevances.
  - Camembert (*pie-chart*) : Budgets *vs.* Réalisations.
  -Histogramme : Budgets *vs.* Réalisations par rubrique.

- **Visualisations Avancées** :
  - Tableaux récapitulatifs par projet (Redevances & Coûts).
  - Évolution annuelles (`evol_Cout_2017`, `evolution_Redv_2017`, `evolution_2017`).
  - Calculs spécifiques : Coefficients projets, ventilation coûts (`Vent_CI_NRP`, `Vent_CI_CMOD`, etc.).

- **Données** :
  Utilisation de DataFrames Pandas (ex. : `ds_tba`, `ds_tba_prj`, `ds_tba_ev_R`, etc.) pour le traitement des données.

---

## Architecture et Flux

Le flux du dashboard est décrit dans le *flowchart* (`TBA_Flowchart.pdf`) :

### Démarrage Local
- L'utilisateur accède via un navigateur web à `localhost:8050`.
- Binding via **Gunicorn**.
- Login et authentification **Dash**.

### Navigation
- De la page d'accueil, accès aux sections :
  - Analyses des Marges,
  - Redevances,
  - Coûts Processus.
- Décisions conditionnelles (**YES/NO**) pour afficher des visualisations spécifiques (ex. : Exercice en cours ? Cumul 2017-2022 ?).

### Traitement des Données
- **Import des feuilles Excel** :
  - `BA_CHARGES_details`,
  - `Balance_Details`,
  - `Balance_an_Ex2023`.
- **Processus et Projets** :
  - `Vent_CI_NRP`,
  - `Vent_CI_CMOD`,
  - `Coûts_processus`, etc.
- **Résultats analytiques** :
  - `resultat_analytique`,
  - `Charges_2017_2022`,
  - `red_2017_2022`.
- **Calculs** :
  - Marge projets (`marge_projets`, `marge_pj_cum3`),
  - Coefficients (`CD_RCMOD`, `CI_RP`, `CI_NRP`).

### Déploiement Cloud
- Hébergé sur **AWS PaaS** avec une instance conteneurisée.
- Accès via navigateur web à une **IP statique** sur le port `8050`.

---

## Prérequis

- **Python 3.x** avec les bibliothèques suivantes (voir `requirements.txt`) :
  ```text
  Dash
  Pandas
  Plotly (pour les visualisations)
  Gunicorn (pour le serveur)
