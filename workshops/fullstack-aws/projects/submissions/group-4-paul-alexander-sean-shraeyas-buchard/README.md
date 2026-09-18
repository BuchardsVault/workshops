# CHAD Banking

A modern, full-stack digital banking application built with the **FARM stack** (FastAPI, React, MongoDB, and Tailwind CSS). This platform provides secure, real-time banking operations including account management, deposits, withdrawals, and instant fund transfers

🌐 **Live Application:** [https://9asif7ntt8.execute-api.us-east-1.amazonaws.com/](https://9asif7ntt8.execute-api.us-east-1.amazonaws.com/)

---

## 🚀 Tech Stack

### Frontend & UI
* **Core Framework:** React 18, Vite
* **Styling & Components:** Tailwind CSS, shadcn/ui components
* **Navigation & Icons:** Lucide React, React Router

### Backend & API
* **Core Framework:** FastAPI (Python 3.11+), Uvicorn
* **Data Validation & Persistence:** Pydantic models, PyMongo
* **Package Management:** `uv` (Python), `npm` (Node.js)

### Security & Database
* **Database:** MongoDB / MongoDB Atlas
* **Authentication:** JWT (JSON Web Tokens) with BCrypt password hashing

---

## 🛠️ Features

### Frontend User Interface
* **Interactive Dashboard:** Real-time account summaries, financial overviews, and balance tracking.
* **Banking Operations:** Modular pages for instant deposits, withdrawals, and peer-to-peer transfers.
* **Account Management:** Intuitive creation workflow for new checking and savings accounts.
* **Transaction Lookup:** Dynamic search and audit logs for historical user activity.
* **Responsive Sidebar:** Smooth client-side navigation powered by Vite and React.

### Backend Services & API
* **User & Session Management:** Secure registration, authentication, and token verification.
* **Core Banking Logic:** Atomic database updates for monetary transfers and ledger management.
* **Interactive API Docs:** Built-in OpenAPI / Swagger documentation for backend testing.

---

## 💻 Local Development Setup

### Prerequisites

* [Python 3.11+](https://www.python.org/)
* [Node.js (v18+)](https://nodejs.org/) & `npm`
* [MongoDB](https://www.mongodb.com/) (running locally or a MongoDB Atlas connection string)
* [`uv`](https://docs.astral.sh/uv/) package manager
