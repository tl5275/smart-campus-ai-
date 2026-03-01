<<<<<<< HEAD
# Smart Campus AI

Production-ready FastAPI + Leaflet deployment for smart campus operations.

## Features
- Live monitoring dashboard for bins, water, and energy nodes
- AI risk scoring and decision engine
- OSRM-based road routing for waste pickup
- Zone-aware digital twin simulation
- Multi-page web entrypoints:
  - `/` Landing page
  - `/dashboard` Live operations dashboard
  - `/analytics` Analytics page entry
  - `/digital-twin` Digital twin page entry

## Project Structure
```text
smart-campus-ai/
|-- backend/
|   |-- main.py
|   |-- data_simulator.py
|   `-- models.py
|-- frontend/
|   |-- index.html
|   |-- dashboard.html
|   |-- analytics.html
|   `-- digital-twin.html
|-- requirements.txt
|-- Procfile
|-- .env.example
`-- README.md
```

## Architecture
- **Backend**: FastAPI service exposes simulation + intelligence APIs and serves frontend files.
- **Frontend**: Leaflet + Leaflet Routing Machine dashboard with tabbed operations views.
- **Routing Engine**: OSRM public endpoint for road-constrained pickup routes.
- **Digital Twin**: Scenario + mode controls that influence live risk and forecast outputs.

## Environment Configuration
Set environment variables before running in production:

- `APP_ENV`: `development` or `production`
- `HOST`: bind host (default `0.0.0.0`)
- `PORT`: bind port (default `8000`)
- `CORS_ORIGINS`: comma-separated allowed origins
  - Example: `https://your-app.onrender.com,https://ops.example.com`

When `APP_ENV=development` and `CORS_ORIGINS` is empty, permissive CORS (`*`) is enabled.

## Local Setup
1. Create and activate virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Open:
   - `http://127.0.0.1:8000/` for landing
   - `http://127.0.0.1:8000/dashboard` for dashboard

## Deployment (Render Example)
1. Push this repository to GitHub.
2. In Render, create a **Web Service** from the repo.
3. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables:
   - `APP_ENV=production`
   - `CORS_ORIGINS=https://<your-render-domain>`
5. Deploy.

## Deployment (Railway)
- Railway will detect `Procfile`.
- Ensure the same env vars are configured (`APP_ENV`, `CORS_ORIGINS`).

## Production Notes
- Frontend API calls use relative paths (no localhost hardcoding).
- Page routing is served by FastAPI endpoints (`/`, `/dashboard`, `/analytics`, `/digital-twin`).
- Health endpoint: `/healthz`

## API Endpoints (Core)
- `/bins`
- `/water-nodes`
- `/energy-nodes`
- `/ai-decisions`
- `/digital-twin/status`
- `/digital-twin/config`
- `/forecast`
- `/cost-optimization`
- `/cross-intelligence`
- `/sustainability-score`
=======
# smart-campus-ai
>>>>>>> 9cf8e24d1db5849a63af3628b428298963e1110a
