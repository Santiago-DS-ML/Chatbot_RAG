# 🤖 JANGO — Chatbot RAG avec LangChain, FAISS & Gemini

JANGO est un chatbot conversationnel intelligent développé avec **Streamlit**, **LangChain** et **Google Gemini**.

Il utilise une architecture **Retrieval-Augmented Generation (RAG)** afin de répondre aux questions des utilisateurs à partir d'une base documentaire spécifique à l'entreprise fictive **TechNova Store**.

L'objectif du projet est de construire un assistant capable de fournir des réponses pertinentes à partir d'informations documentaires, tout en conservant le contexte de la conversation.

---

## 🚀 Démo

🌐 **Accéder au chatbot :**

👉 [🔗 JANGO — Chatbot RAG](https://jango-v2-rag.streamlit.app/)

---

## 📸 Aperçu de l'application

### Interface du chatbot

![Interface du chatbot](chatbot-interface.png)

### Conversation avec mémoire et RAG

![Conversation avec JANGO](chatbot-conversation.png)

> Ajoutez vos deux captures dans un dossier `images/` à la racine du projet.

---

## 🧠 Architecture du projet

JANGO repose sur une architecture **Retrieval-Augmented Generation (RAG)**.

```text
                    ┌──────────────────┐
                    │ informations.txt │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    TextLoader    │
                    └────────┬─────────┘
                             │
                             ▼
              ┌────────────────────────────┐
              │ RecursiveCharacterTextSplitter │
              └─────────────┬──────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │   Embeddings    │
                   │  MiniLM-L6-v2   │
                   └────────┬────────┘
                            │
                            ▼
                     ┌────────────┐
                     │   FAISS    │
                     │ VectorStore│
                     └─────┬──────┘
                           │
                           ▼
                    ┌────────────┐
                    │  Retriever │
                    └─────┬──────┘
                          │
                          ▼
                    ┌────────────┐
                    │   Prompt   │
                    └─────┬──────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  Gemini 2.5 Flash│
                 └────────┬─────────┘
                          │
                          ▼
                    Réponse JANGO
```

---

## 🔎 Comment fonctionne le RAG ?

Lorsqu'un utilisateur pose une question :

1. La question est envoyée au **retriever**.
2. Le retriever recherche les documents les plus pertinents dans FAISS.
3. Les documents récupérés sont transmis à la chaîne de génération.
4. Le contexte est injecté dans le prompt.
5. **Gemini 2.5 Flash** génère la réponse.
6. La réponse est affichée progressivement grâce au **streaming**.
7. L'historique de conversation est conservé afin de permettre à JANGO de comprendre les échanges précédents.

Cette architecture permet de séparer clairement :

* la recherche d'information ;
* la génération de réponse ;
* la mémoire conversationnelle ;
* l'interface utilisateur.

---

## 💬 Mémoire conversationnelle

JANGO conserve l'historique des échanges grâce à `st.session_state`.

Les messages utilisateur et assistant sont ensuite convertis en objets LangChain :

* `HumanMessage`
* `AIMessage`

Ils sont injectés dans le prompt grâce à :

```python
MessagesPlaceholder("chat_history")
```

Ainsi, JANGO peut prendre en compte le contexte des échanges précédents.

---

## ⚡ Streaming

Les réponses de Gemini sont générées progressivement et affichées en temps réel dans Streamlit.

Cela permet d'obtenir une expérience plus naturelle qu'une réponse affichée uniquement après la génération complète.

---

## 🛠️ Technologies utilisées

| Technologie           | Utilisation                   |
| --------------------- | ----------------------------- |
| Python                | Langage principal             |
| Streamlit             | Interface web                 |
| LangChain             | Orchestration du pipeline RAG |
| Gemini 2.5 Flash      | Modèle de langage             |
| FAISS                 | Base vectorielle              |
| Hugging Face          | Modèle d'embeddings           |
| Sentence Transformers | `all-MiniLM-L6-v2`            |
| GitHub                | Gestion et partage du code    |
| Streamlit Cloud       | Déploiement                   |

---

## 📂 Structure du projet

```text
jango/
│
├── app.py
├── informations.txt
├── requirements.txt
├── README.md
├── chatbot-interface.jpeg
├── chatbot-conversation.jpeg

## 🔐 Sécurité

La clé API Gemini n'est pas écrite directement dans le code.

Elle est récupérée depuis les secrets Streamlit :

```python
st.secrets["GEMINI_API_KEY"]
```
---

## 🎯 Fonctionnalités

* ✅ Interface conversationnelle avec Streamlit
* ✅ Intégration de Gemini 2.5 Flash
* ✅ RAG basé sur une base documentaire
* ✅ Découpage automatique des documents
* ✅ Embeddings avec Sentence Transformers
* ✅ Recherche vectorielle avec FAISS
* ✅ Retriever LangChain
* ✅ Prompt avec contexte documentaire
* ✅ Mémoire conversationnelle
* ✅ Streaming des réponses
* ✅ Possibilité d'effacer l'historique
* ✅ Déploiement sur Streamlit Cloud

---

## 📚 Ce que ce projet m'a permis d'apprendre

Ce projet m'a surtout permis de comprendre le fonctionnement d'un système RAG en passant d'abord par une implémentation **from scratch**, avant de reconstruire le pipeline avec **LangChain**.

J'ai ainsi pu comprendre concrètement le rôle de chaque composant :

```text
Document
   ↓
Chunking
   ↓
Embedding
   ↓
Vector Store
   ↓
Retriever
   ↓
Context
   ↓
Prompt
   ↓
LLM
```

Cette approche m'a permis de mieux comprendre les abstractions proposées par LangChain au lieu de simplement les utiliser comme une boîte noire.

---

## 🔮 Améliorations possibles

Plusieurs évolutions sont envisageables :

* [ ] Support de fichiers PDF
* [ ] Upload de documents directement depuis Streamlit
* [ ] Support de plusieurs documents
* [ ] Affichage des sources utilisées pour chaque réponse
* [ ] Amélioration du système de mémoire
* [ ] Recherche hybride
* [ ] Reranking des documents récupérés
* [ ] Interface utilisateur plus avancée
* [ ] Persistance du Vector Store

---

## 👨‍💻 Auteur

**APPIA Jacques-Elie**

Étudiant et passionné par la **Data Science, l'Intelligence Artificielle, le Machine Learning et les applications orientées Business**.

Ce projet s'inscrit dans mon parcours d'apprentissage autour des applications LLM, du RAG et de la Data Science appliquée.

---

## ⭐ Si ce projet vous intéresse

N'hésitez pas à explorer le code, tester l'application et laisser un ⭐ sur le repository.

**Merci d'avoir découvert JANGO ! 🤖**
