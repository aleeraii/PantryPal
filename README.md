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
- [x] `RELEASE.md` per sub-project — version history (auto-generated, see Versioning section above)

---

## Versioning & Release Workflow

PantryPal uses [Conventional Commits](https://www.conventionalcommits.org/) enforced by **commitlint** + **Husky**, and per-sub-project semantic versioning managed by **standard-version** (mobile) and **bump-my-version** + **git-cliff** (backend, frontend, ai).

Each sub-project is versioned independently and maintains its own `RELEASE.md` changelog.

| Sub-project | Current version source | Changelog |
|---|---|---|
| `mobile` | `mobile/package.json` + `mobile/app.json` | [`mobile/RELEASE.md`](mobile/RELEASE.md) |
| `backend` | `backend/VERSION` + `backend/pyproject.toml` | [`backend/RELEASE.md`](backend/RELEASE.md) |
| `frontend` | `frontend/VERSION` + `frontend/pyproject.toml` | [`frontend/RELEASE.md`](frontend/RELEASE.md) |
| `ai` | `ai/VERSION` + `ai/pyproject.toml` | [`ai/RELEASE.md`](ai/RELEASE.md) |

---

### New Developer Setup

After cloning, run these once to activate commit linting and install Python release tools:

```bash
npm install              # installs husky + commitlint, activates the git commit-msg hook
npm run setup:python     # creates .venv and installs bump-my-version + git-cliff
cd mobile && npm install
```

---

### How to Write Commit Messages

Every commit **must** follow the Conventional Commits format or it will be **rejected** by the git hook:

```
<type>(<scope>): <short description>

[optional body — explain the why, not the what]

[optional footer — BREAKING CHANGE: describe what breaks]
```

**Allowed scopes** (maps to sub-projects):

| Scope | Use for |
|---|---|
| `mobile` | React Native / Expo app changes |
| `backend` | FastAPI, models, database, API routes |
| `frontend` | Admin dashboard (React + Vite) |
| `ai` | AI agents (Google ADK) |
| `root` | Monorepo-level config, tooling |
| `ci` | GitHub Actions workflows |
| `deps` | Dependency updates across projects |

**Allowed types and what they mean:**

| Type | Semver impact | When to use |
|---|---|---|
| `feat` | Minor bump | A new feature visible to users or API consumers |
| `fix` | Patch bump | A bug fix |
| `perf` | Patch bump | A performance improvement |
| `refactor` | No bump | Code restructuring with no behaviour change |
| `docs` | No bump | Documentation only |
| `test` | No bump | Adding or fixing tests |
| `chore` | No bump | Build scripts, config, tooling |
| `ci` | No bump | CI/CD pipeline changes |
| `build` | No bump | Build system changes |
| `revert` | Patch bump | Reverting a previous commit |

**Breaking changes** (major bump) — append `!` after the scope or add a `BREAKING CHANGE:` footer:

```
feat(backend)!: redesign inventory API response shape

BREAKING CHANGE: all /inventory endpoints now return items as a flat array instead of nested object
```

**Good examples:**

```bash
feat(mobile): add barcode scanner to pantry inventory screen
fix(backend): correct JWT token expiry calculation
perf(mobile): lazy-load recipe images with expo-image
refactor(backend): extract auth logic into core/security.py
chore(deps): bump expo from 54.0.33 to 54.1.0
ci(root): add backend lint step to PR workflow
docs(ai): document recipe generator agent inputs and outputs
feat(backend)!: redesign inventory API  # triggers major bump
```

**Bad examples (will be rejected):**

```bash
fixed stuff                    # no type, no scope
Update README                  # no type, no scope
feat: add login                # missing scope
feat(payments): add stripe     # "payments" is not an allowed scope
Feat(mobile): Add Login Screen # capitalised type and subject
```

---

### How to Create a Release

Releases are run manually when you are ready to publish a version. They bump the version number, regenerate the `RELEASE.md` changelog, commit the changes, and create a git tag.

#### Mobile (React Native / Expo)

```bash
# From the repo root:
npm run release:mobile:patch   # 1.0.2 → 1.0.3  (bug fixes only)
npm run release:mobile:minor   # 1.0.2 → 1.1.0  (new features)
npm run release:mobile:major   # 1.0.2 → 2.0.0  (breaking changes)

# Or from inside mobile/:
cd mobile
npm run release:patch
npm run release:minor
npm run release:major
```

What happens automatically:
1. `standard-version` reads all commits since the last `mobile-v*` tag
2. Bumps the version in `mobile/package.json`
3. Bumps the version in `mobile/app.json` (`expo.version`) — Expo OTA and store builds read this
4. Writes `mobile/RELEASE.md` with Features / Bug Fixes / Performance sections
5. Creates a git commit (`chore(release): 1.0.3`) and a tag (`mobile-v1.0.3`)

#### Backend / Frontend / AI (Python projects)

```bash
# From the repo root:
npm run release:backend:patch   # 1.1.1 → 1.1.2
npm run release:backend:minor   # 1.1.1 → 1.2.0
npm run release:backend:major   # 1.1.1 → 2.0.0

npm run release:frontend:patch
npm run release:frontend:minor

npm run release:ai:patch
npm run release:ai:minor
```

What happens automatically:
1. `bump-my-version` bumps the version in both `VERSION` (plain text) and `pyproject.toml`
2. `git-cliff` scans the full git history and filters to commits scoped to that project only (e.g. only `fix(backend):...` commits appear in the backend changelog)
3. Writes `<project>/RELEASE.md` with versioned sections grouped by Features / Bug Fixes
4. Creates a release commit (`chore(backend): release v1.1.2`) and a tag (`backend-v1.1.2`)

#### After any release

Push the commits and tags to the remote:

```bash
git push --follow-tags origin main
```

---

### What Goes Into a Release

A release is automatically built from your commit history. Only commits with visible types (`feat`, `fix`, `perf`, `refactor`, `revert`) appear in `RELEASE.md`. Hidden types (`docs`, `chore`, `test`, `ci`, `build`, `style`) are excluded from the changelog.

**Patch release** (`1.0.0 → 1.0.1`) — triggered by `fix`, `perf`, or `revert` commits:
```markdown
## [1.0.1] - 2026-02-28
### Bug Fixes
- Correct JWT token expiry calculation (abc1234)
- Handle null pantry items in meal plan generation (def5678)
```

**Minor release** (`1.0.0 → 1.1.0`) — triggered by any `feat` commit:
```markdown
## [1.1.0] - 2026-02-28
### Features
- Add recipe recommendation endpoint (abc1234)
- Add barcode scanner to pantry inventory screen (def5678)
### Bug Fixes
- Correct inventory item quantity validation (ghi9012)
```

**Major release** (`1.0.0 → 2.0.0`) — triggered by a breaking change (`!` or `BREAKING CHANGE:` footer):
```markdown
## [2.0.0] - 2026-02-28
### Features
- [BREAKING] Redesign inventory API response shape (abc1234)
```

---

### Why This Workflow Matters

- **Consistency** — every commit is machine-readable, making it possible to auto-generate accurate changelogs with zero manual effort
- **Traceability** — each release entry links to the exact commit that introduced the change
- **Independent versioning** — mobile, backend, frontend, and AI can each be at different versions and released on their own cadence without interfering with each other
- **Build version sync** — the mobile `app.json` version is always in sync with `package.json`, so Expo OTA updates and App Store submissions always carry the correct version; the backend exposes its `VERSION` file on the `/health` endpoint
- **Scoped changelogs** — the backend `RELEASE.md` only ever shows backend commits; mobile only shows mobile commits — no noise from unrelated sub-projects
- **Git tags** — every release creates a tag (`mobile-v1.0.3`, `backend-v1.1.2`) making it trivial to diff between releases or roll back

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
