<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/headerDark.svg" />
    <img src="assets/headerLight.svg" alt="DuoReadme" />
  </picture>

[Usage CI/CD](#intégration-github-actions) | [Usage CLI](#utilisation) | [API Usage](#interface-de-programmation) | [Signaler des Problèmes](https://github.com/duoreadme/duoreadme/issues/new/choose)

</div>

DuoReadme est un outil CLI puissant pour traduire automatiquement le code et les fichiers README d'un projet dans plusieurs langues et générer une documentation multilingue standardisée.

## Fonctionnalités

- **Support Multilingue** : Prend en charge plus de 100 langues dont le chinois, l'anglais, le japonais, le coréen, le français, l'allemand, l'espagnol, l'italien, le portugais, le russe, etc. Pour la liste complète des langues, veuillez consulter [Codes ISO des Langues](./LANGUAGE.md).
- **Analyse Intelligente** : Analyse automatiquement la structure du projet et le contenu du code.
  1. Si le projet contient un fichier `.gitignore`, il applique automatiquement les règles de filtrage.
  2. DuoReadme utilise une stratégie de lecture intelligente du contenu du projet pour garantir que le contenu traduit soit à la fois complet et précis, en fonction du niveau des fichiers et dossiers.
- **Traitements en Batch** : Génère des fichiers README pour toutes les langues en un seul clic.
- **Intégration avec Tencent Cloud** : Intégré à la plateforme d'Intelligence Tencent Cloud.
- **Configuration Standard** : Utilise des normes de projet courantes, plaçant le README.md en anglais dans le répertoire racine et les autres fichiers README.md dans le répertoire docs.
- **Intégration GitHub Actions** : Traduit automatiquement les fichiers README dans plusieurs langues à l'aide de GitHub Actions. Vous pouvez consulter la section [Intégration GitHub Actions](#intégration-github-actions) pour plus de détails.

## Installation

```bash
pip install duoreadme
```

## Configuration

> Vous pouvez consulter le fichier [APPLY.md](./APPLY.md) pour plus de détails.

Vous pouvez consulter le fichier [config.yaml.example](./config.yaml.example) pour la configuration du fichier.

## Utilisation

### gen - Générer README Multilingue (Optimisé avec modèle README étoile élevée)

```bash
# Générer README multilingue en utilisant les paramètres par défaut
duoreadme gen

# Spécifier les langues à traduire
duoreadme gen --languages "zh-Hans,en,ja,ko,fr"

# Options générales
Utilisation: duoreadme gen [OPTIONS]

  Générer un README multilingue

Options:
  --project-path TEXT  Chemin du projet, par défaut répertoire courant
  --languages TEXT     Langues à générer, séparées par des virgules, par exemple: zh-Hans,en,ja
  --config TEXT  Chemin du fichier de configuration
  --verbose  Afficher les détails de la sortie
  --debug  Activer le mode débogage, afficher les logs au niveau DEBUG
  --help   Afficher ce message et quitter
```

### trans - Seulement Traduction de Texte

La commande `trans` est une fonction pure de traduction de texte qui lit le fichier README à partir du répertoire racine du projet et le traduit dans plusieurs langues. Contrairement à la commande `gen` qui traite toute la structure du projet, `trans` se concentre uniquement sur la traduction du contenu README.

```bash
# Traduire le fichier README en utilisant les paramètres par défaut
duoreadme trans

# Spécifier les langues à traduire
duoreadme trans --languages "zh-Hans,en,ja,ko,fr"

# Options générales
Utilisation: duoreadme trans [OPTIONS]

  Fonction pure de traduction de texte - traduire le fichier README dans le répertoire racine
  du projet

Options:
  --project-path TEXT  Chemin du projet, par défaut répertoire courant
  --languages TEXT     Langues à traduire, séparées par des virgules, par exemple: zh-
   Hans,en,ja
  --config TEXT  Chemin du fichier de configuration
  --verbose  Afficher les détails de la sortie
  --debug  Activer le mode débogage, afficher les logs au niveau DEBUG
  --help   Afficher ce message et quitter
```

### config - Afficher les Informations de Configuration
```bash
# Afficher la configuration intégrée actuelle
duoreadme config

# Activer le mode débogage pour voir les informations de configuration détaillées
duoreadme config --debug
```

### set - Mettre à Jour la Configuration Intégrée (Seulement Développement)
```bash
# Appliquer une nouvelle configuration à la configuration intégrée (pour développement/build uniquement)
duoreadme set my_config.yaml
```

### export - Exporter la Configuration Intégrée
```bash
# Exporter la configuration intégrée actuelle
duoreadme export [-o exported_config.yaml]
```

## Interface de Programmation

DuoReadme fournit une API Python complète pour intégrer la fonctionnalité de traduction dans vos applications.

```python
from src.core.translator import Translator
from src.core.parser import Parser
from src.utils.config import Config

# Configuration personnalisée
config = Config("custom_config.yaml")

# Créer un traducteur avec des paramètres personnalisés
translator = Translator(config)

# Traduire avec des langues spécifiques
languages = ["zh-Hans", "en", "ja", "ko"]
result = translator.translate_project(
    project_path="./my_project",
    languages=languages
)

# Parser et traiter les résultats
parser = Parser()
parsed_content = parser.parse_multilingual_content(result)

# Accéder au contenu traduit
for lang, content in parsed_content.content.items():
    print(f"Langue: {lang}")
    print(f"Contenu: {content[:200]}...")
    print("-" * 50)
```

## Intégration GitHub Actions

DuoReadme peut être intégré à votre dépôt GitHub à l'aide de GitHub Actions pour des workflows de traduction automatisés.

### Configuration Rapide

> Vous pouvez consulter le fichier [APPLY.md](./APPLY.md) pour plus de détails.

1. **Configurer les Secrets** :
   1. TENCENTCLOUD_SECRET_ID : À appliquer dans [Tencent Cloud Console](https://console.cloud.tencent.com/cam/capi), sélectionnez `Créer une clé`.
   2. TENCENTCLOUD_SECRET_KEY : Même principe.
   3. DUOREADME_BOT_APP_KEY : Dans votre [page d'application](https://lke.cloud.tencent.com/lke#/app/home), sélectionnez `Appeler` puis trouvez-le dans `appkey`.
   4. GH_TOKEN : Vous pouvez l'appliquer dans `Paramètres` - `Paramètres développeurs` - `Jetons personnels` - `Jetons (classique)` - `Créer un nouveau jeton` - `Sans expiration` - `Sélection: repo et workflow`.
   5. Ajouter les secrets requis à votre dépôt `votre dépôt` - `paramètres` - `Sécurité et variables` - `Actions` - `Nouveau secret du dépôt`.

2. **Utiliser l'Action** : Ajoutez le fichier d'action ci-dessous à votre dossier workflow `.github/workflows/duoreadme.yml`.

```yaml
# .github/workflows/duoreadme.yml
name: DuoReadme

on:
  push: # Vous pouvez changer la condition déclencheuse.
    branches: [ main ]
    paths: [ 'README.md', 'docs/**' ]
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
  - uses: actions/checkout@v4
  with:
  token: ${{ secrets.GH_TOKEN }}

  - name: Traduire avec paramètres personnalisés
  uses: duoreadme/duoreadme@v0.1.2
  with:
  languages: "zh-Hans,en,ja" # Vous pouvez spécifier plusieurs langues, séparées par des virgules
  translation_mode: "trans" # Vous pouvez utiliser 'gen' ou 'trans'.
  commit_message: "Mettre à jour la documentation multilingue" # Vous pouvez personnaliser le message de commit.
  debug: "false" # Vous pouvez activer le mode débogage pour voir les logs détaillés.
  env:
  TENCENTCLOUD_SECRET_ID: ${{ secrets.TENCENTCLOUD_SECRET_ID }}
  TENCENTCLOUD_SECRET_KEY: ${{ secrets.TENCENTCLOUD_SECRET_KEY }}
  DUOREADME_BOT_APP_KEY: ${{ secrets.DUOREADME_BOT_APP_KEY }}
```

3. À chaque modification du README ou des docs, l'action traduira automatiquement le README et les docs dans les langues spécifiées.

## Stratégie de Compression

### 1. Stratégie d'Analyse des Fichiers
```
Répertoire Racine du Projet
├── README.md (Lecture Prioritaire)
├── .gitignore (Pour Filtrage)
├── src/ (Répertoire du Code Source)
├── lib/ (Répertoire des Fichiers Bibliothèque)
├── docs/ (Répertoire de Documentation)
└── Autres Fichiers de Configuration
```

### 2. Ordre de Lecture Prioritaire
1. **README.md** - Documentation principale du projet, lecture prioritaire et traitement compressé.
2. **Fichiers Source** - Lecture par importance.
3. **Fichiers de Configuration** - Fichiers de configuration du projet.
4. **Fichiers de Documentation** - Autres fichiers d'explications documentaires.

### 3. Workflow de Traitement du Contenu

#### 3.1 Filtrage des Fichiers
- Applique automatiquement les règles `.gitignore`.
- Filtre les fichiers binaires, temporaires et artefacts de build.
- Ne traite que les fichiers texte (.md, .py, .js, .java, .cpp, etc.).

#### 3.2 Compression du Contenu
- **README.md** : Compressé à 3000 caractères, conservant le contenu principal.
- **Fichiers Source** : Sélection intelligente des fichiers importants, chaque fichier compressé à 2000 caractères.
- **Limite Totale de Contenu** : Pas plus de 15KB par traduction, le contenu long est traité par lots automatiquement.

#### 3.3 Sélection Intelligente
- Priorise les fichiers contenant la logique principale.
- Omet les fichiers de test, exemples et temporaires.
- Conserve les définitions de fonctions clés, classes et commentaires.

#### 3.4 Mécanisme de Traitement en Lots
Lorsque le contenu du projet dépasse 15KB, le système traite automatiquement en lots :

```
Analyse du Contenu → Groupe des Fichiers → Traduction en Lots → Fusion des Résultats
```

- **Groupe des Fichiers** : Groupe par type et importance des fichiers.
- **Traduction en Lots** : Traite jusqu'à 15KB de contenu par lot.
- **Fusion des Résultats** : Fusionne intelligemment les résultats des lots multiples.

### 4. Types de Fichiers Supportés
- **Fichiers Documentation** : `.md`, `.txt`, `.rst`
- **Code Source** : `.py`, `.js`, `.java`, `.cpp`, `.c`, `.go`, `.rs`
- **Fichiers Configuration** : `.yaml`, `.yml`, `.json`, `.toml`
- **Autres Textes** : `.sql`, `.sh`, `.bat`