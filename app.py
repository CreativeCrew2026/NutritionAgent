"""
Nutrition Agentic AI — Flask Backend
Agentic SDLC Phase: API / Orchestration Layer
Routes: /generate-plan, /query, /save-plan, /health
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Local agent
from agent.granite_agent import GraniteNutritionAgent

load_dotenv()

# ── App setup ───────────────────────────────────
app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "nutrition-ai-dev-key")
CORS(app)

# Singleton agent instance
_agent = GraniteNutritionAgent()

# Plans directory
PLANS_DIR = Path("nutrition_plans")
PLANS_DIR.mkdir(exist_ok=True)

# ── Input validation ────────────────────────────
REQUIRED_FIELDS = ["name", "age"]

def _validate_user_data(data: dict) -> tuple[bool, str]:
    for field in REQUIRED_FIELDS:
        if not data.get(field):
            return False, f"Field '{field}' is required."
    try:
        age = int(data["age"])
        if not (1 <= age <= 120):
            return False, "Age must be between 1 and 120."
    except (ValueError, TypeError):
        return False, "Age must be a valid number."
    # Sanitise text inputs
    for key in ["name", "medical_history", "goal", "allergies"]:
        val = data.get(key, "")
        if len(str(val)) > 500:
            return False, f"Field '{key}' exceeds maximum length."
    return True, ""


def _sanitise_input(text: str) -> str:
    """Remove potential prompt injection characters."""
    text = re.sub(r"<\|.*?\|>", "", text)           # Remove special tokens
    text = re.sub(r"[<>]", "", text)                 # Strip HTML tags
    text = text.strip()
    return text[:500]                                 # Hard cap


# ── Routes ──────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "model": "ibm/granite-13b-instruct-v2",
        "demo_mode": _agent.is_mock,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })


@app.route("/api/generate-plan", methods=["POST"])
def generate_plan():
    """
    Agentic endpoint: collect user details → invoke Granite → return plan.
    """
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Sanitise all string inputs
        sanitised = {}
        for key, val in data.items():
            sanitised[key] = _sanitise_input(str(val)) if isinstance(val, str) else val

        # Validate
        valid, error_msg = _validate_user_data(sanitised)
        if not valid:
            return jsonify({"error": error_msg}), 422

        # Call agent
        result = _agent.generate_nutrition_plan(sanitised)

        # Auto-save to file
        filename = _save_plan_to_file(result, sanitised)
        result["saved_file"] = filename

        return jsonify(result), 200

    except Exception as e:
        print(f"[API] /generate-plan error: {e}")
        return jsonify({"error": "An internal error occurred. Please try again."}), 500


@app.route("/api/query", methods=["POST"])
def query():
    """Answer a standalone nutrition question."""
    try:
        data = request.get_json(force=True)
        if not data or not data.get("question"):
            return jsonify({"error": "Question is required"}), 400

        question = _sanitise_input(data["question"])
        if len(question) < 3:
            return jsonify({"error": "Question is too short"}), 422

        user_context = data.get("user_context")
        result = _agent.answer_query(question, user_context)
        return jsonify(result), 200

    except Exception as e:
        print(f"[API] /query error: {e}")
        return jsonify({"error": "An internal error occurred."}), 500


@app.route("/api/save-plan", methods=["POST"])
def save_plan():
    """Explicitly save/re-save a nutrition plan to markdown file."""
    try:
        data = request.get_json(force=True)
        plan_text = data.get("plan", "")
        user_data = data.get("user_data", {})

        if not plan_text:
            return jsonify({"error": "No plan content to save"}), 400

        result_stub = {
            "plan": plan_text,
            "user_name": user_data.get("name", "User"),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        filename = _save_plan_to_file(result_stub, user_data)
        return jsonify({"status": "saved", "filename": filename}), 200

    except Exception as e:
        print(f"[API] /save-plan error: {e}")
        return jsonify({"error": "Failed to save plan."}), 500


@app.route("/api/plans", methods=["GET"])
def list_plans():
    """List all saved nutrition plans."""
    try:
        plans = []
        for f in sorted(PLANS_DIR.glob("*.md"), reverse=True):
            stat = f.stat()
            plans.append({
                "filename": f.name,
                "size_bytes": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            })
        return jsonify({"plans": plans}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/plans/<filename>", methods=["GET"])
def get_plan(filename):
    """Download a saved plan."""
    safe_name = re.sub(r"[^a-zA-Z0-9_\-.]", "", filename)
    plan_path = PLANS_DIR / safe_name
    if not plan_path.exists():
        return jsonify({"error": "Plan not found"}), 404
    return send_from_directory(str(PLANS_DIR.resolve()), safe_name, as_attachment=True)


# ── Utility ──────────────────────────────────────

def _save_plan_to_file(result: dict, user_data: dict) -> str:
    """Write the nutrition plan to a timestamped .md file."""
    name_slug = re.sub(r"[^a-zA-Z0-9]", "_", result.get("user_name", "user"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nutrition_plan_{name_slug}_{timestamp}.md"
    filepath = PLANS_DIR / filename

    header = f"""---
title: "Nutrition Plan for {result.get('user_name', 'User')}"
generated_at: "{result.get('generated_at', '')}"
model: "{result.get('model', 'IBM Granite')}"
app_version: "1.0.0"
---

# Personalised Nutrition Plan
**Name:** {user_data.get('name', 'N/A')}  
**Age:** {user_data.get('age', 'N/A')}  
**Diet Preference:** {user_data.get('diet_preference', 'N/A')}  
**Location:** {user_data.get('city', '')}, {user_data.get('country', '')}  
**Goal:** {user_data.get('goal', 'N/A')}  
**Generated:** {result.get('generated_at', '')}  
**AI Model:** {result.get('model', 'IBM Granite')}

---

"""
    filepath.write_text(header + result.get("plan", ""), encoding="utf-8")
    print(f"[API] Plan saved → {filepath}")
    return filename


# ── Entry point ─────────────────────────────────

if __name__ == "__main__":
    import sys
    # Ensure stdout can handle Unicode on Windows
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    print("=" * 60)
    print("  NutriGuide AI -- IBM Granite Nutrition Agent")
    print(f"  Server: http://localhost:{port}")
    print(f"  Demo mode: {_agent.is_mock}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=debug)
