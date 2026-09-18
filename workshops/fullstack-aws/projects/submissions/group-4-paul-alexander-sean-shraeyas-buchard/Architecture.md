# Architecture — best-banking-app

## 1. Overview

**best-banking-app** is a simple full-stack banking demo app with two components:

- `frontend/` — a React (Vite) single-page app using shadcn/ui components
- `backend/` — a Python API server (FastAPI-style stack, run via `uvicorn`) with a
  layered models → repositories → services structure, backed by SQLite

Core features (inferred from page/route names): user login, account creation,
deposits, withdrawals, transfers between accounts, transaction lookup, and a
settings page.

## 2. High-Level Architecture

```
┌──────────────────────────┐        HTTP (REST, via src/api.js)      ┌──────────────────────────┐
│        frontend/          │ ───────────────────────────────────────▶ │         backend/          │
│  React 18 + Vite          │                                          │  Python + uvicorn         │
│  shadcn/ui components     │ ◀─────────────────────────────────────── │  app.py (entry/routes)    │
└──────────────────────────┘                                          └────────────┬─────────────┘
                                                                                      │
                                                                          services/  │  (business logic)
                                                                                      ▼
                                                                          repositories/ (data access)
                                                                                      │
                                                                                      ▼
                                                                          ┌──────────────────────┐
                                                                          │   banking.db (SQLite) │
                                                                          └──────────────────────┘
```

## 3. Backend (`backend/`)

| Aspect | Details |
|---|---|
| Language / runtime | Python 3.14 |
| Package manager | `uv` (`pyproject.toml`, `uv.lock`) |
| Web server | `uvicorn` (present in `.venv/Scripts`) — indicates a FastAPI/Starlette-style ASGI app |
| Auth | `auth.py`, password hashing via `argon2-cffi` |
| Validation / schemas | Pydantic-style `models/schemas.py` (`annotated_types`, `anyio` present as transitive deps) |
| Data store | SQLite (`backend/banking.db`) via `db.py` |
| Seeding | `seed.py` populates initial data |
| Tests | `test.py` (single top-level test file — no dedicated test directory yet) |

**Layered structure:**

```
backend/
├── app.py                          # entry point / route definitions
├── auth.py                         # authentication (argon2 password hashing)
├── db.py                           # database connection/setup
├── banking.db                      # SQLite database file
├── seed.py                         # seed/demo data
├── test.py                         # tests
├── models/
│   ├── user_entity.py
│   ├── account_entity.py
│   ├── transaction_entity.py
│   └── schemas.py                  # request/response (Pydantic) schemas
├── repositories/
│   ├── user_repository.py
│   ├── account_repository.py
│   └── transaction_repository.py
├── services/
│   └── transaction_service.py      # business logic for transactions
├── pyproject.toml
└── uv.lock
```

This is a classic **3-layer backend pattern**:
- **Entities** (`models/`) define the shape of Users, Accounts, and Transactions.
- **Repositories** (`repositories/`) isolate direct database access per entity.
- **Services** (`services/`) hold business rules — currently only
  `transaction_service.py` exists, so transfer/deposit/withdraw logic likely
  lives there; user and account logic may still sit directly in `app.py`.

> Note: the backend's virtual environment also has a MySQL connector package
> installed (`_mysql_connector...pyd`), but the actual data file present is
> SQLite (`banking.db`). This may be a leftover/unused dependency, or the app
> may support swapping databases — worth confirming in `db.py`.

A `backend/.env` and `.env.example` exist, so configuration (likely DB path,
secret keys for auth) is handled via environment variables.

## 4. Frontend (`frontend/`)

| Aspect | Details |
|---|---|
| Framework | React (JSX) |
| Build tool | Vite |
| UI components | shadcn/ui (`components.json`, `src/components/ui/*`) |
| Linting | oxlint (`.oxlintrc.json`) |
| API layer | `src/api.js` — single client module for backend calls |

**Structure:**

```
frontend/
├── index.html
├── vite.config.js
├── components.json                 # shadcn/ui config
├── package.json / package-lock.json
├── jsconfig.json
├── public/
│   ├── favicon.svg
│   └── icons.svg
└── src/
    ├── main.jsx                    # app entry
    ├── App.jsx / App.css
    ├── api.js                      # backend API client
    ├── currentUser.js              # current-user/session state
    ├── layouts/
    │   └── AppLayout.jsx
    ├── pages/
    │   ├── Welcome.jsx
    │   ├── Login.jsx
    │   ├── Dashboard.jsx
    │   ├── CreateAccount.jsx
    │   ├── NewAccount.jsx
    │   ├── Deposit.jsx
    │   ├── Withdraw.jsx
    │   ├── Transfer.jsx
    │   ├── TransactionLookup.jsx
    │   └── Settings.jsx
    ├── components/
    │   ├── AccountCard.jsx
    │   ├── AppSidebar.jsx
    │   ├── UserCard.jsx
    │   └── ui/                     # shadcn primitives: badge, button, card,
    │                                # input, select, separator, sheet,
    │                                # sidebar, skeleton, table, tooltip
    ├── hooks/
    │   └── use-mobile.js
    ├── lib/
    │   └── utils.js
    └── assets/
        ├── hero.png, react.svg, vite.svg
```

**Routing / flow (inferred from page names):**
`Welcome` → `Login` / `CreateAccount` → `Dashboard` → `Deposit` / `Withdraw` /
`Transfer` / `NewAccount` / `TransactionLookup` / `Settings`. `AppLayout.jsx`
+ `AppSidebar.jsx` provide the shared shell for authenticated pages.

## 5. Data Model (inferred)

Based on the three entity files, the core domain is:

- **User** (`user_entity.py`) — account holder / login identity
- **Account** (`account_entity.py`) — a bank account belonging to a user, with a
  balance
- **Transaction** (`transaction_entity.py`) — a deposit, withdrawal, or transfer
  affecting one or more accounts

Exact fields aren't visible from the file tree alone — pull `models/*.py` and
`models/schemas.py` to document the real schema and relationships.

## 6. Cross-Cutting Concerns

- **Authentication**: `auth.py` + `argon2-cffi` suggests password-based login
  with securely hashed credentials. No dedicated `middleware.py` or token file
  is visible, so it's unclear yet whether sessions or JWTs are used — check
  `auth.py` and `app.py` for the mechanism.
- **Security**: no rate limiting, CORS config, or audit logging visible from
  file names alone — worth checking `app.py` directly, especially since this
  is a banking app.
- **Testing**: only one `test.py` at the backend root; no frontend test setup
  visible (no `*.test.jsx` files or test runner config).
- **CI/CD**: no `.github/workflows/` present — no automated pipeline yet.
- **Environment config**: `backend/.env` + `.env.example` present; no
  equivalent `.env.example` visible for the frontend.

## 7. Repository Layout (top level)

```
best-banking-app/
├── backend/       # Python/FastAPI-style API, SQLite DB, layered architecture
├── frontend/      # React + Vite SPA, shadcn/ui
├── .gitignore
└── README.md      # currently a placeholder, no project description
```

## 8. Gaps / Suggested Next Steps

- Add a real project description and setup instructions to the root `README.md`.
- Confirm whether the MySQL connector dependency is intentional or leftover.
- Document the actual auth mechanism (session vs JWT) once `auth.py` is reviewed.
- Add a `.env.example` for the frontend if it needs any runtime config (e.g.
  API base URL).
- Consider adding CI (lint + backend tests) given `test.py` and `oxlint` are
  already present but not wired into automation.
