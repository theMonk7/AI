# Reproducible Environment Setup (Single Source)

Use this section for all setup and environment steps. Do not split setup steps across other files.

## 1) System prerequisites
- Python 3.11 or newer
- pip
- Git
- Optional: Docker Desktop (for n8n in later weeks)

Check versions:
```bash
python3 --version
pip --version
git --version
```

## 2) Clone/open workspace
From the repository root:
```bash
pwd
# expected: /Users/utkarshraj/Documents/Learning/AI
```

## 3) Create isolated Python environment
```bash
python3 -m venv .venv
source .venv/bin/activate
python -V
```

## 4) Install dependencies (pinned by requirements)
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 5) Configure environment variables
```bash
cp .env.example .env
```

Then edit `.env` with your values when needed.
For Week 1, API key is not required for the live API status project.

## 6) Validate setup by running baseline scripts
```bash
python src/weeks/week_01/foundations/async_patterns.py
python src/weeks/week_01/foundations/reliable_client.py
python src/weeks/week_01/llm_core/structured_outputs.py
python -m pytest -q
```

## 7) Run Week 1 live mini-project
```bash
python src/weeks/week_01/projects/week01_live_api_status.py
```

Expected outputs:
- Console summary of API status and latency
- JSON report at `artifacts/week01/api_health_report.json`

## 8) Reproducibility checklist
- `.venv` created and activated
- dependencies installed from `requirements.txt`
- `.env` created
- all baseline scripts run successfully
- tests pass
- Week 1 project report generated

## 9) Common issues and fixes
- `ModuleNotFoundError`: activate `.venv` and reinstall requirements.
- SSL/network errors: retry on stable internet; if blocked, change endpoints in script.
- Wrong Python version: ensure `python3` points to 3.11+.
