# 💸 RupeeTracker — Personal Finance Expense Tracker & Analytics

A premium, full-stack personal finance web application built with **Streamlit**, **SQLAlchemy**, **Plotly**, and **JWT authentication**. Track your income and expenses, set monthly budgets, visualize spending patterns, forecast future costs, and manage custom categories — all from a beautiful glassmorphic dashboard with Dark & Light mode support.

---

## 📋 Table of Contents

- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Environment Variables](#-environment-variables)
- [Running the App](#-running-the-app)
- [Demo User & Sample Data](#-demo-user--sample-data)
- [Pages & Features](#-pages--features)
- [Authentication Flow](#-authentication-flow)
- [Budget Alert System](#-budget-alert-system)
- [Forecasting Engine](#-forecasting-engine)
- [Default Categories](#-default-categories)
- [Theme System](#-theme-system)
- [Running Tests](#-running-tests)

---

## 🔄 How It Works

RupeeTracker follows a simple, intuitive workflow:

```
Register / Login
       ↓
 Log Transactions (Income & Expenses)
       ↓
 Categorize Each Entry
       ↓
 Set Monthly Budget Limits
       ↓
 View Analytics & Spending Charts
       ↓
 Get Budget Alerts (Green / Orange / Red)
       ↓
 Forecast Next Month's Expenses
```

1. **Sign up** with your email and password — a secure account is created with JWT-based sessions.
2. **Log transactions** — record every income or expense with a date, amount, category, and optional notes.
3. **Set budgets** — define monthly spending caps (overall or per-category).
4. **Analyze** — interactive Plotly charts show where your money goes, trends over time, and category breakdowns.
5. **Get alerts** — the system automatically evaluates your spending against budget limits and shows color-coded warnings.
6. **Forecast** — a rolling-average engine predicts next month's spending per category based on historical data.

All data is **user-isolated** — each account only sees its own transactions, categories, and budgets.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit (Python) with custom CSS/HTML injection |
| **Database** | SQLite via SQLAlchemy ORM |
| **Charts** | Plotly Express |
| **Authentication** | JWT (PyJWT) with bcrypt password hashing |
| **Email** | SMTP-based notifications (login / logout / password reset) |
| **Styling** | Glassmorphic CSS with Plus Jakarta Sans typography |
| **Testing** | pytest (13 unit tests) |

---

## 📁 Project Structure

```
newProject/
├── .env                        # Environment variables (secrets, SMTP config)
├── .env.example                # Template for .env setup
├── .streamlit/
│   └── config.toml             # Streamlit server configuration
├── app.py                      # Main application (UI, routing, all pages)
├── requirements.txt            # Python dependencies
├── finance_app.db              # SQLite database (auto-created on first run)
├── check_compile.py            # Quick syntax validation script
├── seed_demo_user.py           # Script to populate demo data from CSV archives
│
├── db/                         # Database layer
│   ├── models.py               # SQLAlchemy ORM models (User, Transaction, Category, Budget, PasswordReset)
│   ├── repository.py           # Data access layer (CRUD operations)
│   ├── seed.py                 # Default category definitions & seeding logic
│   └── utils.py                # Database utility helpers
│
├── services/                   # Business logic layer
│   ├── analytics.py            # Monthly totals, category breakdowns, daily analysis
│   ├── auth.py                 # JWT token creation, decoding, expiration checks
│   ├── budgets.py              # Budget evaluation engine (green/orange/red logic)
│   ├── emailer.py              # SMTP email sender (login, logout, password reset emails)
│   ├── forecast.py             # Spending prediction engine (rolling averages per category)
│   ├── logger.py               # Centralized logging configuration
│   ├── passwords.py            # bcrypt password hashing & verification
│   └── user_service.py         # User registration & authentication helpers
│
├── tests/                      # Unit test suite
│   ├── test_analytics.py       # Analytics service tests
│   ├── test_budgets_and_forecast.py  # Budget & forecast integration tests
│   ├── test_category_forecast.py     # Category-level forecast tests
│   ├── test_emailer.py         # Email service tests (mocked SMTP)
│   ├── test_repository.py      # Database repository CRUD tests
│   └── test_transactions_and_categories.py  # Transaction & category tests
│
├── archive (1)/                # Sample CSV data for demo seeding
│   ├── Income_clean.csv        # ~200 income records
│   └── Expenses_clean.csv      # ~1000 expense records
│
└── logs/                       # Application log files (auto-created)
```

---

## 🚀 Setup & Installation

### Prerequisites

- **Python 3.10+** installed on your system
- **pip** package manager

### Step-by-Step

**1. Clone or download the project**

```bash
cd newProject
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

**3. Activate the virtual environment**

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Configure environment variables**

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` with your settings (see [Environment Variables](#-environment-variables) below).

**6. Run the application**

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

---

## 🔐 Environment Variables

Create a `.env` file in the project root with the following keys:

| Variable | Description | Example |
|---|---|---|
| `JWT_SECRET` | Secret key for signing JWT tokens | `my_super_secret_key_123` |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `JWT_EXP_SECONDS` | Token expiration time in seconds | `3600` |
| `SMTP_HOST` | SMTP mail server host | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port | `587` |
| `SMTP_USERNAME` | SMTP login username | `your-email@gmail.com` |
| `SMTP_PASSWORD` | SMTP login password or app password | `your-app-password` |
| `EMAIL_FROM` | Sender email address | `noreply@rupeetracker.com` |
| `BUDGET_NEAR_THRESHOLD` | Warning threshold ratio (0.0 – 1.0) | `0.8` |
| `DATABASE_URL` | SQLAlchemy database connection string | `sqlite:///finance_app.db` |
| `DEFAULT_THEME` | Default UI theme on first load | `dark` |

> **Note:** If email credentials are not configured, the app still works — email sending will fail silently and log a warning.

---

## ▶ Running the App

```bash
# Activate virtual environment first
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# Start the Streamlit server
streamlit run app.py
```

The app launches at `http://localhost:8501`. You can:
- **Create a new account** from the login screen
- **Or use the demo user** (see below)

---

## 👤 Demo User & Sample Data

A ready-made demo account can be seeded with ~1,200 real transactions from the CSV archive files.

### Option A: Seed from the Sidebar (Recommended)

1. Log in with **any account**
2. Open the **sidebar** (click the hamburger `☰` icon top-left)
3. Click the **🔄 Reset & Seed Demo Data** button
4. The demo user is created with credentials:
   - **Email:** `demo@rupeetracker.com`
   - **Password:** `demouser123`

### Option B: Seed from the Command Line

```bash
python seed_demo_user.py
```

This reads `archive (1)/Income_clean.csv` and `archive (1)/Expenses_clean.csv`, creates the demo user, and inserts all transactions into the database.

---

## 📄 Pages & Features

After logging in, use the **sidebar navigation** to switch between pages. Here's what each page shows:

---

### 🏠 1. Home Dashboard

The landing page after login. Gives you a complete snapshot of your financial health.

| Section | What It Shows |
|---|---|
| **Greeting Banner** | Dynamic greeting based on time of day ("Good Morning / Afternoon / Evening") with a rotating daily finance tip |
| **Cash Flow Health Badge** | Real-time ratio of spending vs. income — shows "High Surplus", "Balanced", or "Deficit Danger" with color coding |
| **Finance Cards** | Three glassmorphic cards: Total Income (green), Total Expenses (red), Net Savings (green/red) |
| **Metrics Row** | Average monthly spending, biggest spending category, and a quick "Log a New Transaction" button |
| **Budget Alerts** | Global banner notifications — green (safe), orange (approaching limit), red (over budget) |
| **Money Passbook** | Full transaction history table with live search, category filter, and income/expense type filter pills |
| **Row Actions** | Select any row to edit its details or permanently delete it |

---

### ➕ 2. Add Money Entry

A form to log a single income or expense transaction.

| Field | Description |
|---|---|
| **Type** | Select "income" or "expense" |
| **Amount** | Transaction amount in Rupees (₹) |
| **Date** | Date of the transaction (defaults to today) |
| **Category** | Pick from your existing categories or create a new custom one on-the-fly |
| **Notes** | Optional remarks — shop name, item details, etc. |

On submission, the entry is saved to the database and immediately reflected in the Dashboard and Analytics pages.

---

### 📊 3. Spending Analytics

Interactive charts that visualize exactly where your money goes.

| Chart | What It Shows |
|---|---|
| **Income vs Expenses Trend** | A Plotly line chart comparing income and expense totals over the past 3–24 months (adjustable via slider) |
| **Category Spending Breakdown** | A bar chart showing top 10 expense categories for any selected month |

All charts are theme-aware — they automatically switch between `plotly_dark` and `plotly_white` templates based on the active theme.

---

### 🛡 4. Monthly Budgets

Set spending limits and monitor your budget safety.

| Section | What It Shows |
|---|---|
| **Budget Form** | Set a maximum spending cap for a specific month — either as a total monthly budget or per individual category |
| **Budget Safety Cards** | Color-coded glassmorphic cards showing each budget's status with a progress bar |

**Alert colors:**
- 🟢 **Green** — Spending is well within limits (under 80%)
- 🟠 **Orange** — Approaching the limit (80%–99% of budget consumed)
- 🔴 **Red** — Budget exceeded (100%+ spent)

The 80% threshold is configurable via the `BUDGET_NEAR_THRESHOLD` environment variable.

---

### 🔮 5. Future Forecast

A data-driven prediction tool that estimates next month's expenses by category.

| Section | What It Shows |
|---|---|
| **Lookback Slider** | Choose how many months of historical data to use for the prediction (1–12 months) |
| **Comparison Bar Chart** | Side-by-side grouped bars comparing current month's spending vs. predicted next month — per category |
| **Forecast Ledger Table** | A data table with exact predicted values for each category |
| **Total Prediction Card** | Aggregated estimate of total expenses expected next month |

The prediction engine uses a **rolling historical average** — it calculates the mean expense per category over the lookback window. At least 2 months of data are required.

---

### 🏷 6. Manage Categories

Create, rename, or delete your custom spending categories.

| Section | What It Shows |
|---|---|
| **Active Categories List** | All categories with their internal ID codes |
| **Add a Category** | Text input to create a new category |
| **Rename Category** | Select an existing category and give it a new name |
| **Delete Category** | Remove a category from your account |

When a new user registers, **22 default categories** are automatically created (Salary, Groceries, Transport, Healthcare, etc.). See [Default Categories](#-default-categories).

---

## 🔑 Authentication Flow

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Login Form    │────▶│ Verify Password  │────▶│  Issue JWT      │
│ (email + pass)  │     │ (bcrypt check)   │     │  (session state)│
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │ Send Login Email│
                                                 │ (SMTP)          │
                                                 └─────────────────┘
```

- **Registration**: Email + password → password hashed with bcrypt → stored in database → JWT issued → default categories seeded
- **Login**: Email + password → bcrypt verification → JWT issued → login notification email sent
- **Logout**: JWT cleared from session → logout notification email sent
- **Password Reset**: Email-based reset code (6-digit) with 20-minute expiry → new password set via code verification
- **Session Management**: JWT stored in `st.session_state` with configurable expiration

---

## 🚦 Budget Alert System

The budget evaluator runs on every page load and checks all active budgets for the current month:

```python
ratio = spent / limit

if ratio >= 1.0:    → 🔴 RED    — "Critical Budget Alert! You have breached your limit."
elif ratio >= 0.8:  → 🟠 ORANGE — "Warning! You have consumed X% of your budget."
else:               → 🟢 GREEN  — "Budget Safe! Spending is well within limits."
```

Alerts are shown as banner notifications at the top of every page and as color-coded cards on the Monthly Budgets page.

---

## 📈 Forecasting Engine

The forecast service (`services/forecast.py`) provides two prediction functions:

| Function | What It Does |
|---|---|
| `forecast_next_month()` | Predicts total expenses for next month using a rolling average |
| `forecast_categories_next_month()` | Predicts expenses per individual category using rolling averages over a configurable lookback window |

**Algorithm**: For each category, the engine collects monthly expense totals over the lookback period and returns the arithmetic mean as the predicted value.

---

## 🏷 Default Categories

Every new user automatically receives these 22 categories on registration:

| Income | Everyday | Lifestyle | Financial |
|---|---|---|---|
| Salary / Income | Groceries | Entertainment | Savings |
| Business / Side Hustle | Dining | Personal Care | Investment |
| | Transport | Gifts & Donations | Insurance |
| | Bills | Family & Kids | Loan given |
| | Housing | Shopping | Debt return / Borrowed money |
| | Utilities | Travel | |
| | Healthcare | Subscriptions | |
| | Education | Other | |

Users can also create custom categories at any time from the Manage Categories page or inline when adding a transaction.

---

## 🎨 Theme System

RupeeTracker supports **Dark Mode** and **Light Mode**, switchable from the sidebar.

| Property | Dark Mode | Light Mode |
|---|---|---|
| Background | `#07090e` (deep navy) | `#f0f2f5` (soft gray) |
| Card Background | `rgba(13, 18, 30, 0.75)` | `rgba(255, 255, 255, 0.92)` |
| Text Color | `#f8fafc` (off-white) | `#0f172a` (dark slate) |
| Accent Color | `#6366f1` (indigo) | `#4f46e5` (deep indigo) |
| Charts | `plotly_dark` template | `plotly_white` template |

The theme is applied through:
1. **CSS custom injection** — dynamic `<style>` block with theme variables
2. **Streamlit internal config** — `st._config.set_option()` for canvas-rendered widgets (dataframes, native widgets)
3. **Plotly templates** — charts automatically switch between dark/white templates

---

## 🧪 Running Tests

The project includes **13 unit tests** covering the database layer, analytics, budgets, forecasting, and email services.

```bash
# Activate virtual environment
venv\Scripts\activate

# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run a specific test file
python -m pytest tests/test_repository.py
```

### Test Coverage

| Test File | What It Covers |
|---|---|
| `test_repository.py` | User creation, transaction CRUD, listing & limits |
| `test_transactions_and_categories.py` | Transaction editing, deletion, category upsert & rename |
| `test_analytics.py` | Monthly totals aggregation, category breakdowns |
| `test_budgets_and_forecast.py` | Budget evaluation logic, basic forecast predictions |
| `test_category_forecast.py` | Per-category forecast calculations with multi-month data |
| `test_emailer.py` | SMTP email composition & sending (mocked) |

### Syntax Check

```bash
python check_compile.py
```

Returns `py_compile OK` if the main `app.py` file has no syntax errors.

---

