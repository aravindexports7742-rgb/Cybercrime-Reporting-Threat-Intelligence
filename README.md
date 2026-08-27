# Cybercrime & Threat Intelligence Platform

This is a unified application for cybercrime reporting, investigation, threat intelligence, and incident response.

## Setup Instructions

### 1. Database Setup
1. Ensure MySQL is running on your system.
2. Create a database named `cybercrime_db` (or as specified in your `.env` file).
3. Run `python init_db.py` to create the schema and initialize the database.
4. (Optional) Run `python seed_data.py` to populate the database with dummy data for testing.

### 2. Environment Variables
1. Copy `.env.example` to a new file named `.env`.
2. Update the variables in `.env` with your database credentials and a secure JWT secret key.

### 3. Install Dependencies
Run the following command to install the required Python packages:
```bash
pip install -r requirements.txt
```

### 4. Running the Application

**Start the Backend (FastAPI)**
In one terminal, run:
```bash
uvicorn backend.main:app --reload
```

**Start the Frontend (Streamlit)**
In another terminal, run:
```bash
streamlit run frontend/app.py
```

Once both are running, open the URL provided by Streamlit (usually http://localhost:8501) in your browser. All user roles (Victim, Officer, Threat Analyst, Incident Responder, Admin) log in through this single interface.