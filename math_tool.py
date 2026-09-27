"""
math_tool.py - AI-powered math solver using OpenRouter API
Provides textbook-format solutions with step-by-step explanations.
"""

import json
import os
import requests
from typing import Optional

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fakeos_config.json")
DEFAULT_MODEL = "openai/gpt-3.5-turbo"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """You are a mathematics tutor. Provide solutions in textbook format with CLEAR HUMAN-READABLE MATH NOTATION.

**CRITICAL FORMATTING RULES:**
- NEVER use LaTeX ($...$, $$...$$, \\frac, \\sqrt, \\int, etc.)
- NEVER use ^ for exponents — use Unicode superscripts: x², x³, xⁿ
- NEVER use / for fractions — use Unicode fractions: ½, ⅓, ¼, ⅕, ⅙, ⅐, ⅛, ⅑, ⅒, or write as "a over b"
- NEVER use * for multiplication — use × or · or implicit multiplication
- NEVER use sqrt() — use √(…)
- NEVER use \\int — use ∫
- NEVER use \\sum — use Σ
- NEVER use \\lim — use lim
- NEVER use \\pi — use π
- NEVER use \\infty — use ∞
- NEVER use \\pm — use ±
- NEVER use \\neq — use ≠
- NEVER use \\leq — use ≤
- NEVER use \\geq — use ≥
- NEVER use \\approx — use ≈
- NEVER use \\cdot — use ·
- NEVER use \\times — use ×
- NEVER use \\div — use ÷
- NEVER use \\partial — use ∂
- NEVER use \\alpha, \\beta, etc. — use α, β, γ, δ, ε, θ, λ, μ, π, σ, φ, ω
- NEVER use \\sin, \\cos, \\tan — use sin, cos, tan
- NEVER use \\log, \\ln — use log, ln
- NEVER use \\boxed{} — use ▓▓▓ answer ▓▓▓ or [answer]

**USE THESE UNICODE SYMBOLS:**
- Exponents: ⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ⁿ ⁱ ⁺ ⁻ ⁼ ⁽ ⁾
- Fractions: ½ ⅓ ¼ ⅕ ⅙ ⅐ ⅛ ⅑ ⅒ ⅔ ¾ ⅗ ⅘ ⅚ ⅜ ⅝ ⅞
- Operators: + − × ÷ ± ∓ · √ ∛ ∜ ∞ ∝ ≈ ≠ ≤ ≥ ≪ ≫
- Calculus: ∫ ∬ ∭ ∮ ∯ ∰ ∂ ′ ″ ‴ ∇ Δ
- Sum/Product: Σ Π
- Logic: ∀ ∃ ∄ ∴ ∵ ∧ ∨ ¬ ⇒ ⇔
- Sets: ∈ ∉ ⊂ ⊃ ⊆ ⊇ ∪ ∩ ∅
- Greek: α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω
- Arrows: → ← ↔ ⇒ ⇐ ⇔ ↦ ↖ ↗ ↘ ↙
- Brackets: ⌊ ⌋ ⌈ ⌉ ⟨ ⟩ ┌ ┐ └ ┘
- Box: ▓▓▓ answer ▓▓▓

**Format Requirements:**
1. **Given**: Restate the problem clearly using Unicode math
2. **Formula/Theorem**: State relevant formulas using Unicode
3. **Step-by-Step Solution**: Number each step with clear explanations
4. **Final Answer**: Box with ▓▓▓ answer ▓▓▓
5. **Verification** (optional): Quick check

**Example Output:**
**Given**: Solve 2x + 5 = 13

**Formula**: Linear equation: ax + b = c → x = (c − b) / a

**Step 1**: Subtract 5 from both sides: 2x = 8

**Step 2**: Divide by 2: x = 4

**Final Answer**: ▓▓▓ x = 4 ▓▓▓

> **Check**: 2(4) + 5 = 8 + 5 = 13 ✓"""

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def save_config(config: dict):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
    except OSError:
        pass

def get_api_key() -> str:
    config = load_config()
    key = config.get("openrouter_api_key", "").strip()
    if key:
        return key
    # First time - ask user
    print("🔑 OpenRouter API Key Required")
    print("Get one at: https://openrouter.ai/keys")
    key = input("Enter your OpenRouter API key: ").strip()
    if not key:
        raise ValueError("API key cannot be empty")
    config["openrouter_api_key"] = key
    config.setdefault("openrouter_model", DEFAULT_MODEL)
    config.setdefault("math_temperature", 0.1)
    save_config(config)
    print("✅ Key saved securely (gitignored)")
    return key

def solve_math(question: str, retry_count: int = 0) -> str:
    api_key = get_api_key()
    config = load_config()
    model = config.get("openrouter_model", DEFAULT_MODEL)
    temp = config.get("math_temperature", 0.1)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/xarvynx/fakeos",
        "X-Title": "FakeOS Math Tool"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        "temperature": temp,
        "max_tokens": 3000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401 and retry_count < 1:
            # Invalid key - clear it and retry once
            config["openrouter_api_key"] = ""
            save_config(config)
            print("❌ Invalid API key. Please re-enter.")
            return solve_math(question, retry_count + 1)
        return f"❌ API Error ({e.response.status_code}): {e.response.text[:200]}"
    except requests.exceptions.Timeout:
        return "❌ Request timed out. Try a simpler question or check your connection."
    except requests.exceptions.RequestException as e:
        return f"❌ Network Error: {e}"
    except (KeyError, IndexError):
        return "❌ Unexpected API response format"

def math_cli():
    print("🧮 FakeOS Math Solver (OpenRouter)")
    print("Type 'exit' to quit, 'config' to change model, 'newkey' to change API key, 'clear' to clear screen")
    print("-" * 50)

    while True:
        try:
            question = input("\n📐 Math Question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit", "q"):
            break
        if question.lower() == "config":
            config = load_config()
            print(f"Current model: {config.get('openrouter_model', DEFAULT_MODEL)}")
            print("Popular models:")
            print("  • anthropic/claude-3.5-sonnet (default, best for math)")
            print("  • openai/gpt-4o")
            print("  • google/gemini-pro")
            print("  • deepseek/deepseek-chat")
            print("  • meta-llama/llama-3.1-70b-instruct")
            print("See all: https://openrouter.ai/models")
            new_model = input("New model (Enter to keep): ").strip()
            if new_model and new_model.lower() not in ("help", "exit", "quit", "clear", "config", "newkey"):
                config["openrouter_model"] = new_model
                save_config(config)
                print(f"✅ Model updated to {new_model}")
            elif new_model:
                print("❌ Invalid model name")
            continue
        if question.lower() == "newkey":
            config = load_config()
            print("🔑 Enter new OpenRouter API key:")
            print("Get one at: https://openrouter.ai/keys")
            new_key = input("New API key: ").strip()
            if new_key:
                config["openrouter_api_key"] = new_key
                save_config(config)
                print("✅ API key updated!")
            else:
                print("❌ Key cannot be empty")
            continue
        if question.lower() == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            continue
        if question.lower() == "help":
            print("""
Commands:
  <any math question>  - Get textbook-format solution
  config               - Change AI model
  newkey               - Change OpenRouter API key
  clear                - Clear screen
  help                 - Show this help
  exit                 - Return to FakeOS
""")
            continue

        print("\n🤔 Thinking...")
        answer = solve_math(question)
        print("\n" + "=" * 50)
        print(answer)
        print("=" * 50)