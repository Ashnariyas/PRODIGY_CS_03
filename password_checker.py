"""
password_checker.py
Password Strength Assessment Tool

Evaluates a password across six criteria and returns
a detailed score, rating, and actionable feedback.

Criteria:
  1. Length         — tiered scoring (8 / 12 / 16+ chars)
  2. Uppercase      — at least one A-Z
  3. Lowercase      — at least one a-z
  4. Digits         — at least one 0-9
  5. Special chars  — at least one !@#$... etc.
  6. No common      — not in the top-10000 password list
"""

from __future__ import annotations
import re
import math
import getpass

# ---------------------------------------------------------------------------
# Common passwords (top 50 as a lightweight embedded list)
# In production, load from a full wordlist file.
# ---------------------------------------------------------------------------
COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123", "monkey",
    "1234567", "letmein", "trustno1", "dragon", "baseball", "iloveyou",
    "master", "sunshine", "ashley", "bailey", "passw0rd", "shadow",
    "123123", "654321", "superman", "qazwsx", "michael", "football",
    "password1", "password123", "admin", "welcome", "login", "hello",
    "charlie", "donald", "password2", "qwerty123", "1q2w3e4r", "zxcvbnm",
    "iloveyou1", "1234", "12345", "123456789", "0987654321", "111111",
    "1111111", "000000", "987654321", "pass", "test", "guest", "root",
}

SPECIAL_CHARS = r"!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~"
SPECIAL_RE    = re.compile(rf"[{SPECIAL_CHARS}]")


# ---------------------------------------------------------------------------
# Core analyser
# ---------------------------------------------------------------------------

def analyse(password: str) -> dict:
    """
    Analyse a password and return a result dict containing:
      - criteria   : dict of criterion → (passed: bool, detail: str)
      - score      : int 0-100
      - rating     : str  ("Very Weak" … "Very Strong")
      - entropy    : float (bits)
      - suggestions: list[str]
    """
    length      = len(password)
    has_upper   = bool(re.search(r"[A-Z]", password))
    has_lower   = bool(re.search(r"[a-z]", password))
    has_digit   = bool(re.search(r"\d",    password))
    has_special = bool(SPECIAL_RE.search(password))
    is_common   = password.lower() in COMMON_PASSWORDS

    # --- Score breakdown (total 100 pts) ---
    score = 0
    criteria = {}

    # Length  (0-35 pts)
    if length >= 16:
        length_pts, length_detail = 35, f"{length} chars — excellent"
    elif length >= 12:
        length_pts, length_detail = 25, f"{length} chars — good"
    elif length >= 8:
        length_pts, length_detail = 15, f"{length} chars — acceptable"
    else:
        length_pts, length_detail = 0,  f"{length} chars — too short"
    score += length_pts
    criteria["Length"] = (length >= 8, length_detail)

    # Uppercase  (0-15 pts)
    criteria["Uppercase letters"] = (has_upper, "A-Z present" if has_upper else "No uppercase found")
    score += 15 if has_upper else 0

    # Lowercase  (0-15 pts)
    criteria["Lowercase letters"] = (has_lower, "a-z present" if has_lower else "No lowercase found")
    score += 15 if has_lower else 0

    # Digits  (0-15 pts)
    criteria["Numbers"] = (has_digit, "Digits present" if has_digit else "No digits found")
    score += 15 if has_digit else 0

    # Special  (0-15 pts)
    criteria["Special characters"] = (
        has_special,
        "Special chars present" if has_special else "No special characters (!@#$ …)"
    )
    score += 15 if has_special else 0

    # Not common  (0-5 pts penalty if common)
    if is_common:
        score = max(0, score - 20)
        criteria["Not a common password"] = (False, "⚠ Found in common passwords list!")
    else:
        criteria["Not a common password"] = (True, "Not in known common list")

    score = max(0, min(100, score))

    # --- Rating ---
    if score >= 85:
        rating = "Very Strong"
    elif score >= 65:
        rating = "Strong"
    elif score >= 45:
        rating = "Moderate"
    elif score >= 25:
        rating = "Weak"
    else:
        rating = "Very Weak"

    # --- Entropy estimate ---
    pool = 0
    if has_lower:   pool += 26
    if has_upper:   pool += 26
    if has_digit:   pool += 10
    if has_special: pool += 32
    if pool == 0:   pool  = 26
    entropy = length * math.log2(pool) if length > 0 else 0.0

    # --- Suggestions ---
    suggestions = []
    if length < 8:
        suggestions.append("Use at least 8 characters (12+ recommended).")
    elif length < 12:
        suggestions.append("Increase length to 12+ characters for better security.")
    if not has_upper:
        suggestions.append("Add uppercase letters (A-Z).")
    if not has_lower:
        suggestions.append("Add lowercase letters (a-z).")
    if not has_digit:
        suggestions.append("Include at least one number (0-9).")
    if not has_special:
        suggestions.append("Add special characters (e.g. !@#$%^&*).")
    if is_common:
        suggestions.append("Avoid commonly used passwords — choose something unique.")
    if not suggestions:
        suggestions.append("Great password! Store it securely in a password manager.")

    return {
        "password":    password,
        "score":       score,
        "rating":      rating,
        "entropy":     round(entropy, 1),
        "criteria":    criteria,
        "suggestions": suggestions,
    }


# ---------------------------------------------------------------------------
# Pretty printer
# ---------------------------------------------------------------------------

RATING_BARS = {
    "Very Weak":  ("█░░░░", "\033[91m"),   # red
    "Weak":       ("██░░░", "\033[93m"),   # yellow
    "Moderate":   ("███░░", "\033[33m"),   # orange-ish
    "Strong":     ("████░", "\033[92m"),   # green
    "Very Strong":("█████", "\033[92m"),   # bright green
}

def _c(code: str, text: str, reset="\033[0m") -> str:
    """Wrap text in ANSI colour."""
    return f"{code}{text}{reset}"

def print_result(result: dict) -> None:
    rating  = result["rating"]
    bar, colour = RATING_BARS.get(rating, ("░░░░░", "\033[0m"))
    score   = result["score"]

    print()
    print("─" * 52)
    print(f"  Strength  : {_c(colour, rating)}  {_c(colour, bar)}  {score}/100")
    print(f"  Entropy   : {result['entropy']} bits")
    print("─" * 52)
    print("  Criteria:")
    for name, (passed, detail) in result["criteria"].items():
        icon = _c("\033[92m", "✔") if passed else _c("\033[91m", "✘")
        print(f"    {icon}  {name:<26} {detail}")
    print("─" * 52)
    print("  Suggestions:")
    for tip in result["suggestions"]:
        print(f"    →  {tip}")
    print("─" * 52)
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    print("\n" + "═" * 52)
    print("       Password Strength Checker")
    print("═" * 52)

    while True:
        print("\nOptions:")
        print("  1 — Check a password")
        print("  2 — Quit")
        choice = input("Choose (1/2): ").strip()

        if choice == "2":
            print("\nStay secure!\n")
            break
        elif choice != "1":
            print("  Please enter 1 or 2.")
            continue

        # Use getpass so the password isn't echoed
        try:
            pwd = getpass.getpass("  Enter password (hidden): ")
        except Exception:
            pwd = input("  Enter password: ")

        if not pwd:
            print("  No password entered.")
            continue

        result = analyse(pwd)
        print_result(result)


if __name__ == "__main__":
    main()
