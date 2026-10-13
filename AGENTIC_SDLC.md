# Agentic AI SDLC — NutriGuide AI

## Software Development Life Cycle for Agentic AI Applications

---

## Phase 1: Requirements Engineering

### Problem Statement
Individuals lack personalised, medically-aware nutrition guidance that respects their
cultural preferences, health conditions, and local food availability.

### Functional Requirements
| ID | Requirement |
|----|-------------|
| FR-01 | Collect user details: name, age, diet preference, medical history, location |
| FR-02 | Generate personalised 7-day nutrition plan using IBM Granite LLM |
| FR-03 | Support vegetarian, vegan, non-vegetarian, and flexitarian diets |
| FR-04 | Adapt plan for medical conditions (diabetes, hypertension, etc.) |
| FR-05 | Answer user queries via a chat interface |
| FR-06 | Save generated plans to .md files |
| FR-07 | List and download previously saved plans |

### Non-Functional Requirements
| ID | Requirement |
|----|-------------|
| NFR-01 | AI Ethics: Follow IBM's 5 AI Ethics Principles |
| NFR-02 | Safety: Guardrails block 8+ harmful content patterns |
| NFR-03 | HAM Tone: Helpful, Accurate, Mindful communication |
| NFR-04 | Performance: Response within 30 seconds |
| NFR-05 | Transparency: Always disclose AI-generated content |
| NFR-06 | Disclaimer: Medical disclaimer on every plan |
| NFR-07 | Graceful degradation: Demo mode when no API key |

---

## Phase 2: System Design

### Agentic AI Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     NutriGuide AI System                        │
│                                                                 │
│  ┌──────────────┐    HTTP/JSON    ┌───────────────────────────┐ │
│  │   Web UI     │ ◄────────────► │     Flask API Layer        │ │
│  │ (HTML/CSS/JS)│                │  app.py                   │ │
│  └──────────────┘                │  - Input validation        │ │
│                                  │  - Sanitisation            │ │
│                                  │  - Route handlers          │ │
│                                  └────────────┬──────────────┘ │
│                                               │                 │
│                                  ┌────────────▼──────────────┐ │
│                                  │   Granite Nutrition Agent  │ │
│                                  │  granite_agent.py          │ │
│                                  │                            │ │
│                                  │  ┌─────────────────────┐  │ │
│                                  │  │  Agentic Pipeline   │  │ │
│                                  │  │  1. Plan            │  │ │
│                                  │  │  2. Retrieve ctx    │  │ │
│                                  │  │  3. Build prompt    │  │ │
│                                  │  │  4. Generate (LLM)  │  │ │
│                                  │  │  5. Guardrails      │  │ │
│                                  │  │  6. Reflect         │  │ │
│                                  │  │  7. Output          │  │ │
│                                  │  └─────────────────────┘  │ │
│                                  └────────────┬──────────────┘ │
│                                               │                 │
│                                  ┌────────────▼──────────────┐ │
│                                  │  IBM watsonx.ai SDK        │ │
│                                  │  ibm-watsonx-ai           │ │
│                                  │  Model: granite-13b-inst   │ │
│                                  └────────────┬──────────────┘ │
│                                               │                 │
│                                  ┌────────────▼──────────────┐ │
│                                  │  IBM Cloud / watsonx.ai    │ │
│                                  │  (External LLM Service)    │ │
│                                  └───────────────────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Nutrition Plans Storage (nutrition_plans/*.md)           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Agentic Pattern: ReAct (Reason + Act)

```
User Input
    │
    ▼
┌─────────┐    ┌──────────────┐    ┌────────────────┐
│  REASON │───►│     ACT      │───►│    OBSERVE     │
│         │    │              │    │                │
│ Analyse │    │ Build prompt │    │ Receive LLM    │
│ profile │    │ Call Granite │    │ response       │
│ Select  │    │ Apply guards │    │ Check quality  │
│ strategy│    │ Save to disk │    │ Apply feedback │
└─────────┘    └──────────────┘    └────────┬───────┘
     ▲                                       │
     └───────────────────────────────────────┘
                    (Reflection loop)
```

---

## Phase 3: Implementation

### Technology Decisions

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| LLM | IBM Granite 13B Instruct v2 | Domain-appropriate, instruction-tuned |
| AI Platform | IBM watsonx.ai | Enterprise-grade, governed AI |
| Backend | Flask 3.0 | Lightweight, Python-native |
| Frontend | Vanilla JS + CSS | Zero dependencies, fast load |
| Output | Markdown (.md) | Portable, readable, version-controllable |

### Key Design Decisions
1. **Single-file frontend** — No build system required; runs from any server
2. **Demo mode fallback** — App works without credentials using rich mock data
3. **Regex guardrails** — Pre-compiled patterns for zero-latency safety checks
4. **Prompt engineering** — System + user prompt structure matches Granite's training
5. **Timestamped filenames** — Prevents overwrites; enables plan history

---

## Phase 4: Testing Strategy

### Test Categories

| Category | Tests | Status |
|----------|-------|--------|
| Unit | Agent guardrails, input validation, file saving | Implemented |
| Integration | Flask routes → Agent → File system | Via app startup |
| Ethics | Harmful content blocking, disclaimer presence | Guardrail regex |
| UX | Browser compatibility, responsive layout | Manual |
| API | All 6 endpoints, error codes | Via /health |

### Guardrail Test Cases
```python
# Should be BLOCKED:
"Stop taking your insulin"           # → [CONTENT REMOVED]
"Guaranteed weight loss in 5 days"  # → [CONTENT REMOVED]
"Detox your liver naturally"         # → [CONTENT REMOVED]

# Should PASS:
"Eat more leafy greens"              # → OK
"Drink 8 glasses of water daily"     # → OK
"Consult your doctor first"          # → OK
```

---

## Phase 5: Deployment

### Local Deployment (Windows)
```
run.bat → Python venv → pip install → Flask server → Browser
```

### Production Deployment Options
| Platform | Method |
|----------|--------|
| IBM Code Engine | `ibmcloud ce application create` |
| Docker | `docker build -t nutriguide . && docker run -p 5000:5000` |
| Heroku | `git push heroku main` |
| Azure App Service | `az webapp create` |

---

## Phase 6: Monitoring & Governance

### Metrics to Track
- Plan generation success/failure rate
- Guardrail trigger frequency (by pattern)
- Average response time
- Demo vs. live mode usage ratio
- Most common health goals

### AI Governance Checklist
- [x] Model card documented (Granite 13B Instruct v2)
- [x] Guardrails implemented and tested
- [x] Medical disclaimer on every output
- [x] Input validation and sanitisation
- [x] No PII stored beyond session
- [x] Demo mode for testing without live data
- [x] Transparency: model name shown to user

---

## Phase 7: Continuous Improvement

### Backlog
- [ ] Add user authentication (IBM App ID)
- [ ] Store plans in IBM Cloudant NoSQL
- [ ] Add RAG with nutrition research papers
- [ ] Fine-tune Granite on nutrition domain data
- [ ] Add meal photo analysis (vision model)
- [ ] Multi-language support (Hindi, Spanish, Arabic)
- [ ] Dietitian review workflow

---

*NutriGuide AI SDLC Document — v1.0*  
*IBM Granite | watsonx.ai | Agentic AI*
