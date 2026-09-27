"""
math_tool.py - AI-powered math solver using OpenRouter API
Provides textbook-format solutions with step-by-step explanations.
"""

import json
import os
import requests
from typing import Optional

# Import visual components from visuals
from visuals import (C, S, ICON, colorize, gradient, spinner_animation, 
                     progress_bar, clear_screen, print_box)

# Config file path
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
    print(f'{S.INFO}{ICON.KEY} OpenRouter API Key Required{C.R}')
    print(f'{S.DIM}Get one at: https://openrouter.ai/keys{C.R}')
    key = input(f'{S.CMD}Enter your OpenRouter API key: {C.R}').strip()
    if not key:
        raise ValueError("API key cannot be empty")
    config["openrouter_api_key"] = key
    config.setdefault("openrouter_model", DEFAULT_MODEL)
    config.setdefault("math_temperature", 0.1)
    save_config(config)
    print(f'{S.OK}{ICON.CHECK} Key saved securely (gitignored){C.R}')
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
            print(f'{S.ERR}{ICON.CROSS} Invalid API key. Please re-enter.{C.R}')
            return solve_math(question, retry_count + 1)
        return f'{S.ERR}{ICON.CROSS} API Error ({e.response.status_code}): {e.response.text[:200]}{C.R}'
    except requests.exceptions.Timeout:
        return f'{S.ERR}{ICON.CROSS} Request timed out. Try a simpler question or check your connection.{C.R}'
    except requests.exceptions.RequestException as e:
        return f'{S.ERR}{ICON.CROSS} Network Error: {e}{C.R}'
    except (KeyError, IndexError):
        return f'{S.ERR}{ICON.CROSS} Unexpected API response format{C.R}'


def math_cli():
    clear_screen()
    print_box('AI MATH SOLVER', [
        f'{S.CMD}Ask any math question{C.R}',
        f'{S.CMD}Uses OpenRouter API (LLM){C.R}',
        f'{S.CMD}Textbook format with Unicode math{C.R}',
    ], 55, ICON.MATH)
    print()
    
    print(f'{S.INFO}{ICON.MATH} FakeOS Math Solver (OpenRouter){C.R}')
    print(f'{S.DIM}Commands: exit, config, newkey, clear, help{C.R}')
    print(f'{S.DIM}{"─" * 50}{C.R}')
    print()

    while True:
        try:
            question = input(f'{S.CMD}Math{S.DIM}> {C.R}').strip()
        except (EOFError, KeyboardInterrupt):
            print(f'\n{S.INFO}Exiting...{C.R}')
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit", "q"):
            print(f'{S.OK}{ICON.CHECK} Returning to FakeOS...{C.R}')
            break
        if question.lower() == "config":
            config = load_config()
            print(f'{S.INFO}Current model: {S.CMD}{config.get("openrouter_model", DEFAULT_MODEL)}{C.R}')
            print(f'{S.INFO}Popular models:{C.R}')
            print(f'  {S.CMD}• openai/gpt-3.5-turbo{C.R} (fast, reliable)')
            print(f'  {S.CMD}• openai/gpt-4o{C.R} (smartest)')
            print(f'  {S.CMD}• anthropic/claude-3.5-sonnet{C.R} (great for math)')
            print(f'  {S.CMD}• deepseek/deepseek-chat{C.R} (free tier)')
            print(f'  {S.CMD}• meta-llama/llama-3.1-70b{C.R} (open source)')
            print(f'{S.DIM}See all: https://openrouter.ai/models{C.R}')
            new_model = input(f'{S.CMD}New model (Enter to keep): {C.R}').strip()
            if new_model and new_model.lower() not in ("help", "exit", "quit", "clear", "config", "newkey"):
                config["openrouter_model"] = new_model
                save_config(config)
                print(f'{S.OK}{ICON.CHECK} Model updated to {S.CMD}{new_model}{C.R}')
            elif new_model:
                print(f'{S.ERR}{ICON.CROSS} Invalid model name{C.R}')
            continue
        if question.lower() == "newkey":
            config = load_config()
            print(f'{S.INFO}{ICON.KEY} Enter new OpenRouter API key:{C.R}')
            print(f'{S.DIM}Get one at: https://openrouter.ai/keys{C.R}')
            new_key = input(f'{S.CMD}New API key: {C.R}').strip()
            if new_key:
                config["openrouter_api_key"] = new_key
                save_config(config)
                print(f'{S.OK}{ICON.CHECK} API key updated!{C.R}')
            else:
                print(f'{S.ERR}{ICON.CROSS} Key cannot be empty{C.R}')
            continue
        if question.lower() == "clear":
            clear_screen()
            print_box('AI MATH SOLVER', [
                f'{S.CMD}Ask any math question{C.R}',
                f'{S.CMD}Uses OpenRouter API (LLM){C.R}',
                f'{S.CMD}Textbook format with Unicode math{C.R}',
            ], 55, ICON.MATH)
            print()
            continue
        if question.lower() == "help":
            print_box('MATH SOLVER COMMANDS', [
                f'{S.CMD}<any math question>{C.R}  {S.DIM}Get textbook-format solution{C.R}',
                f'{S.CMD}config{C.R}               {S.DIM}Change AI model{C.R}',
                f'{S.CMD}newkey{C.R}               {S.DIM}Change OpenRouter API key{C.R}',
                f'{S.CMD}clear{C.R}                {S.DIM}Clear screen{C.R}',
                f'{S.CMD}help{C.R}                 {S.DIM}Show this help{C.R}',
                f'{S.CMD}exit{C.R}                 {S.DIM}Return to FakeOS{C.R}',
            ], 55, ICON.INFO)
            continue

        print()
        spinner_animation('Thinking...', 0.5)
        answer = solve_math(question)
        print()
        print(f'{S.ACCENT}{"═" * 50}{C.R}')
        print(answer)
        print(f'{S.ACCENT}{"═" * 50}{C.R}')
        print()