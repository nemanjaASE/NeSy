# NeSy Frontend

React + TypeScript + Vite client for the NeSy FastAPI backend.

## Setup

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

The development server runs on:

```text
http://localhost:5173
```

## Environment

Frontend settings live in `.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_VERSION=v1
VITE_APP_NAME=NeSy Diagnostic Client
```

The Vite dev server also proxies `/api` and `/health` to `http://localhost:8000`.

## Backend CORS

In `backend/.env`, allow the frontend origin when calling the backend directly:

```env
ALLOWED_ORIGINS=http://localhost:5173
ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS
ALLOWED_HEADERS=Content-Type,Authorization
ALLOW_CREDENTIALS=false
```

## API Modules

Diagnostic calls are prepared in:

```text
src/features/diagnostics/api.ts
```
