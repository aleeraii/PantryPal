# PantryPal

Cook smarter with what you have. PantryPal is a full-stack platform that helps users discover personalized recipes based on the ingredients and utensils they already own — powered by AI agents, a FastAPI backend, a React admin dashboard, and a React Native mobile app.

---

## Repository Structure

```
PantryPal/
├── mobile/          # React Native (Expo) — user-facing mobile app
├── frontend/        # React + Vite — admin dashboard
├── backend/         # FastAPI — REST API + database layer
├── ai/              # Google ADK — AI agents for recipe generation
└── requirements.txt # Shared Python dependencies
```

---

## Services Overview

### `mobile/` — React Native App (Expo)

The primary user-facing application. Built with Expo SDK 54, expo-router, Zustand, and Reanimated.

**Key features:**
- Onboarding slides + kitchen setup wizard (ingredients, utensils, dietary preferences, household size)
- Email and phone-based auth with OTP verification
- AI-powered recipe generator (cuisine + time filters → pantry-matched recipes)
- Recipe detail with ingredients checklist, step-by-step instructions, and nutrition tab
- Pantry management, meal planning calendar, and user profile

See [`mobile/README.md`](mobile/README.md) for full setup instructions and screen inventory.

**Tech:** React Native, Expo SDK 54, expo-router, Zustand, Reanimated, Roboto + Montserrat fonts

---

### `frontend/` — Admin Dashboard (React + Vite)

Internal admin panel for managing the PantryPal platform.

**Planned features:**
- User management (view, suspend, delete accounts)
- Recipe moderation and manual recipe entry
- Ingredient and utensil master list management
- AI request log viewer (costs, latency, errors)
- Analytics dashboard (DAU, recipe generation volume, popular cuisines)
- Meal plan and shopping list oversight

**Tech:** React, Vite, TypeScript, TailwindCSS (planned)

---

### `backend/` — REST API (FastAPI)

The core API layer connecting the mobile app, admin dashboard, and AI agents.

**Current models:**
| Model | Description |
|---|---|
| `User` | Account, auth, dietary preferences, household size |
| `Inventory` | User's ingredients and utensils |
| `Recipe` | Recipe metadata, ingredients, instructions, nutrition |
| `MealPlan` | Weekly meal plan entries per user |
| `ShoppingList` | Auto-generated shopping lists from recipes |
| `UserRecipeHistory` | Recipes generated/saved per user |
| `AIRequestLog` | Logs of AI agent calls (model, tokens, latency, cost) |

**Planned endpoints:**
- `POST /auth/register`, `POST /auth/login`, `POST /auth/otp/verify`
- `GET/PUT /users/{id}/inventory`
- `POST /recipes/generate` — triggers AI agent
- `GET /recipes/{id}`
- `GET/POST /meal-plans`
- `GET /shopping-lists/{user_id}`
- `GET /admin/ai-logs`

**Tech:** FastAPI, SQLAlchemy 2.0+, PostgreSQL (planned), Pydantic, Alembic (planned)

---

### `ai/` — AI Agents (Google ADK)

Autonomous agents responsible for recipe generation and pantry intelligence.

**Planned agents:**
- **Recipe Generator Agent** — takes user pantry + cuisine + time constraints, returns ranked recipe suggestions with pantry match scores
- **Ingredient Matcher Agent** — cross-references user inventory against recipe requirements
- **Meal Plan Agent** — generates a weekly meal plan optimized for pantry usage and dietary preferences
- **Shopping List Agent** — computes the delta between a meal plan and current inventory

**Tech:** Google Agent Development Kit (ADK), Gemini models, LangChain (optional), Python

---

## Data Flow

```
Mobile App
    │
    ├── Auth / Profile / Pantry ──────────────────► FastAPI Backend ──► PostgreSQL
    │                                                      │
    └── Generate Recipe ──────────────────────────► FastAPI Backend
                                                           │
                                                    AI Agent (ADK)
                                                           │
                                                    Gemini Model
                                                           │
                                                    Recipe Results ◄── cached in DB
                                                           │
                                                    ◄── Mobile App

Admin Dashboard ──────────────────────────────────► FastAPI Backend (admin routes)
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (for backend)
- Expo CLI (`npm install -g expo-cli`)
- Google ADK credentials (for AI agents)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r ../requirements.txt
uvicorn main:app --reload
```

### Frontend (Admin Dashboard)

```bash
cd frontend
npm install
npm run dev
```

### Mobile

```bash
cd mobile
npm install
npx expo start
```

### AI Agents

```bash
cd ai
pip install google-adk
# Configure GOOGLE_API_KEY in .env
python agents/recipe_generator.py
```

---

## Environment Variables

Create a `.env` file in each service directory. Never commit `.env` files.

### `backend/.env`
```
DATABASE_URL=postgresql://user:password@localhost:5432/pantrypal
SECRET_KEY=your-jwt-secret
GOOGLE_API_KEY=your-google-api-key
ENVIRONMENT=development
```

### `ai/.env`
```
GOOGLE_API_KEY=your-google-api-key
GOOGLE_CLOUD_PROJECT=your-gcp-project
```

### `frontend/.env`
```
VITE_API_BASE_URL=http://localhost:8000
```

### `mobile/.env`
```
EXPO_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

## TODO — Infrastructure & DevOps

The following items need to be added to the codebase:

### CI/CD — GitHub Actions

- [ ] `/.github/workflows/backend-ci.yml` — lint (ruff), type-check (mypy), run pytest on every PR
- [ ] `/.github/workflows/frontend-ci.yml` — ESLint, TypeScript check, Vite build on every PR
- [ ] `/.github/workflows/mobile-ci.yml` — ESLint, TypeScript check, Expo export dry-run on every PR
- [ ] `/.github/workflows/ai-ci.yml` — lint and unit tests for AI agents on every PR
- [ ] `/.github/workflows/deploy-backend.yml` — deploy to cloud on merge to `main`
- [ ] `/.github/workflows/deploy-frontend.yml` — build and deploy admin dashboard on merge to `main`

### Docker

- [ ] `backend/Dockerfile` — multi-stage Python image (builder + slim runtime)
- [ ] `frontend/Dockerfile` — Node build stage + nginx serve stage
- [ ] `ai/Dockerfile` — Python image for AI agent workers
- [ ] `docker-compose.yml` (root) — orchestrates backend + frontend + postgres + redis (for job queues)
- [ ] `docker-compose.override.yml` — local dev overrides (hot reload, volume mounts)
- [ ] `.dockerignore` files in each service

### Database

- [ ] Set up Alembic in `backend/` for database migrations (`alembic init`, initial migration)
- [ ] `backend/db/session.py` — SQLAlchemy async session factory
- [ ] `backend/db/base.py` — declarative base with common mixins (created_at, updated_at)
- [ ] Seed script `backend/scripts/seed.py` — populate ingredient/utensil master lists

### Backend

- [ ] `backend/main.py` — FastAPI app entry point with CORS, middleware, router registration
- [ ] `backend/core/config.py` — Pydantic Settings class reading from `.env`
- [ ] `backend/core/security.py` — JWT token creation/verification, password hashing
- [ ] `backend/api/routes/` — individual route files (auth, users, recipes, inventory, meal_plans, admin)
- [ ] `backend/api/deps.py` — FastAPI dependency injection (get_db, get_current_user)
- [ ] `backend/schemas/` — Pydantic request/response schemas for all models
- [ ] Rate limiting middleware (slowapi or custom)
- [ ] Structured logging (structlog or loguru)

### Frontend (Admin Dashboard)

- [ ] Scaffold Vite + React + TypeScript project in `frontend/`
- [ ] Set up TailwindCSS + shadcn/ui component library
- [ ] `frontend/src/api/` — typed API client (axios or fetch wrapper)
- [ ] Auth guard (admin-only JWT validation)
- [ ] Route structure: `/dashboard`, `/users`, `/recipes`, `/ai-logs`, `/settings`

### Mobile

- [ ] `mobile/.env` support via `expo-constants` / `EXPO_PUBLIC_` prefix
- [ ] API client (`mobile/lib/api.ts`) — axios instance with auth token injection
- [ ] Error boundary component for graceful crash handling
- [ ] Push notification setup (Expo Notifications)
- [ ] Deep linking configuration in `app.json`

### AI Agents

- [ ] Scaffold `ai/agents/` directory with base agent class
- [ ] `ai/agents/recipe_generator.py` — Recipe Generator Agent
- [ ] `ai/agents/ingredient_matcher.py` — Ingredient Matcher Agent
- [ ] `ai/agents/meal_planner.py` — Meal Plan Agent
- [ ] `ai/agents/shopping_list.py` — Shopping List Agent
- [ ] `ai/tools/` — reusable ADK tools (pantry lookup, recipe DB query)
- [ ] `ai/tests/` — unit tests with mocked Gemini responses

### Security & Quality

- [ ] `backend/` — add `ruff` + `mypy` config to `pyproject.toml`
- [ ] `frontend/` + `mobile/` — ESLint + Prettier config
- [ ] Pre-commit hooks (`.pre-commit-config.yaml`) — lint, format, secret scanning
- [ ] `SECURITY.md` — responsible disclosure policy
- [ ] Dependabot config (`.github/dependabot.yml`) — automated dependency updates for npm and pip

### Documentation

- [ ] `docs/api.md` — OpenAPI/Swagger endpoint reference
- [ ] `docs/architecture.md` — system architecture diagram
- [ ] `docs/deployment.md` — production deployment guide
- [ ] `CONTRIBUTING.md` — branching strategy, PR template, code style guide
- [ ] `CHANGELOG.md` — version history

---

## Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Production-ready code |
| `develop` | Integration branch — all features merge here first |
| `feature/*` | Individual feature branches |
| `fix/*` | Bug fix branches |
| `release/*` | Release candidate branches |

---

## License

Private — All rights reserved.
