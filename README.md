# Job Scraper Service

Lightweight FastAPI service that uses Playwright to fetch job-search JSON from Hiring Cafe.

Current flow:
1. Client (for example n8n) calls a GET endpoint.
2. Service opens Hiring Cafe with Playwright.
3. Service captures the `/api/search-jobs` response.
4. Service returns that JSON payload.

## Requirements

- Python 3.11+
- Docker Desktop (optional, recommended for deployment)

## Local Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Docker Run

Build image:

```powershell
docker build -t jobscraper:latest .
```

Run container:

```powershell
docker run -d --name jobscraper -p 8000:8000 jobscraper:latest
```

View logs:

```powershell
docker logs -f jobscraper
```

Stop/remove:

```powershell
docker stop jobscraper
docker rm jobscraper
```

## API

- `GET /health`
- `GET /jobs/hiringcafe`

Example:

```text
GET http://localhost:8000/jobs/hiringcafe
```

Quick test:

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health"
Invoke-RestMethod -Uri "http://localhost:8000/jobs/hiringcafe"
```

## Response

- Success: raw JSON from Hiring Cafe `/api/search-jobs`
- Failure: `504` with error details if the expected API response is not captured in time

## GitHub Setup

This project is already initialized as a git repo. To commit and push updates:

```powershell
git add .
git commit -m "Update README"
```

Connect to GitHub and push:

```powershell
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

## Troubleshooting

- If endpoint behavior seems old after code changes, rebuild the image and recreate the container:

```powershell
docker stop jobscraper
docker rm jobscraper
docker build -t jobscraper:latest .
docker run -d --name jobscraper -p 8000:8000 jobscraper:latest
```
