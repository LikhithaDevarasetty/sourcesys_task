# 📊 Premium SaaS Revenue & Churn Business Intelligence Portal

Welcome to the **SaaS Revenue & Churn Analytics & Prediction Portal**—a state-of-the-art business intelligence (BI) web application designed for executive analytics, customer retention analysis, and AI-powered churn risk simulation. Built using **Streamlit** and styled with a **premium glassmorphism theme**, it offers real-time analytics and predictive models that adapt dynamically to any business data.

---

## 🚀 Key Features

*   **Premium Glassmorphic UI**: Vibrant,Harmonious custom color palettes (teals, violets, and rose accents) featuring micro-animations, transparent card grids, custom loaders, and fully responsive layouts.
*   **Secure Authentication Suite**: Multi-tier login portal with:
    *   Secure **Email & Password** verification backed by salted/hashed passwords (`bcrypt`).
    *   **Google Federated Single Sign-On (SSO)** backed by secure popup triggers (`streamlit-oauth`).
    *   Dynamic **Forgot/Reset Password** flows.
*   **Asynchronous SMTP Notifications**: Real-time email triggers for sign-ins, logouts, and new account welcomes, featuring automated Gmail config corrections.
*   **Executive Sales Dashboard**: Real-time SaaS metric cards (ARR, MRR, ARPU, LTV, Churn Rate), sales trends, regional contributions, category break-down charts, and discount-vs-profitability scatter matrices.
*   **Retention Cohort Matrix**: Dynamic transaction cohort tables computing month-on-month customer retention percentages, survival curves, and lifetime values.
*   **AI Churn Predictor**: Real-time "What-If" churn risk simulator utilizing a highly optimized **Random Forest Classifier** achieving **80.2% accuracy** and **0.846 ROC AUC**. It computes top retention risk factors instantly and renders clear, actionable playbooks.
*   **Dynamic Custom CSV Uploader**: Allows uploading custom SaaS Sales or Customer Churn CSV files. If any required columns are absent, it dynamically:
    1.  Shows a gorgeous, glassmorphic notice banner listing all absent elements.
    2.  Gracefully imputes/fills all missing data (e.g. setting sequential IDs, calculating monthly charges from order values) so that all panels and models compile and run flawlessly without crashing!

---

## 🛠️ Technology Stack & Dependencies

*   **Frontend & Layout**: Streamlit (Python-based reactive web framework)
*   **Styling**: Vanilla CSS (Premium transparent glassmorphism injected globally)
*   **Data Processing**: Pandas, NumPy
*   **Data Visualization**: Plotly Express (Interactive charts & heatmaps)
*   **Machine Learning**: Scikit-Learn (Random Forest, Dummy Classifier, Train-Test Split, Metrics)
*   **Database / Storage**: JSON-based encrypted flat file system (`users_db.json`)
*   **Authentication & Hashing**: Bcrypt, PyJWT, Authlib, Streamlit-OAuth (Google SSO Integration)
*   **Email Engine**: SmtpLib, Jinja2, Email.MIME (Asynchronous threaded email service)

---

## 📂 Project Architecture

```directory
SaaS_analytics/
│
├── app.py                      # Main entrypoint, handles page caching & dynamic imports
├── requirements.txt            # System dependencies
├── README.md                   # Full system documentation
│
├── backend/
│   ├── .env                    # System environmental variables (fallback SMTP, etc.)
│   ├── google_creds.json       # Git-ignored local Google OAuth JSON
│   ├── SaaS-Sales.csv          # Base Sales & transaction history dataset
│   ├── WA_Fn-UseC_-Telco-Customer-Churn.csv  # Base customer churn dataset
│   ├── users_db.json           # Secured user credentials & session records
│   ├── sent_emails_log.txt     # Log file storing sent notifications (Mock mode fallback)
│   │
│   └── utils/
│       ├── auth_db.py          # Secure user registration, validation, and bcrypt hashing
│       ├── data_loader.py      # Load base CSVs, parse custom CSVs, and impute absent elements
│       ├── email_service.py    # Multi-threaded asynchronous SMTP email engine
│       └── ml_model.py         # AI Churn Model (RandomForest, imputation, importances)
│
└── frontend/
    ├── app.py                  # Streamlit Multi-page main dashboard router
    ├── styles.css              # Premium custom glassmorphic styling sheet
    │
    └── components/
        ├── login.py            # Glass-card signup, sign-in, SSO, reset pages
        ├── sales_dashboard.py  # Sales KPI metrics, charts, and custom dataset banners
        ├── retention_cohort.py # Cohort calculations, matrix grids, and survival curves
        └── churn_predictor.py  # What-If risk calculators, contribution bars, playbooks
```

---

## 🔄 Core Workflows & How It Works

### 1. Secure Authentication Flow
*   When a user visits the site, the main Streamlit router checks `st.session_state.logged_in`. If false, it renders the Login portal (`components/login.py`).
*   **Email Sign-in**: The email is verified against `users_db.json` using salted password hashing (`bcrypt.checkpw`).
*   **Google OAuth Sign-in**: Incorporates a premium centered "Continue with Google" button. Clicking triggers a popup validating identity. A JWT id_token is decoded using base64 and matched to load/provision a new workspace instantly.
*   Upon successful login, an asynchronous email notification is dispatched (`send_login_email_async`), and the user is redirected to the main dashboard.

### 2. Custom Dataset Uploading & Imputation
*   Under the workspace sidebar, users can toggle between **System Default Datasets** and **Upload Custom CSV 📂**.
*   When a custom CSV is uploaded, `utils/data_loader.py` validates the schema against required columns:
    *   **Sales Requirement**: `Order Date`, `Sales`, `Quantity`, `Profit`, `Customer ID`, `Segment`, `Category`.
    *   **Churn Requirement**: `Churn`, `gender`, `Contract`, `InternetService`, `PaymentMethod`, `tenure`, `MonthlyCharges`.
*   **If columns are missing**: It collects the list of absent names, displays an informative notice banner inside the active workspace, and automatically executes robust fallbacks (e.g. mapping `Profit` as 15% of Sales, auto-filling `Churn` target as `No`, computing sequence ranges). This ensures all Plotly charts, cohort heatmaps, and ML models continue to execute beautifully.

### 3. Machine Learning Churn Engine
*   **Data Preparation**: Cat-columns are one-hot encoded (`get_dummies`), missing metrics are filled with median templates (`_impute_X`), and `TotalCharges` are log-normalized to prevent bias.
*   **Model Training**: The engine fits a **`RandomForestClassifier`** with `100` estimators and a `max_depth=8`.
*   **Importance Drivers**: It immediately accesses the native `model.feature_importances_` to identify churn drivers, fallback-checking with `permutation_importance` if needed.
*   **What-If Simulation**: Users adjust sliders/selectboxes in the simulator. The values are encoded, imputed with column medians, and fed to `predict_proba()` to display real-time Churn risk percentages alongside playbooks.
*   **Stale Cache Prevention**: To ensure Streamlit Cloud instantly reflects edits and does not serve stale models, the model training is cache-busted using a unique function signature `_version=5` parameter.

### 4. SMTP Email Dispatch Engine
*   The email system operates fully **asynchronously** using python `threading` so that user interactions never freeze during SMTP network negotiations.
*   Supports live **SSL/TLS SMTP negotiations** (`smtp.gmail.com`) as well as a local **Mock Mode** fallback which prints outgoing emails to `backend/sent_emails_log.txt` when internet/credentials are absent.

---

## 🏃 Setup & Installation

### Prerequisiets
Ensure you have Python 3.9+ installed on your system.

### 1. Clone & Enter the Repository
```bash
git clone https://github.com/LikhithaDevarasetty/sourcesys_task.git
cd sourcesys_task/SaaS_analytics
```

### 2. Install System Dependencies
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```

### 3. Environmental Configuration (Optional)
To enable live email notifications, create/edit the `.env` file at `backend/.env`:
```ini
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
EMAIL_FROM=your-email@gmail.com
```

### 4. Run the Streamlit Application
Start the Streamlit portal locally using:
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser to explore the dashboard!

---

## 🤝 Verification & Operational Integrity

All aspects of the platform are continuously verified using unit scripts located in the brain artifacts directory:
*   `test_ml_model.py`: Validates model training, RF feature importances, and inference bounds.
*   `test_import_only.py`: Checks absolute module paths and cross-layer imports.
*   `test_accuracy.py`: Benchmarks classifier models (Random Forest, Gradient Boosting, HistGBC) to guarantee optimal performance.
