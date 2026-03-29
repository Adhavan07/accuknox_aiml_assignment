# Problem Statement 2 — LLM / AI / ML Conceptual Questions

---

## Q1 — Self-Rating on LLM, Deep Learning, AI, ML

| Domain | Rating | What I can actually do | Tools I've used |
|---|---|---|---|
| Machine Learning | B | Can build and evaluate models with guidance; comfortable with core algorithms | scikit-learn, pandas, NumPy |
| Deep Learning | B | Understand backprop, CNNs, RNNs; need docs for hyperparameter tuning | PyTorch, TensorFlow (basics) |
| AI (broad) | B | Solid on concepts like search, agents, planning; building RAG prototypes | LangChain, OpenAI API |
| LLMs | B | Hands-on with prompt engineering and API integration; exploring fine-tuning | GPT-4, Claude API, RAG |

> Scale: **A** = code independently | **B** = code under supervision | **C** = little/no understanding

I'm a B across all four areas. That means I can work with these technologies and build functional systems, but I lean on documentation for production-level work. My background is in DevOps and cloud engineering (AWS, Kubernetes, Prometheus), so I've applied ML-adjacent things in real systems — like anomaly detection on metrics and log classification — but I'm still growing on the pure ML and deep learning side. I'm being honest here because I'd rather show real progress than overstate where I am.

---

## Q2 — Key Architectural Components of an LLM-Based Chatbot

I'll walk through this the way I'd explain it to someone building one from scratch.

### 1. User Interface + API Gateway
A chat UI (web or mobile) captures the user's message. Behind it sits a lightweight API server — FastAPI or Express — that handles auth, rate limiting, and routes the request. For streaming responses so the user sees tokens appear in real time, you'd use Server-Sent Events or WebSockets rather than waiting for the full response.

### 2. Prompt Construction
Before anything hits the LLM, a prompt builder assembles the full context:
- A **system prompt** that defines the bot's role and constraints
- **Retrieved knowledge chunks** from the RAG step (see below)
- **Conversation history** trimmed to fit the model's context window

This is actually one of the most important parts to get right — the LLM is only as good as what you put in the prompt.

### 3. RAG — Retrieval-Augmented Generation
If the bot needs to answer questions about domain-specific knowledge (docs, manuals, past tickets), you don't retrain the model — you retrieve relevant content at query time and inject it into the prompt.

How it works:
1. Documents are chunked and embedded into vectors
2. Stored in a vector database (e.g., Qdrant, Pinecone)
3. At query time, the user's message is also embedded
4. A nearest-neighbour search retrieves the top-K most relevant chunks
5. Those chunks go into the prompt as grounding context

This is how you get a chatbot that can answer *"what does our security policy say about CVE-2024-xxxx?"* without hallucinating.

### 4. LLM Inference
The assembled prompt gets sent to the model — OpenAI, Anthropic, or a self-hosted open-source model on a GPU server. The response streams back token by token. Temperature and top-p are tuned depending on whether you want precise factual answers (low temperature) or more creative responses (higher).

### 5. Session Memory
- **Short-term**: conversation turns stored in Redis keyed by session ID — fast, cheap, ephemeral
- **Long-term**: key facts stored in a database or back into the vector store for future retrieval across sessions

### 6. Safety and Observability
- All prompts and responses logged (with PII scrubbed) for audit and fine-tuning
- Input/output classifiers (e.g., OpenAI Moderation API) to reject harmful content
- p95 latency monitoring on inference — LLMs are slow compared to normal APIs and users notice quickly

### Architecture Overview

```
User → API Gateway → Prompt Builder ← [RAG: Embeddings + Vector DB]
                          ↓
                    LLM (GPT-4 / Claude / Llama)
                          ↓
               Streamed response → UI
                          ↓
              Redis (session) + Logger + Safety Classifier
```

---

## Q3 — Vector Databases: What They Are and Which I'd Choose

### What is a vector database?

A relational database stores data in rows and columns and matches exact values. A vector database stores data as high-dimensional numerical vectors — embeddings — and finds things that are **semantically similar**, even if they share no exact words.

When you run text through an embedding model (like OpenAI's `text-embedding-3-small`), it maps the meaning of the text into a point in high-dimensional space. Sentences that mean similar things end up close together in that space. A vector DB's job is to take a query vector and find the nearest neighbours among millions of stored vectors — fast.

**Simple analogy:** "How do I restart a pod in Kubernetes?" and "kubectl rollout restart steps" look completely different as text, but their embedding vectors are almost identical. A SQL `LIKE` query would miss the connection entirely. A vector search finds it instantly.

The most common index structure used is **HNSW (Hierarchical Navigable Small World)** which gives sub-millisecond approximate nearest-neighbour search even over millions of vectors.

### My Hypothetical Problem

Imagine AccuKnox gets a new CVE alert at 2am. Instead of an analyst spending 45 minutes digging through past incident notes to find similar ones, you want a system that automatically surfaces: *"here are the 3 most similar past security incidents and what resolved them."*

That's a semantic search problem — and that's exactly what a vector DB solves.

### Options Compared

| DB | Hosting | Payload Filtering | Performance | Best For |
|---|---|---|---|---|
| **Qdrant** | Self-host or cloud | Rich JSON filters | Excellent (HNSW) | On-prem enterprise / security |
| Pinecone | SaaS only | Good | Excellent | Fast cloud prototypes |
| Weaviate | Self-host or cloud | GraphQL-based | Good | Knowledge graph + vector |
| ChromaDB | Local only | Basic | Limited at scale | Local dev / experiments |

### Why I'd Choose Qdrant

For this specific security use case, Qdrant wins on the things that actually matter:

1. **Security data can't leave the building.** Pinecone is SaaS only — all your CVE data and incident history goes to their servers. For a security product like AccuKnox, self-hosting is a hard requirement. Qdrant runs perfectly on-prem.

2. **Payload filtering is a real feature.** When an analyst wants *"similar incidents where severity='CRITICAL' AND cluster='prod'"*, they shouldn't need two queries. Qdrant handles that in one call with JSON payload filters.

3. **HNSW performance holds up at scale.** Millions of incident vectors, p99 under 10ms — that fits a real-time triage SLA.

4. **Apache 2.0 licence.** No GPL complications if AccuKnox wants to embed it in a commercial product.

### End-to-End Flow

```
New CVE alert fires
  → Text embedded using text-embedding-3-small
  → Qdrant: search top-3 nearest past incidents (filtered by severity + cluster)
  → Return: incident ID, resolution steps, similarity score
  → LLM generates a triage summary from the retrieved context
  → Analyst sees recommendation in under 5 seconds
```

The key win here is that the LLM is grounded in real incident history, not making things up. The RAG pattern keeps it accurate and auditable — both things that matter a lot in a security product.

---

*Adhavan | AccuKnox AI/ML Trainee Assignment | March 2026*
