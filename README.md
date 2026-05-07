# AI Daily Briefing

A command-line tool that fetches your morning briefing — weather + top news headlines — and saves a history.

## Features
- 🌤️ Current weather via OpenWeatherMap
- 📰 Top headlines via NewsAPI
- 💾 Auto-saves history to `data/history.json`

## Setup

1. Clone the repo:
```bash
   git clone https://github.com/Smadavaram-Kumar/ai-daily-briefing.git
   cd ai-daily-briefing
```

2. Create and activate a virtual environment:
```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1   # Windows PowerShell
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Get free API keys:
   - OpenWeatherMap: https://openweathermap.org/api
   - NewsAPI: https://newsapi.org

5. Copy `.env.example` to `.env` and fill in your keys:
```bash
   copy .env.example .env
```

6. Run it:
```bash
   python main.py
```

## Tech
- Python 3.12
- requests (HTTP client)
- python-dotenv (secrets management)



### Theory 

# Day 6 — Build & Ship Your First Real Python Project

> **What you'll have at the end of this:** A working command-line tool that fetches your morning weather + top news headlines, saves a history, and is pushed to GitHub the **right way** — with proper isolation (`venv`), secrets management (`.env`), and dependency tracking (`requirements.txt`).
>
> This is not a tutorial. This is **the template** for every Python project you'll build for the rest of your career. The skeleton you build today is the same skeleton your AI apps will use on Day 9, your RAG system on Day 15, and your production agent on Day 25.
>
> Buckle up — this is a long one. Read it once start to finish, then go back and implement step by step.

---

## What We're Building: `ai-daily-briefing`

A CLI tool that, when you run it in the morning, prints:
- 🌤️ Current weather in your city
- 📰 Top news headlines
- 💾 Saves the briefing to `data/history.json`

**Why this specific project?**

| Reason | Why it matters |
|---|---|
| Uses **two real APIs at once** | That's how real apps work. No one-API toy. |
| Same shape as **every AI agent** | `fetch → fetch → combine → save` is what RAG, agents, and AI tools do. |
| **Actually useful** | You'll run it tomorrow morning. Real motivation. |
| Forces **secrets, errors, file I/O** | The three things that break in production. |
| Bridges to **Day 9 (Claude API)** | Stretch goal: send headlines to Claude, get an AI summary. |

---

## The Final Folder Structure (Where We're Heading)

```
ai-daily-briefing/
│
├── .env                    🔒 SECRET — your real API keys (gitignored)
├── .env.example            ✅ Template with fake values (committed)
├── .gitignore              ✅ Tells Git what to ignore
├── README.md               ✅ Project description
├── requirements.txt        ✅ List of Python libraries needed
│
├── venv/                   📦 Isolated Python environment (gitignored)
│   ├── Scripts/            (Windows: python.exe, pip.exe, activate scripts)
│   └── Lib/site-packages/  (where requests, dotenv get installed)
│
├── main.py                 🚀 Entry point — what you run
├── weather.py              🌤️ Talks to OpenWeatherMap API
├── news.py                 📰 Talks to NewsAPI
│
└── data/                   💾 Output folder (gitignored)
    └── history.json        ⚠️ Auto-generated
```

**Why split code into 3 files?** Same reason you don't put 50 actions in one Power Automate flow — break it by responsibility:
- `weather.py` → "How do I get weather?"
- `news.py` → "How do I get news?"
- `main.py` → "Combine them and show the user"

This is **separation of concerns** — universal in every codebase. Each file has ONE job; easy to swap out (replace NewsAPI? just edit `news.py`).

---

## The Big Picture: The Three Pillars

Every Python project rests on three pillars. Today you learn all three.

```
   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
   │   requests   │    │   dotenv     │    │     venv     │
   │              │    │              │    │              │
   │ Talk to APIs │    │ Hide secrets │    │ Isolate deps │
   └──────────────┘    └──────────────┘    └──────────────┘
          │                   │                   │
          └───────────────────┴───────────────────┘
                              │
                    Foundation of every Python AI app
```

| Pillar | What it does | Power Platform parallel |
|---|---|---|
| `requests` | HTTP calls to APIs | The HTTP connector |
| `python-dotenv` | Manages API keys safely | Connection references / Key Vault |
| `venv` | Each project gets isolated dependencies | Dev/Test/Prod environments |

---

## Step 0 — Get Your API Keys First (15 mins, includes wait time)

Do this FIRST because OpenWeather keys take ~10 minutes to activate. While you wait, you can set up the project.

### Key 1 — OpenWeatherMap (Weather)

1. Go to **https://openweathermap.org/**
2. Top right → **"Sign In"** → **"Create an Account"**
3. Email, username, password, check the boxes
4. Confirm via email (check spam)
5. After login → click your username (top right) → **"My API keys"**
6. Default key is already created. **Copy it.**
7. ⚠️ **New keys take ~10 minutes to activate.** If you get `401 Unauthorized` immediately, just wait.

**What it looks like:** `abc123def456ghi789jkl012mno345pq` — 32-character hex string.

### Key 2 — NewsAPI (News Headlines)

1. Go to **https://newsapi.org/**
2. Click **"Get API Key"**
3. Name, email, password, "personal/individual"
4. Your API key appears on the dashboard immediately
5. **Copy it.**

**Free tier limits:** 100 requests/day, only works from `localhost` (your computer). Perfect for learning.

### Save Both Keys Temporarily

Open Notepad. Paste:
```
OpenWeatherMap: paste-your-key-here
NewsAPI: paste-your-key-here
```

Save it somewhere — we'll move them into `.env` shortly. **Don't put them in your project folder yet.**

---

## The 8-Step Workflow

This is the **template for every Python project** you'll build going forward. Memorize this order — it matters.

```
1. Create project folder
2. Create .gitignore        ← BEFORE anything else
3. Create venv
4. Activate venv
5. Create .env + .env.example
6. Install dependencies → freeze requirements.txt
7. Write code
8. Initialize git, commit, push
```

Now we walk through each step.

---

## Step 1 — Create the Project Folder

Open PowerShell. Navigate to wherever you keep projects (Desktop, OneDrive, etc.):

```powershell
cd "$env:USERPROFILE\Desktop"
```

Create the project folder and enter it:

```powershell
mkdir ai-daily-briefing
cd ai-daily-briefing
```

Verify you're in the right place:
```powershell
pwd
```

Should print: `C:\Users\smadavaram\Desktop\ai-daily-briefing`

> **Don't open VS Code yet.** We'll do that in Step 4 after the venv exists, so VS Code can detect it automatically.

---

## Step 2 — Create `.gitignore` FIRST (Critical Timing!)

> ⚠️ **This MUST happen before you ever run `git add`.** Once Git starts tracking a file, adding it to `.gitignore` later does NOT untrack it. The file stays in Git history forever, and bots already found your secrets. Do this first, every time.

### What is `.gitignore`?

A plain text file that tells Git: **"Ignore these files. Don't track them, don't commit them, pretend they don't exist."**

Without it, every file gets pushed to GitHub — including:
- 🚨 `.env` (your secret API keys → bots steal them within 60 seconds)
- 🚨 `__pycache__/` (Python's bytecode cache → useless clutter)
- 🚨 `venv/` (could be 500MB+ → clogs the repo)
- 🚨 `data/history.json` (your runtime output → not source code)

### Pattern Syntax — How `.gitignore` Works

| Pattern | What It Matches | Example |
|---|---|---|
| `filename` | Specific file anywhere | `.env` matches `.env` in any folder |
| `*.ext` | All files with that extension | `*.pyc` matches all compiled Python |
| `foldername/` | Folder and everything inside | `venv/` ignores entire folder |
| `/filename` | Only at project root | `/config.json` only at root |
| `# comment` | Comment line | `# Secrets section` |
| `!pattern` | Un-ignore (exception) | `!keep-this.log` |

### Create the File

In PowerShell:
```powershell
New-Item .gitignore
```

Open it in Notepad (or VS Code if already installed) and paste this **production-ready `.gitignore`**:

```gitignore
# ─────────────────────────────────────────────────────
# SECRETS — most important section
# ─────────────────────────────────────────────────────
.env
.env.local
.env.*.local
*.key
*.pem

# ─────────────────────────────────────────────────────
# Python build artifacts
# ─────────────────────────────────────────────────────
__pycache__/
*.pyc
*.pyo
*.egg-info/
build/
dist/

# ─────────────────────────────────────────────────────
# Virtual environments — huge, machine-specific
# ─────────────────────────────────────────────────────
venv/
.venv/
env/
ENV/

# ─────────────────────────────────────────────────────
# IDE / editor settings
# ─────────────────────────────────────────────────────
.vscode/
.idea/
*.swp

# ─────────────────────────────────────────────────────
# OS junk
# ─────────────────────────────────────────────────────
.DS_Store
Thumbs.db
desktop.ini

# ─────────────────────────────────────────────────────
# Project-specific output
# ─────────────────────────────────────────────────────
data/
*.log
output/

# ─────────────────────────────────────────────────────
# Jupyter (used later in the journey)
# ─────────────────────────────────────────────────────
.ipynb_checkpoints/
```

Save it. **Done. We can now safely create the rest.**

> **Notice `venv/` and `data/` are in there from the start** — even though they don't exist yet. That's intentional. By the time we create them, Git already knows to ignore them.

---

## Step 3 — Create the `venv` (Your Project's Private Python)

### What `venv` Actually Is

Your intuition was right: **a container for dependencies.** Let's make that precise.

A `venv` is **literally just a folder** containing:
- A copy of Python (`python.exe`)
- Its own `pip`
- Its own `site-packages/` folder where libraries get installed
- An activation script

When you "activate" it, your terminal temporarily uses the venv's Python instead of your global Python. When you `pip install requests`, it goes into the venv's `site-packages/` — **not your global Python**.

### Why Bother? The Disaster Scenarios

```
Without venv:

  Project A: ai-daily-briefing  → needs requests==2.31.0
  Project B: mcp-claude-server  → needs requests==2.20.0

  pip install requests==2.20.0     (for Project B)
  → Now Project A breaks
  pip install requests==2.31.0     (back for Project A)
  → Now Project B breaks

  Infinite swap. Welcome to dependency hell.
```

```
Without venv:

  pip freeze > requirements.txt
  → Lists EVERY library from EVERY project you ever installed.
  → Friend clones your repo, runs pip install -r requirements.txt.
  → Half the packages fail. They quit your project.
```

```
With venv:

  Each project has its own isolated Python.
  Projects can't see each other.
  Projects can't break each other.
  pip freeze gives you ONLY what this project uses.
  Clean. Reproducible. Professional.
```

### The Container Analogy — Where It Holds and Where It Breaks

| Your intuition | Reality |
|---|---|
| ✅ Isolated from other projects | True — packages don't leak between venvs |
| ✅ Has its own dependencies | True — own `site-packages/` folder |
| ✅ Can be destroyed/recreated | True — just delete the folder |
| ❌ Like a Docker container running in background | False — NOT running anything. Just files on disk. |
| ❌ Sandboxed from the OS | False — only isolates *Python packages*. Filesystem/network still accessible. |

**Better analogy:** A `venv` is like a separate Power Platform **environment** (Dev/Test/Prod). Each has its own solutions, connections, configs. They don't pollute each other. Same idea — for Python projects.

### Create It

```powershell
python -m venv venv
```

**Decoding the command:**
- `python` — Run Python
- `-m venv` — Use Python's built-in `venv` module
- `venv` — Name the folder `venv` (convention)

Takes ~5 seconds. You should now see a `venv/` folder in your project.

**Verify it exists:**
```powershell
ls
```

You should see: `.gitignore`, `venv`

---

## Step 4 — Activate the venv (PATH Magic)

### How Activation Actually Works

Remember Day 1, where you learned PATH determines which `python.exe` runs? `venv` exploits exactly that.

**Before activation:**
```
PATH = "C:\Windows\System32;C:\...\Python\Python312;..."

You type:  python
Computer searches PATH → finds Python312\python.exe → runs GLOBAL Python.
```

**The activation script does ONE thing:**
```
PATH = "C:\my-project\venv\Scripts;<original PATH>"
              ↑
       Prepends venv's folder
```

**After activation:**
```
You type:  python
Computer searches PATH → finds venv\Scripts\python.exe FIRST → runs VENV Python.
You type:  pip install requests
Computer finds venv's pip → installs INTO venv\Lib\site-packages\
```

**That's the entire trick.** No magic, just PATH manipulation. This is why understanding PATH from Day 1 was so important.

### Activate It

```powershell
.\venv\Scripts\Activate.ps1
```

> **If you get this error:**
> ```
> .\venv\Scripts\Activate.ps1 : File ... cannot be loaded because running scripts is disabled on this system.
> ```
> Windows blocks scripts by default. Fix it ONCE, forever:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> - `-Scope CurrentUser` — only your account, no admin needed
> - `-ExecutionPolicy RemoteSigned` — allows local scripts
>
> Then retry activation.

**Success indicator:** Your prompt now starts with `(venv)`:
```
(venv) PS C:\Users\smadavaram\Desktop\ai-daily-briefing>
```

The `(venv)` prefix is your **safety light**. It means: "Anything I `pip install` right now goes into this project's venv, not global." If you ever don't see `(venv)`, STOP and activate first.

### Verify the Isolation

Before installing anything:

```powershell
pip list
```

You should see ONLY:
```
Package    Version
---------- -------
pip        24.x.x
setuptools xx.x.x
```

**That's it!** None of your globally installed packages. Fresh, isolated Python.

```powershell
where.exe python
```

Should show TWO paths, **venv first**:
```
C:\Users\smadavaram\Desktop\ai-daily-briefing\venv\Scripts\python.exe
C:\Users\smadavaram\AppData\Local\Programs\Python\Python312\python.exe
```

The venv comes first → that's why it gets used.

### Open VS Code Now

```powershell
code .
```

VS Code is smart about venvs:
1. Press `Ctrl+Shift+P`
2. Type: `Python: Select Interpreter`
3. Pick the one ending in `venv\Scripts\python.exe`

After this:
- Every new VS Code terminal **auto-activates the venv**
- Pylance autocomplete uses venv's packages
- F5 / Run button uses venv Python

**One-time setup. Then everything just works.**

---

## Step 5 — Create `.env` and `.env.example` (Secrets Management)

### Why You Should Be Scared of API Keys

Your API key is **money**. Anyone who has it can spend your account dry. Bots scan GitHub 24/7 looking for committed keys — they've been measured to find and abuse keys **within 60 seconds** of public commit.

```python
# main.py — pushed to GitHub
API_KEY = "sk-ant-real-key-here"   # ← The mistake

git add .
git commit -m "first AI app"
git push                       # ← Key now public
                               # ← Bots find it within minutes
                               # ← Account drained
                               # ← You wake up to an angry email
```

**Even if you delete the file later, it's still in Git history forever.** The only fix is to revoke the key and generate a new one.

### The `.env` Pattern

```
your-project/
├── .env                ← REAL secrets (NEVER committed — already in .gitignore ✅)
├── .env.example        ← TEMPLATE with fake values (committed, helps teammates)
└── main.py             ← Reads from .env via os.getenv()
```

### Create the Files

In PowerShell:
```powershell
New-Item .env
New-Item .env.example
```

### Fill `.env.example` (the committed template)

Open `.env.example` in VS Code, paste:

```
# OpenWeatherMap — get yours at https://openweathermap.org/api
OPENWEATHER_API_KEY=your-openweathermap-key-here

# NewsAPI — get yours at https://newsapi.org
NEWSAPI_KEY=your-newsapi-key-here

# Your default city for weather
DEFAULT_CITY=Hyderabad

# News country code (us, in, gb, ca, au, ...)
NEWS_COUNTRY=in
```

Save.

### Fill `.env` (your REAL keys, gitignored)

Open `.env` in VS Code, paste — but with your **real keys** from Notepad:

```
OPENWEATHER_API_KEY=abc123yourrealopenweatherkey456
NEWSAPI_KEY=xyz789yourrealnewsapikey012
DEFAULT_CITY=Hyderabad
NEWS_COUNTRY=in
```

> **Format rules:**
> - No spaces around `=` (write `KEY=value`, not `KEY = value`)
> - No quotes needed (don't write `KEY="value"`)
> - One key per line
> - Comments start with `#`

Save. **Now delete the keys from your Notepad file** — they live in `.env` only.

### Safety Check

```powershell
git status
```

Wait — we haven't initialized Git yet. We'll verify after we do, in Step 8. For now, trust that `.gitignore` already lists `.env`, so it'll be safe.

---

## Step 6 — Install Dependencies → Freeze Requirements

### Install

With venv active (you should see `(venv)` in prompt):

```powershell
pip install requests python-dotenv
```

These install into `venv\Lib\site-packages\`, **not your global Python**. Verify:

```powershell
pip list
```

Should now show:
```
Package          Version
---------------- -------
certifi          2024.x.x
charset-normalizer x.x.x
idna             x.x
pip              24.x.x
python-dotenv    1.0.0
requests         2.31.0
setuptools       xx.x.x
urllib3          x.x.x
```

The `requests` package brought a few helpers with it (certifi, idna, etc.) — that's normal, those are sub-dependencies.

### Freeze to `requirements.txt`

```powershell
pip freeze > requirements.txt
```

**What this command does:**
- `pip freeze` — list every installed package with exact version
- `>` — redirect output into a file
- `requirements.txt` — the file (created if missing)

Open `requirements.txt`. You'll see something like:
```
certifi==2024.x.x
charset-normalizer==x.x.x
idna==x.x
python-dotenv==1.0.0
requests==2.31.0
urllib3==x.x.x
```

**This is THE critical reason for venv:** without it, `pip freeze` would dump every package from every project you've ever touched. With venv, it's clean — only what THIS project uses.

> **Why pin versions (`==2.31.0`)?** So when someone (or future-you) clones the repo and runs `pip install -r requirements.txt`, they get the EXACT same versions you used. No "works on my machine" surprises.

---

## Step 7 — Write the Code

Time to actually build the thing. Three files: `weather.py`, `news.py`, `main.py`.

### Reading API Docs — The Skill That Multiplies Everything

Before we write code, here's how to read API docs. Once you can read one, you can read any.

**Anatomy of an API doc page (OpenWeatherMap):**

Open https://openweathermap.org/current. You'll see:

```
URL TEMPLATE:
https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}

PARAMETERS TABLE:
┌──────────┬──────────┬─────────────────────┐
│ q        │ required │ City name           │
│ appid    │ required │ Your API key        │
│ units    │ optional │ standard|metric|... │
│ lang     │ optional │ language code       │
└──────────┴──────────┴─────────────────────┘

EXAMPLE RESPONSE:
{ "main": { "temp": 22.5, ... }, "weather": [...], ... }
```

**Translation to Python:**

| Doc says | Python code |
|---|---|
| `https://api.openweathermap.org/data/2.5/weather` | `url = "..."` (first arg to `requests.get`) |
| `?q={city name}` | `params={"q": "Hyderabad"}` |
| `&appid={API key}` | `params={"appid": "your-key"}` |
| Required parameter | Must include in `params` |
| Optional parameter | Include only if you want it |

```
Doc URL:  ...weather?q=Hyderabad&appid=KEY&units=metric
                     └──────────params──────────┘

Python:   requests.get(
              "https://api.openweathermap.org/data/2.5/weather",
              params={"q": "Hyderabad", "appid": "KEY", "units": "metric"}
          )
```

`requests` builds the `?q=...&appid=...` part for you. Always pass via `params=`.

**For NewsAPI** (https://newsapi.org/docs/endpoints/top-headlines):

```
URL: https://newsapi.org/v2/top-headlines

Parameters:
  country   - 2-letter code (us, in, gb, ...)
  pageSize  - number of results
  apiKey    - your key (or use X-Api-Key header — preferred)
```

> **Why headers > params for keys:** Headers don't appear in browser history, server logs, or URLs. **Best practice: if both options are offered, use headers for keys.** Keep params for non-secret data.

### File 1 — `weather.py`

In VS Code, create `weather.py` and paste:

```python
"""
weather.py
Handles all OpenWeatherMap API interactions.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> dict:
    """
    Fetch current weather for a city.
    Returns a clean dict with what we care about, or raises an exception.
    """
    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY not set in .env file")

    try:
        response = requests.get(
            BASE_URL,
            params={
                "q": city,
                "appid": API_KEY,
                "units": "metric"   # Celsius. Use "imperial" for Fahrenheit.
            },
            timeout=10
        )
        response.raise_for_status()
        raw = response.json()

        # Extract just what we need (clean output)
        return {
            "city": raw["name"],
            "country": raw["sys"]["country"],
            "temp": raw["main"]["temp"],
            "feels_like": raw["main"]["feels_like"],
            "humidity": raw["main"]["humidity"],
            "description": raw["weather"][0]["description"].title(),
            "wind_speed": raw["wind"]["speed"],
        }

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid OpenWeather API key (or wait 10 mins after signup)")
        elif e.response.status_code == 404:
            raise ValueError(f"City '{city}' not found")
        raise

    except requests.exceptions.Timeout:
        raise TimeoutError("OpenWeather request timed out")
```

### File 2 — `news.py`

Create `news.py`, paste:

```python
"""
news.py
Handles all NewsAPI interactions.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWSAPI_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"


def get_top_headlines(country: str = "us", limit: int = 5) -> list:
    """
    Fetch top news headlines for a country.
    Returns a list of dicts with title, source, url.
    """
    if not API_KEY:
        raise ValueError("NEWSAPI_KEY not set in .env file")

    try:
        response = requests.get(
            BASE_URL,
            params={
                "country": country,
                "pageSize": limit
            },
            headers={"X-Api-Key": API_KEY},   # Key in HEADER (more secure)
            timeout=10
        )
        response.raise_for_status()
        raw = response.json()

        # Clean the response into just what we need
        articles = []
        for article in raw.get("articles", []):
            articles.append({
                "title": article.get("title", "No title"),
                "source": article.get("source", {}).get("name", "Unknown"),
                "url": article.get("url", ""),
            })
        return articles

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid NewsAPI key")
        elif e.response.status_code == 429:
            raise ValueError("NewsAPI rate limit hit (100/day on free tier)")
        raise

    except requests.exceptions.Timeout:
        raise TimeoutError("NewsAPI request timed out")
```

### File 3 — `main.py` (The Orchestrator)

Create `main.py`, paste:

```python
"""
main.py
Daily Briefing — runs the whole show.
"""
import os
import json
from datetime import datetime
from dotenv import load_dotenv

from weather import get_weather
from news import get_top_headlines

load_dotenv()

DEFAULT_CITY = os.getenv("DEFAULT_CITY", "London")
NEWS_COUNTRY = os.getenv("NEWS_COUNTRY", "us")
HISTORY_FILE = "data/history.json"


def print_weather(weather: dict) -> None:
    """Pretty-print the weather block."""
    print("\n" + "=" * 50)
    print(f"🌤️  WEATHER — {weather['city']}, {weather['country']}")
    print("=" * 50)
    print(f"  Condition:    {weather['description']}")
    print(f"  Temperature:  {weather['temp']}°C (feels like {weather['feels_like']}°C)")
    print(f"  Humidity:     {weather['humidity']}%")
    print(f"  Wind speed:   {weather['wind_speed']} m/s")


def print_news(articles: list) -> None:
    """Pretty-print the news block."""
    print("\n" + "=" * 50)
    print("📰 TOP HEADLINES")
    print("=" * 50)
    for i, article in enumerate(articles, start=1):
        print(f"  {i}. {article['title']}")
        print(f"     ↳ {article['source']}")
        print(f"     {article['url']}\n")


def save_history(weather: dict, articles: list) -> None:
    """Append today's briefing to history.json."""
    os.makedirs("data", exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "weather": weather,
        "news": articles
    }

    # Load existing history (if any)
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    history.append(entry)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Saved briefing to {HISTORY_FILE}")


def main():
    print(f"\n📅 Daily Briefing — {datetime.now().strftime('%A, %B %d, %Y')}")

    # Step 1: Fetch weather
    try:
        weather = get_weather(DEFAULT_CITY)
        print_weather(weather)
    except Exception as e:
        print(f"\n❌ Weather failed: {e}")
        weather = None

    # Step 2: Fetch news
    try:
        articles = get_top_headlines(country=NEWS_COUNTRY, limit=5)
        print_news(articles)
    except Exception as e:
        print(f"\n❌ News failed: {e}")
        articles = []

    # Step 3: Save (only if at least one succeeded)
    if weather or articles:
        save_history(weather or {}, articles)

    print("\n✅ Done.\n")


if __name__ == "__main__":
    main()
```

### File 4 — `README.md`

Create `README.md`, paste:

```markdown
# AI Daily Briefing

A command-line tool that fetches your morning briefing — weather + top news headlines — and saves a history.

## Features
- 🌤️ Current weather via OpenWeatherMap
- 📰 Top headlines via NewsAPI
- 💾 Auto-saves history to `data/history.json`

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/Smadavaram-Kumar/ai-daily-briefing.git
   cd ai-daily-briefing
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1   # Windows PowerShell
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Get free API keys:
   - OpenWeatherMap: https://openweathermap.org/api
   - NewsAPI: https://newsapi.org

5. Copy `.env.example` to `.env` and fill in your keys:
   ```bash
   copy .env.example .env
   ```

6. Run it:
   ```bash
   python main.py
   ```

## Tech
- Python 3.12
- requests (HTTP client)
- python-dotenv (secrets management)
```

### Run It!

In your VS Code terminal (with `(venv)` showing):

```powershell
python main.py
```

**Expected output:**
```
📅 Daily Briefing — Tuesday, May 05, 2026

==================================================
🌤️  WEATHER — Hyderabad, IN
==================================================
  Condition:    Clear Sky
  Temperature:  32.1°C (feels like 35.4°C)
  Humidity:     45%
  Wind speed:   3.6 m/s

==================================================
📰 TOP HEADLINES
==================================================
  1. Some news headline here...
     ↳ Reuters
     https://...
  2. Another headline...
     ↳ BBC News
     https://...
  ...

💾 Saved briefing to data/history.json

✅ Done.
```

🎉 **You just built your first multi-API Python tool.**

Run it again. Look in `data/history.json` — both runs are saved.

#### Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'requests'` | venv not activated. Run `.\venv\Scripts\Activate.ps1` |
| `Invalid OpenWeather API key` | Wait 10 min after signup. Check for trailing spaces in `.env` |
| `City 'XYZ' not found` | Try a bigger city name. OpenWeatherMap is picky about spelling. |
| `NewsAPI rate limit hit` | Free tier is 100/day. Wait 24h or test with weather only |
| Output prints garbled emojis | Windows terminal encoding. Try Windows Terminal app instead of legacy console |

---

## Step 8 — Push to GitHub Safely

### Initialize Git

```powershell
git init
```

### THE CRITICAL SAFETY CHECK

```powershell
git status
```

**Look at the list carefully:**

✅ **MUST appear** (these get committed):
- `.gitignore`
- `.env.example`
- `README.md`
- `requirements.txt`
- `main.py`
- `weather.py`
- `news.py`

❌ **MUST NOT appear** (these are gitignored):
- `.env` ← if this appears, STOP, fix `.gitignore` first
- `venv/`
- `data/`
- `__pycache__/`

If `.env` appears: open `.gitignore`, make sure `.env` is on its own line with no typo, save, run `git status` again.

### Commit & Push

```powershell
git add .
git commit -m "Day 6: AI Daily Briefing — first multi-API Python project"
```

Now create a new repo on **github.com**:
1. Click `+` (top right) → New repository
2. Name: `ai-daily-briefing`
3. Description: "Daily weather + news CLI tool. Day 6 of my AI Engineering Journey."
4. **Do NOT** check "Add a README" or "Add .gitignore" (we have them already)
5. Click "Create repository"

GitHub shows you setup instructions. Use the "push existing repository" block:

```powershell
git branch -M main
git remote add origin https://github.com/Smadavaram-Kumar/ai-daily-briefing.git
git push -u origin main
```

### Verify on GitHub

Go to your repo URL in the browser. **Verify visually:**
- ✅ See: `main.py`, `weather.py`, `news.py`, `.env.example`, `.gitignore`, `README.md`, `requirements.txt`
- ❌ Should NOT see: `.env`, `data/`, `venv/`, `__pycache__/`

If `.env` is visible on GitHub:
1. **Revoke both API keys IMMEDIATELY** at OpenWeatherMap and NewsAPI dashboards
2. Generate new keys, update `.env` locally
3. Run `git rm --cached .env`, commit, push
4. (The old commit still exists in history — assume those keys are burned forever)

---

## "Help, I Already Committed `.env`!" — Rescue Procedure

If you ever push `.env` by mistake (this project or future ones):

**Step 1 — Revoke the leaked keys IMMEDIATELY**
- OpenWeatherMap → API Keys → delete leaked → generate new
- NewsAPI → Dashboard → reset key
- (For Claude/OpenAI later: same — revoke first, ask questions later)

**Step 2 — Remove from Git tracking**
```powershell
git rm --cached .env              # Stop tracking, keep local file
git commit -m "Remove .env from tracking"
git push
```

**Step 3 — Update `.env` with new keys** locally. Don't push.

The leaked commit is still in history — but the keys are dead, so it doesn't matter.

---

## Why You Should NEVER Commit `venv/`

Just to drill this in. Check the size:

```powershell
(Get-ChildItem venv -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
```

A typical venv: **150–500 MB**. With AI libraries (LangChain, transformers): **1–3 GB**.

| Reason | Why |
|---|---|
| **Huge** | GitHub size limits, slow clones |
| **Machine-specific** | Your venv has Windows binaries — Linux server can't use them |
| **Pointless** | `requirements.txt` already lists what's needed |
| **Bad practice** | No professional repo commits venvs |

**The pattern:** Commit the **recipe** (`requirements.txt`), not the **cake** (`venv/`).

When someone clones your repo, they:
```bash
git clone ...
cd ai-daily-briefing
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

In 30 seconds they have an identical environment.

---

## Daily Workflow (After Today)

**When you come back tomorrow to work on this project:**

```powershell
cd "$env:USERPROFILE\Desktop\ai-daily-briefing"
.\venv\Scripts\Activate.ps1     # Reactivate venv (must do every session!)
code .                           # Open VS Code
# ... write code, run python main.py ...
git add .
git commit -m "What you did today"
git push
```

That's it. The venv was created once; you only **activate** it each session, never recreate.

**When you start a new project (Day 9, etc.):**

The 8-step workflow. Same every time. Memorize it:

```
1. mkdir my-new-project && cd my-new-project
2. Create .gitignore (paste the production version)
3. python -m venv venv
4. .\venv\Scripts\Activate.ps1
5. Create .env and .env.example
6. pip install <packages> && pip freeze > requirements.txt
7. Write code
8. git init, commit, create GitHub repo, push
```

---

## Bonus Challenges (Once Basic Version Works)

1. **CLI arguments** — Use `sys.argv` to override the city: `python main.py Mumbai`
2. **Multiple cities** — Show weather for 3 cities at once; highlight the hottest
3. **News by category** — Add `NEWS_CATEGORY` to `.env` (technology, business, etc.)
4. **Email it to yourself** — Use Python's `smtplib` to send the briefing as email
5. **Schedule it** — Use Windows Task Scheduler to run at 7am daily
6. **Markdown report** — Generate `briefings/2026-05-05.md` instead of just JSON
7. **🌟 Day 9 stretch goal:** Send the news headlines to Claude API and have it summarize them in 3 sentences. That moment turns this from a CLI tool into a real **AI product**.

That last one is the bridge to your AI Engineering future. The skeleton you built today (fetch → fetch → combine → save) becomes (fetch → fetch → **send to AI** → get smarter output → save). That's an AI agent.

---

## Common Pitfalls

| Mistake | Symptom | Fix |
|---|---|---|
| Forgot to activate venv before `pip install` | Package goes global, project still missing it | Activate venv, install again |
| Forgot to activate before `python main.py` | `ModuleNotFoundError` even though "installed" | Activate venv first |
| Committed `venv/` to GitHub | Massive repo, slow clones | `git rm -r --cached venv`, ensure in `.gitignore` |
| Activation script blocked | "Running scripts is disabled" | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| Renamed/moved project folder | venv breaks (hardcoded paths) | Delete venv, recreate, `pip install -r requirements.txt` |
| Forgot `load_dotenv()` | `os.getenv()` returns `None` | Add `load_dotenv()` at top of script |
| Forgot `timeout=` | Script hangs forever | Always pass `timeout=` to `requests` |
| Used `data=` instead of `json=` | API returns 400 | Use `json=` for JSON APIs |
| Forgot `.raise_for_status()` | Errors silently ignored | Always call after `.get()`/`.post()` |
| Hardcoded API key in code | Bot drains account | Use `.env` from day one |
| `.env` has trailing spaces | 401 Unauthorized | Check for invisible whitespace |
| `.env` values have quotes | Value includes the quotes | Remove quotes |

---

## The Two Rules That Will Save You Hours

1. **If `(venv)` is not in your prompt, you're not in the venv.** Period. New terminal? Activate again. Closed VS Code? Activate again. Always check before `pip install`.

2. **One venv per project.** Don't reuse a venv across projects "to save space." That defeats the entire point. Disk is cheap; debugging conflicts is not.

---

## Cheat Sheet — The Whole Workflow

```powershell
# ─── ONE-TIME SETUP (per project) ──────────────────────
mkdir my-project && cd my-project
# (paste production .gitignore into .gitignore)
python -m venv venv
.\venv\Scripts\Activate.ps1
# (create .env and .env.example)
pip install requests python-dotenv
pip freeze > requirements.txt

# ─── DAILY WORK ────────────────────────────────────────
cd my-project
.\venv\Scripts\Activate.ps1     # ALWAYS first
code .
# ... write code ...
python main.py
git add .
git commit -m "What I did today"
git push

# ─── ONBOARDING A TEAMMATE / NEW MACHINE ───────────────
git clone https://github.com/USER/REPO.git
cd REPO
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# (edit .env with their own keys)
python main.py

# ─── LEAVING THE VENV ──────────────────────────────────
deactivate

# ─── DELETE A VENV (no uninstall — just delete folder) ─
Remove-Item -Recurse -Force venv

# ─── ONE-TIME WINDOWS FIX (if scripts blocked) ─────────
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

## What You Just Learned (Big Picture)

This isn't just "I made two API calls." You built the **fundamental pattern of every AI app**:

```
Input ──▶ Fetch from API 1 ──▶ Fetch from API 2 ──▶ Combine ──▶ Save/Display
                  │                     │
              (weather)               (news)
```

Every AI app you'll build follows this shape:
- **A chatbot** = User input → Fetch from Claude API → Display
- **A RAG system** = User question → Fetch from vector DB → Fetch from Claude → Display
- **An agent** = Goal → Loop(Fetch from tool API → Fetch from Claude → Decide next action) → Display

You also internalized **the three foundations**:
- `requests` → talking to any service on the internet
- `python-dotenv` → keeping secrets safe
- `venv` → keeping projects isolated and reproducible

The rest of the journey is **filling in different APIs** in those boxes.

---

> **Note to future me:** The 8-step workflow isn't ceremony — every piece exists because I learned the hard way why it matters. `.gitignore` first prevents leaks. `venv` prevents dependency hell. `.env` separates secrets from code. `requirements.txt` makes the project reproducible. Splitting `weather.py` and `news.py` makes it easy to swap providers without touching `main.py`. This skeleton scales from a 100-line CLI to a production AI app — same shape, just more files. Reuse this template for every project from Day 6 onward. If something feels off, check: am I in `(venv)`? Is `.env` in `.gitignore`? Did I `pip freeze`? 90% of bugs are one of these three.

> **Power Platform parallel:** Day 6 is your "HTTP connector + Connection References + Environment isolation," all in one. No flow runs limit, no licensing, runs anywhere, infinitely faster. Same mental model: trigger → action → parse response, with secrets externalized and environments isolated. Different power level entirely.