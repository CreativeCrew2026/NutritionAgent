<div align="center">

# 🥗 NutriGuide AI

### Personalised Nutrition Agent powered by IBM Granite LLM

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-black?logo=flask)](https://flask.palletsprojects.com)
[![IBM Granite](https://img.shields.io/badge/IBM%20Granite-13B%20Instruct-0f62fe?logo=ibm)](https://www.ibm.com/products/watsonx-ai)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![AI Ethics](https://img.shields.io/badge/AI%20Ethics-IBM%20Principles-purple)](https://www.ibm.com/artificial-intelligence/ethics)

> An **Agentic AI** web application that generates personalised 7-day nutrition plans using  
> **IBM Granite LLM** via watsonx.ai — complete with ethical guardrails, medical disclaimers,  
> a conversational chat interface, and automatic Markdown plan export.

[Live Demo](#-quick-start) · [Features](#-features) · [Architecture](#-architecture) · [API Docs](#-api-reference) · [Ethics](#-ai-ethics--guardrails)

</div>

---

## 📸 Screenshots

```
┌─────────────────────────────────────────────────────────────────┐
│  NutriGuide AI  [IBM Granite]                   ● Connected     │
├─────────────────────┬───────────────────────────────────────────┤
│  👤 Your Profile    │  📋 Nutrition Plan  💬 Ask  📁 Saved     │
│                     │                                           │
│  Name: Priya        │  ╔══════════════════════════════════╗    │
│  Age:  35           │  ║  🥗 Personalised Nutrition Plan  ║    │
│  City: Mumbai       │  ║  for Priya — IBM Granite AI      ║    │
│  Diet: 🌱 Veg       │  ╠══════════════════════════════════╣    │
│  Goal: Diabetes     │  ║  📊 Daily Calorie: 1,800 kcal    ║    │
│  Medical: T2DM      │  ║  🥩 Protein: 80g  🌾 Carbs: 220g ║   │
│                     │  ║  📅 7-Day Meal Plan...           ║    │
│  [✨ Generate Plan] │  ║  ✅ Foods to Emphasise...        ║    │
│                     │  ║  ⚠️  Medical Disclaimer          ║    │
│                     │  ╚══════════════════════════════════╝    │
└─────────────────────┴───────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **IBM Granite LLM** | `ibm/granite-13b-instruct-v2` via watsonx.ai SDK |
| 🧠 **Agentic AI** | ReAct pattern: Plan → Retrieve → Generate → Guardrail → Reflect |
| 🛡️ **Guardrails** | 8+ regex patterns block harmful/misleading content |
| 🌱 **Diet-Aware** | Vegetarian · Vegan · Non-Vegetarian · Flexitarian |
| 🏥 **Medical-Sensitive** | Adapts plan for diabetes, hypertension, heart disease, etc. |
| 📍 **Location-Based** | Suggests locally available foods by city/country |
| 💾 **Auto-Save .md** | Every plan saved to `nutrition_plans/` as Markdown |
| 💬 **AI Chat** | Ask follow-up nutrition questions with user context |
| 📁 **Plan History** | Browse and download all previously generated plans |
| ⚖️ **AI Ethics** | HAM tone · Transparency · Fairness · No harmful advice |
| ⚠️ **Disclaimer** | Medical disclaimer appended to every generated plan |
| 🎭 **Demo Mode** | Full demo response without IBM credentials — works out of the box |

---

## 🚀 Quick Start

### Prerequisites

| Software | Version | Download |
|----------|---------|----------|
| Python | 3.10 or later | [python.org](https://python.org) |
| Git | Any recent | [git-scm.com](https://git-scm.com) |

### Windows — One-Click Launch

```bat
# 1. Clone the repository
git clone https://github.com/CreativeCrew2026/NutritionAgent.git
cd NutritionAgent

# 2. Double-click setup.bat  (first time)
setup.bat

# OR just run directly
run.bat
```

The browser opens automatically at **http://localhost:5000**

---

### Manual Setup (all platforms)

```bash
# 1. Clone
git clone https://github.com/CreativeCrew2026/NutritionAgent.git
cd NutritionAgent

# 2. Create virtual environment
python -m venv venv

# 3. Activate
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure (optional — app works in demo mode without this)
cp .env.example .env
# Edit .env and add your IBM Cloud credentials

# 6. Run
python app.py
```

Open **http://localhost:5000**

---

## 🔑 IBM watsonx.ai Configuration

To enable **live IBM Granite LLM** responses, add your credentials to `.env`:

```env
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_watsonx_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

### How to get credentials

1. Sign up / log in at [IBM Cloud](https://cloud.ibm.com)
2. Create a **watsonx.ai** service instance
3. Open **watsonx.ai Studio** → Create a project
4. Go to **Manage → Access → API Keys** → Generate new key
5. Copy your **Project ID** from the project settings

> **No credentials?** The app runs in **Demo Mode** with a comprehensive pre-built example plan. All features work — only the LLM call uses a mock response.

---

## 🏗️ Architecture

### Project Structure

```
NutritionAgent/
│
├── app.py                        # Flask backend — API orchestration layer
│
├── agent/
│   ├── __init__.py
│   └── granite_agent.py          # IBM Granite LLM agent (core intelligence)
│
├── static/
│   └── index.html                # Web frontend (HTML5 + CSS3 + Vanilla JS)
│
├── nutrition_plans/
│   └── sample_nutrition_plan_demo.md   # Sample plan (committed)
│   └── *.md                      # Generated plans (git-ignored, user data)
│
├── AGENTIC_SDLC.md               # Full Agentic AI SDLC documentation
├── requirements.txt              # Python dependencies (pinned)
├── .env.example                  # Credentials template
├── .gitignore                    # Git ignore rules
├── run.bat                       # Windows one-click launcher
├── setup.bat                     # Windows first-time setup wizard
└── README.md                     # This file
```

### Agentic Pipeline (ReAct Pattern)

```
User Input (Profile Form)
         │
         ▼
┌────────────────┐
│  1. PLAN       │  Analyse user profile, select nutrition strategy
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  2. RETRIEVE   │  Build contextual prompt with user data + system instructions
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  3. GENERATE   │  Call IBM Granite 13B Instruct v2 via watsonx.ai SDK
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  4. GUARDRAIL  │  Screen output: 8+ harmful patterns → strip or block
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  5. REFLECT    │  Append medical disclaimer, structure response
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  6. OUTPUT     │  Return JSON → render in browser + save .md file
└────────────────┘
```

---

## 🔌 API Reference

### Base URL: `http://localhost:5000`

#### `GET /health`
Returns server status and model information.

```json
{
  "status": "healthy",
  "model": "ibm/granite-13b-instruct-v2",
  "demo_mode": true,
  "timestamp": "2025-01-15T10:30:00",
  "version": "1.0.0"
}
```

---

#### `POST /api/generate-plan`
Generate a personalised nutrition plan.

**Request body:**
```json
{
  "name": "Priya Sharma",
  "age": 35,
  "weight": 68,
  "height": 165,
  "city": "Mumbai",
  "country": "India",
  "diet_preference": "vegetarian",
  "goal": "Manage diabetes",
  "activity_level": "Moderately active (3–5 days/week)",
  "medical_history": "Type 2 Diabetes diagnosed 2020, mild hypertension",
  "allergies": "None"
}
```

**Response:**
```json
{
  "status": "success",
  "plan": "# Personalised Nutrition Plan\n...",
  "user_name": "Priya Sharma",
  "generated_at": "2025-01-15 10:30:00",
  "model": "ibm/granite-13b-instruct-v2",
  "saved_file": "nutrition_plan_Priya_Sharma_20250115_103000.md",
  "guardrail_warnings": [],
  "is_demo": false
}
```

---

#### `POST /api/query`
Ask a nutrition question.

```json
{ "question": "What foods help lower blood pressure?",
  "user_context": { "diet_preference": "vegetarian", "goal": "Manage blood pressure" } }
```

---

#### `GET /api/plans`
List all saved nutrition plan files.

#### `GET /api/plans/<filename>`
Download a saved plan as a `.md` file.

---

## 🛡️ AI Ethics & Guardrails

This application is built on IBM's **5 AI Ethics Principles**:

| Principle | Implementation |
|-----------|---------------|
| **Transparency** | Model name, demo/live status always shown to user |
| **Fairness** | Respects all dietary choices; no cultural bias |
| **Safety** | Guardrail layer blocks 8+ harmful content patterns |
| **Accountability** | Medical disclaimer on every generated plan |
| **Privacy** | No user data stored beyond session; plans saved locally only |

### HAM Communication Framework
All AI responses follow the **H**elpful · **A**ccurate · **M**indful tone:
- Warm, respectful, non-judgmental language
- Evidence-based nutritional guidance
- Clear escalation to healthcare professionals

### Blocked Content Patterns
The guardrail engine automatically removes any output matching:
- `"stop taking [medication]"` — medication interference
- `"cure [disease]"` — unsubstantiated medical claims  
- `"guaranteed weight loss"` — false promises
- `"detox/cleanse"` — pseudoscientific claims
- `"miracle food/diet"` — exaggerated claims
- Extreme caloric restriction promises
- `"starve yourself"` — dangerous advice
- Unsafe fasting recommendations

---

## 📊 Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| AI Model | IBM Granite 13B Instruct v2 | Latest |
| AI Platform | IBM watsonx.ai | — |
| Backend | Python + Flask | 3.13 + 3.0.3 |
| Frontend | HTML5 + CSS3 + Vanilla JS | — |
| HTTP Client | Requests + HTTPX | 2.34.2 + 0.28.1 |
| Data | pandas + numpy | 2.3.3 + 2.5.4 |
| Config | python-dotenv | 1.0.1 |

---

## 📋 Agentic AI SDLC

This project follows all 7 phases of the **Agentic AI Software Development Life Cycle**:

1. **Requirements Engineering** — Functional + non-functional requirements documented
2. **System Design** — Layered architecture with agentic pipeline
3. **Implementation** — IBM Granite integration with ReAct pattern
4. **Testing** — Unit, integration, guardrail, and UX testing
5. **Deployment** — Local (bat), containerisable, cloud-ready
6. **Monitoring** — Health endpoint, guardrail logging
7. **Continuous Improvement** — Backlog in `AGENTIC_SDLC.md`

See [`AGENTIC_SDLC.md`](AGENTIC_SDLC.md) for the full documentation.

---

## ⚠️ Medical Disclaimer

> This application is for **general informational purposes only** and does **not** constitute
> medical advice, diagnosis, or treatment. Always consult a **registered dietitian** or
> **qualified healthcare provider** before making significant dietary changes, especially
> if you have a medical condition.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**NutriGuide AI** — Responsible Nutrition Intelligence  
Built with ❤️ using IBM Granite & watsonx.ai

[IBM watsonx.ai](https://www.ibm.com/products/watsonx-ai) · [IBM AI Ethics](https://www.ibm.com/artificial-intelligence/ethics) · [IBM Granite](https://www.ibm.com/granite)

</div>
