# PRODIGY_CS_03
# Password Strength Checker

A Python tool that analyses password strength across six security criteria, computes an entropy estimate, assigns a rating, and gives clear, actionable feedback.

---

## Features

- **Six-criteria scoring** — length, uppercase, lowercase, digits, special characters, common-password check
- **0–100 score** with five plain-English ratings
- **Entropy estimate** in bits (based on character pool size)
- **Actionable suggestions** — tells you exactly what to improve
- **Common password detection** — flags passwords found in known breach lists
- **Hidden input** via `getpass` — password is never echoed to the terminal
- **Importable module** — use `analyse()` in your own code

---

## Ratings

| Score | Rating |
|-------|--------|
| 85–100 | ✅ Very Strong |
| 65–84 | 🟢 Strong |
| 45–64 | 🟡 Moderate |
| 25–44 | 🟠 Weak |
| 0–24 | 🔴 Very Weak |

---

## Scoring Breakdown

| Criterion | Max Points | Rule |
|-----------|-----------|------|
| Length | 35 pts | 8+ chars = 15, 12+ = 25, 16+ = 35 |
| Uppercase letters | 15 pts | At least one A–Z |
| Lowercase letters | 15 pts | At least one a–z |
| Numbers | 15 pts | At least one 0–9 |
| Special characters | 15 pts | At least one `!@#$%^&*` etc. |
| Common password | −20 pts | Penalised if found in known list |

---

## Requirements

- Python 3.6+
- No third-party libraries

---

## Usage

### Run the interactive CLI

```bash
python password_checker.py
```

```
════════════════════════════════════════════════════
       Password Strength Checker
════════════════════════════════════════════════════

Options:
  1 — Check a password
  2 — Quit
Choose (1/2): 1
  Enter password (hidden):

────────────────────────────────────────────────────
  Strength  : Very Strong  █████  95/100
  Entropy   : 104.9 bits
────────────────────────────────────────────────────
  Criteria:
    ✔  Length                     16 chars — excellent
    ✔  Uppercase letters          A-Z present
    ✔  Lowercase letters          a-z present
    ✔  Numbers                    Digits present
    ✔  Special characters         Special chars present
    ✔  Not a common password      Not in known common list
────────────────────────────────────────────────────
  Suggestions:
    →  Great password! Store it securely in a password manager.
────────────────────────────────────────────────────
```

### Import as a module

```python
from password_checker import analyse

result = analyse("Tr0ub4dor&3")

print(result["score"])       # 75
print(result["rating"])      # Strong
print(result["entropy"])     # 72.1
print(result["suggestions"]) # ['Increase length to 12+ characters...']

for name, (passed, detail) in result["criteria"].items():
    status = "✔" if passed else "✘"
    print(f"{status} {name}: {detail}")
```

### Return value of `analyse()`

```python
{
    "password":    str,
    "score":       int,          # 0–100
    "rating":      str,          # "Very Weak" … "Very Strong"
    "entropy":     float,        # estimated bits
    "criteria": {
        "Length":               (bool, str),
        "Uppercase letters":    (bool, str),
        "Lowercase letters":    (bool, str),
        "Numbers":              (bool, str),
        "Special characters":   (bool, str),
        "Not a common password":(bool, str),
    },
    "suggestions": list[str],
}
```

---

## Project Structure

```
password-checker/
├── password_checker.py   # Core logic + CLI
├── .gitignore
└── README.md
```

---

## Security Note

This tool is for **educational and UX feedback purposes**. It does not store, transmit, or log any passwords. For production authentication, always hash passwords with `bcrypt`, `argon2`, or `scrypt`.

---

© ProDigy Infotech
