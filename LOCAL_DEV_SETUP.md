## Local Development (No Docker)

Run the main backend services on your host so the Next.js app can talk to them without the Docker network.

### 1. Python services

Each service ships with a `requirements.txt`. From the repo root:

> **Python version:** use 3.11 (psycopg2 wheels are not yet available for 3.13).

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r userservice/requirements.txt
pip install -r ScreenerService/requirements.txt
pip install -r Prediction-Engine/requirements.txt
```

Then start the APIs (each in its own terminal):

```powershell
cd userservice
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

cd ..\ScreenerService
uvicorn main:app --host 0.0.0.0 --port 8003 --reload

cd ..\Prediction-Engine
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

Other services (portfolio, paper-trading, analytics, subscription, referral, news) follow the same pattern if you need them.

### 2. Environment variables

Create a `.env.local` inside `aitradingnode/` with:

```
PYTHON_API_URL=http://127.0.0.1:8000
USER_SERVICE_URL=http://127.0.0.1:8001
SCREENER_SERVICE_URL=http://127.0.0.1:8003
```

Next.js API routes will fall back to these hosts automatically, but the explicit values make it obvious.

### 3. Frontend

```
cd aitradingnode
npm install
npm run dev
```

Visit `http://localhost:3000`. The new placeholder pages now render, predictions/backtests use mock data when the ML models are missing, and the screener page forwards requests through `/api/screener/search`.

### 4. Optional helpers

- Use `tests/frontend_capability_sanity.py` to confirm each route responds (`python tests/frontend_capability_sanity.py`).
- The legacy `start_all_services.ps1` still works if you want auto-spawned PowerShell windows.

