# Assistant Agricole Marocain (مساعد الفلاحة المغربية)

Un assistant agricole alimenté par l'IA, conçu pour soutenir les agriculteurs marocains avec des conseils agricoles spécifiques à leur région. L'application fournit une interface web interactive utilisant Streamlit et exploite l'API Groq LLM pour des réponses intelligentes.

## 📋 Prérequis

- Python 3.7 ou supérieur
- Clé API Groq
- Connexion Internet stable
- Au moins 2 Go de RAM disponible
- Espace disque : minimum 500 Mo

## 🚀 Installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/yourusername/assistant-agricole-maroc.git
cd assistant-agricole-maroc
```

2. **Créer et activer un environnement virtuel**
```bash
# Sur Linux/MacOS
python3 -m venv venv
source venv/bin/activate

# Sur Windows
python -m venv venv
venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration des variables d'environnement**
   - Créer un fichier `.env` à la racine du projet
   - Ajouter les variables suivantes :
```env
GROQ_API_KEY=votre_clé_api_ici
MAX_TOKENS=256
TEMPERATURE=0.7
```

## ⚙️ Configuration

### Configuration de base
1. **Configuration du modèle**
   ```python
   # Dans config.py
   MODEL_CONFIG = {
       "model_name": "llama-3.1-70b-versatile",
       "temperature": 0.7,
       "max_tokens": 256
   }
   ```

2. **Configuration régionale**
   - Modifiez le fichier `regions.json` pour ajouter/modifier les régions supportées
   - Adaptez les paramètres climatiques par région dans `climate_data.json`

### Configuration avancée
1. **Personnalisation des réponses**
   - Modifiez `agricultural_context.py` pour adapter le contexte agricole
   - Ajustez les traductions Darija dans `translations.json`

2. **Optimisation des performances**
   ```python
   # Dans app.py
   st.set_page_config(
       layout="wide",
       initial_sidebar_state="collapsed",
       page_icon="🌾"
   )
   ```

## 🚀 Exécution

1. **Démarrer l'application**
```bash
streamlit run app.py
```

2. **Accéder à l'interface**
   - Ouvrez votre navigateur
   - Accédez à `http://localhost:8501`
   - Pour une utilisation en réseau local : `http://[votre-ip]:8501`

3. **Premier lancement**
   - Sélectionnez votre région
   - Choisissez le type de culture
   - Ajustez les paramètres de l'IA selon vos besoins

## 🚧 Limitations actuelles

1. **Limitations techniques**
   - Traitement limité à 256 tokens par réponse
   - Temps de réponse variable selon la charge du serveur
   - Nécessite une connexion Internet stable
   - Support limité pour les fichiers volumineux (max 200 Mo)

2. **Limitations fonctionnelles**
   - Base de connaissances limitée à certaines régions
   - Support partiel des dialectes locaux
   - Pas de support hors ligne
   - Absence de visualisation des données historiques

3. **Limitations d'intégration**
   - Pas d'intégration avec les systèmes météorologiques en temps réel
   - Absence d'API pour l'intégration avec d'autres systèmes
   - Pas de support pour les notifications mobiles

## 🔄 Pistes d'amélioration

1. **Améliorations techniques**
   - [x] Implémenter un système de mise en cache pour améliorer les performances
   - [ ] Ajouter un mode hors ligne avec synchronisation différée
   - [ ] Optimiser le traitement des fichiers volumineux
   - [ ] Améliorer la gestion de la mémoire

2. **Améliorations fonctionnelles**
   - [ ] Étendre la base de connaissances à toutes les régions du Maroc
   - [ ] Ajouter le support complet des dialectes locaux
   - [ ] Intégrer des données météorologiques en temps réel
   - [ ] Développer un système de recommandations proactif

3. **Nouvelles fonctionnalités**
   - [ ] Système de notification pour les alertes agricoles
   - [ ] Interface mobile native
   - [ ] Module d'analyse prédictive des récoltes
   - [ ] Intégration avec les systèmes d'irrigation intelligents

4. **Améliorations de l'interface**
   - [ ] Support multilingue complet
   - [ ] Interface adaptative pour mobiles
   - [ ] Tableaux de bord personnalisables
   - [ ] Visualisations interactives des données

## 📈 Surveillance et maintenance

1. **Logs et monitoring**
```bash
# Activer les logs détaillés
export LOG_LEVEL=DEBUG
streamlit run app.py --logger.level=debug
```

2. **Sauvegarde des données**
```bash
# Script de sauvegarde automatique
./backup.sh --all --compress
```

