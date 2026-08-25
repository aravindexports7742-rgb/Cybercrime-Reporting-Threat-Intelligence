# 00 — Build Instructions
## CYBER CRIME & THREAT INTELLIGENCE PLATFORM — Final Year Project

**Read this file first, before the 5 documentation files below.** It tells you exactly how to build the system; the other files tell you what to build.

Attached / accompanying files:
- `01_Victim_Portal_Cybercrime_Complaint_Management.md`
- `02_Officer_Cybercrime_Response_Investigation_Portal.md`
- `03_Threat_Intelligence_Monitoring_Analysis.md`
- `04_Incident_Response_Security_Operations_Administrative_Control.md`
- `05_Database_Design_Complete.md`

---

## 1. This is ONE unified application — not four separate apps

Build:

- **ONE FastAPI backend** — a single `main.py`, a single running server, a single port.
- **ONE Streamlit frontend** — a single `app.py`, a single running server, a single port.
- **ONE shared MySQL database** — a single schema, created from the SQL in `05_Database_Design_Complete.md` Section 4. Do not create four databases.

The "Member 1 / Member 2 / Member 3 / Member 4" labels in the docs describe **who owns which code module for authorship purposes only** — they do not mean four separate applications. All four sectors must run as one connected system sharing one login, one RBAC layer, and one database.

---

## 2. Required folder structure

Follow this exactly (mirrors Section 11 of `05_Database_Design_Complete.md`):

```text
cyber-crime-threat-intel-platform/
├── backend/
│   ├── main.py                      # mounts all 4 sector routers into ONE app
│   ├── database/
│   │   ├── connection.py            # ONE SQLAlchemy engine / MySQL connection
│   │   └── init_schema.sql          # copy verbatim from 05, Section 4
│   ├── models/
│   │   ├── shared_models.py         # users, roles, permissions, role_permissions
│   │   ├── sector1_victim.py
│   │   ├── sector2_officer.py
│   │   ├── sector3_threat.py
│   │   └── sector4_admin.py
│   ├── schemas/
│   │   ├── sector1_victim.py
│   │   ├── sector2_officer.py
│   │   ├── sector3_threat.py
│   │   └── sector4_admin.py
│   ├── routers/
│   │   ├── sector1_victim.py
│   │   ├── sector2_officer.py
│   │   ├── sector3_threat.py
│   │   └── sector4_admin.py
│   ├── services/                    # correlation engine, playbook runner, notification logic, etc.
│   └── security/
│       ├── auth.py                  # JWT issue/verify — shared by all sectors
│       ├── rbac.py                  # role/permission checks — shared by all sectors
│       └── hashing.py               # password hashing (bcrypt/passlib)
│
├── frontend/
│   ├── app.py                       # ONE entry point; handles login, routes by role
│   ├── pages/
│   │   ├── victim/
│   │   ├── officer/
│   │   ├── threat_intel/
│   │   └── admin/
│   ├── components/                  # shared UI widgets (status badges, tables, forms)
│   └── services/                    # API client wrappers calling the ONE backend
│
├── docs/                            # the 5 documentation files + this one
├── requirements.txt
├── .env.example
└── README.md
```

---

## 3. Build order (build incrementally — do not attempt everything in one pass)

Work through these stages **one at a time**, and pause for review after each:

1. **Foundation:** Create the MySQL database from `init_schema.sql`. Build `database/connection.py`, `security/auth.py`, `security/rbac.py`, `security/hashing.py`, and the `shared_models.py` (users/roles/permissions). Implement `/auth/register` and `/auth/login`. Confirm login works and issues a JWT carrying the user's role.
2. **Sector 1 — Victim Portal:** Implement `sector1_victim.py` models/schemas/routers per file `01`, Sections 7–9. Implement the corresponding Streamlit `pages/victim/` per Section 6. Confirm a victim can register, log in, submit a complaint, get a tracking ID, upload evidence, and see status.
3. **Sector 2 — Officer Portal:** Implement `sector2_officer.py` per file `02`. Confirm officers can see complaints from Sector 1 as cases, manage evidence/chain of custody/suspects, and that status updates flow back to the victim's dashboard.
4. **Sector 3 — Threat Intelligence:** Implement `sector3_threat.py` per file `03`. Confirm indicators from Sector 2's cases can be searched/correlated against IOCs, and campaign detection works across multiple complaints.
5. **Sector 4 — Incident Response & Admin:** Implement `sector4_admin.py` per file `04`. Confirm incidents can be created (including from escalated Sector 2/3 findings), playbooks run, and the admin dashboard shows users, roles, audit logs, login history, and system health.
6. **Cross-sector wiring pass:** Verify every integration point listed in each file's Section 10 ("Integration with Other Sectors") is actually connected end-to-end, not just present as unused code.

---

## 4. Non-negotiable requirements

- Use the **exact SQL schema** from `05_Database_Design_Complete.md` Section 4 — do not redesign tables, rename columns, or drop fields.
- Implement **all API endpoints** listed in Section 7 of each sector file.
- Implement **all dashboard sections** listed in Section 6 of each sector file.
- Enforce **RBAC** on every protected endpoint using the shared `users` → `roles` → `permissions` chain — a Victim must never be able to reach Officer/Analyst/Admin endpoints, and vice versa.
- Passwords must be hashed (never stored or logged in plaintext).
- Write to `audit_logs` for significant actions (submission, case update, evidence access, role change, login).
- Do **not** invent features, tables, or endpoints not described in the 5 documentation files.
- Do **not** split this into multiple databases or multiple backend/frontend apps.

---

## 5. Deliverables expected back

1. Full source code matching the folder structure in Section 2.
2. `requirements.txt` listing all Python dependencies.
3. `.env.example` with placeholder DB credentials and JWT secret.
4. Simple run instructions (or a `docker-compose.yml`) to start MySQL + backend + frontend together.
5. Confirmation, stage by stage, of which build-order step (Section 3) has been completed.

---

## 6. How to run it (target end state)

```text
1. MySQL running as a background service (started once)
2. Backend:  uvicorn backend.main:app --reload
3. Frontend: streamlit run frontend/app.py
```

One login screen, one URL, role-based views after authentication — a Victim, Officer, Threat Analyst, Incident Responder, and Administrator all use the same running application.
