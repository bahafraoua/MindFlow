# MindFlow
[Demo](https://github.com/bahafraoua/MindFlow)


## Comment Utiliser l'Application

Bienvenue sur la plateforme MindFlow ! Cette section vous guidera sur la manière d'interagir avec l'application une fois qu'elle sera déployée.

1.  **Installer les Dépendances :**

    * Installez Streamlit en exécutant la commande suivante dans votre terminal :

        ```
        pip install -r requirements.txt
        ```

2.  **Exécuter l'Application :**

    * Depuis votre terminal, dans le répertoire du projet où se trouve `MindFlow`, exécutez la commande suivante :

        ```
        streamlit run MindFlow.py 
        ```

    * Cette commande démarrera le serveur Streamlit et ouvrira automatiquement la platform


---
![Emotion Recognition](images/img.jpeg)
---
## **Description Générale du Projet**

L’objectif principal de ce stage est de concevoir et développer une plateforme intelligente permettant d’évaluer l’état psychologique des employés en entreprise, à travers deux approches non-invasives :

1. L’analyse de l’écriture manuscrite scannée (graphologie assistée par IA)

2. L’analyse du visage scanné ou capturé via webcam (reconnaissance émotionnelle)

Ces évaluations visent à aider les départements RH à prévenir les risques psychosociaux, détecter le stress, l’anxiété, la fatigue ou la démotivation, tout en garantissant l’anonymat et l’éthique dans le traitement des données.

---

## **Objectifs du Projet**

* Étudier les techniques d’analyse émotionnelle à partir d’images faciales (deep learning).

* Explorer la graphologie numérique pour l’extraction de traits psychologiques à partir d’écritures manuscrites.

* Développer une interface utilisateur web sécurisée pour l’analyse automatique des deux types de données.

* Concevoir un module de scoring psychologique et générer des rapports synthétiques pour les RH.

* Respecter les règles de confidentialité, RGPD et déontologie.

---

## **Livrables Attendus**

* Étude comparative des techniques d’analyse faciale et d’écriture.

* Démonstrateur fonctionnel de la plateforme avec les deux modules d’analyse.

* Base de données anonymisée de tests.

* Tableau de bord RH avec résultats graphiques et suggestions.

---

## **Technologies et Langages Utilisés**

### **Front-End**

* React.js ou Vue.js pour l’interface web

* HTML5 / CSS3 / JavaScript

### **Back-End & API**

* Python (Flask ou FastAPI)

* Librairies IA :

  * Pour l’analyse faciale : OpenCV, Dlib, DeepFace, MediaPipe

  * Pour la graphologie : Tesseract OCR, TensorFlow / PyTorch, Scikit-learn

### **Machine Learning / Deep Learning**

* Modèles pré-entraînés de reconnaissance émotionnelle

* Réseaux de neurones pour le traitement de l’écriture manuscrite

* Traitement d’image et NLP pour analyse sémantique

### **Base de Données**

* PostgreSQL ou MongoDB

### **Langue de Développement**

* Langue principale : Français

* Documentation technique en Français et Anglais

