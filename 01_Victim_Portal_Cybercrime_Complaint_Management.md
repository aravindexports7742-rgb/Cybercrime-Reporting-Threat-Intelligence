# Sector 1: Victim Portal & Cybercrime Complaint Management

**CYBER CRIME & THREAT INTELLIGENCE PLATFORM — Final Year Project**
**Module Owner:** Team Member 1
**Technology Stack:** FastAPI (Backend) · Streamlit (Frontend) · MySQL (Database)

---

## 1. Sector Overview

The **Victim Portal & Cybercrime Complaint Management** sector is the public-facing entry point of the Cyber Crime & Threat Intelligence Platform. It gives members of the public a simple, secure, and traceable channel through which they can report cybercrime incidents and monitor their resolution.

This sector is responsible for the **first stage of the case lifecycle**: identity verification of the victim, structured intake of complaint information, secure evidence collection, and transparent status tracking. Every case handled elsewhere on the platform — investigation (Sector 2), threat correlation (Sector 3), and incident response (Sector 4) — originates from a complaint created here.

Core capabilities delivered by this sector:

- Secure victim account registration and authentication
- Structured, category-driven cybercrime complaint submission
- Evidence upload and metadata capture
- Automatic generation of a unique case tracking identifier
- Real-time complaint status tracking
- Event-driven victim notifications

---

## 2. Objectives

The sector is designed to achieve the following objectives:

1. **Simplify cybercrime reporting** by replacing disconnected, manual reporting methods with a single structured digital workflow.
2. **Centralize complaint data** in the shared MySQL database so it is immediately available to authorized investigating officers.
3. **Guarantee traceability** by issuing every complaint a unique, human-readable tracking ID at the moment of submission.
4. **Protect victim data and evidence** through authentication, hashing, and access-controlled storage.
5. **Keep victims informed** through automated status updates and notifications at each major case milestone.
6. **Provide a foundation for downstream sectors**, ensuring complaint and evidence data is clean, validated, and consistently structured before it reaches investigation and analysis.

---

## 3. Member Responsibility

Team Member 1 owns the full vertical slice of this sector, including:

- Design and implementation of the victim-facing Streamlit interface
- Design and implementation of the FastAPI endpoints listed in Section 8
- Ownership of the database tables listed in Section 9 (`users` is shared with Sector 4's RBAC layer)
- Enforcement of authentication and input validation on all victim-originated data
- Coordination with Sector 2 to ensure submitted complaints are correctly handed off for investigation
- Coordination with Sector 3 to ensure any indicators supplied by victims (suspect URLs, emails, phone numbers) are structured for correlation

---

## 4. Functional Modules

### 4.1 Complaint Categories

Victims may report the following classes of cybercrime:

| Category | Examples |
|---|---|
| Financial Fraud | Online financial fraud, UPI/payment fraud, unauthorized transactions |
| Identity & Account Crime | Phishing, hacking, account compromise, identity theft |
| Harassment & Abuse | Cyber harassment, social media abuse |
| Deception | Fake websites, online scams |
| Other | Any other cyber-related incident not covered above |

### 4.2 User Registration & Login

Victims create an account using their full name, email address, phone number, and password. Authentication is handled entirely through the FastAPI backend, and passwords are **never stored in plain text** — they are hashed (e.g., using `bcrypt`/`passlib`) before being persisted in MySQL. Login issues a token (JWT) used to authorize all subsequent requests.

### 4.3 Complaint Submission

The complaint form captures:

- Complaint title
- Cybercrime category
- Date of incident
- Detailed incident description
- Financial loss amount (if applicable)
- Suspected website/URL
- Suspected phone number
- Suspected email address
- Transaction details (if applicable)
- Any additional supporting information

The Streamlit frontend collects and validates this data client-side before submitting it as JSON to the FastAPI backend, which performs authoritative server-side validation using Pydantic schemas.

### 4.4 Evidence Upload

Victims can attach supporting evidence, including screenshots, images, documents, transaction receipts, email records, chat logs, and URLs. Each upload is validated for file type and size, and access is restricted to the victim and authorized officers only.

### 4.5 Tracking ID Generation

On successful submission, the backend generates a unique, sequential, human-readable tracking ID in the format:

```text
CYB-YYYY-NNNNNN
Example: CYB-2026-000125
```

This ID allows both the victim and investigating officers to reference the case unambiguously, independent of the victim's personal details.

### 4.6 Complaint Status Tracking

Every complaint carries a status that reflects its position in the overall case lifecycle:

```text
Submitted → Under Review → Assigned → Investigation → Action Taken → Resolved → Closed
```

The victim dashboard always reflects the current authoritative status as recorded by Sector 2.

### 4.7 Notifications

The system raises a notification for every significant case event, including:

- Complaint successfully submitted
- Complaint accepted for review
- Complaint assigned for investigation
- Case status changed
- Additional information requested
- Case resolved or closed

---

## 5. Workflow

### 5.1 Complaint Submission Workflow

```text
Victim Login
     │
     ▼
Create New Complaint
     │
     ▼
Enter Incident Details
     │
     ▼
Upload Supporting Evidence
     │
     ▼
Submit Complaint
     │
     ▼
FastAPI Validates Data (Pydantic)
     │
     ▼
Persist Complaint in MySQL
     │
     ▼
Generate Unique Tracking ID
     │
     ▼
Display Confirmation to Victim
     │
     ▼
Notify Victim (Submission Confirmed)
```

### 5.2 Complaint Lifecycle

```text
Submitted
    │
    ▼
Under Review
    │
    ▼
Assigned  ───────────► (Handed to Sector 2: Officer Portal)
    │
    ▼
Investigation
    │
    ▼
Action Taken
    │
    ▼
Resolved
    │
    ▼
Closed
```

---

## 6. Dashboard Design

The Streamlit victim-facing interface is organized as follows:

```text
Victim Dashboard
├── Home                (summary of open/closed cases)
├── New Complaint        (structured submission form)
├── My Complaints        (list view with filters)
├── Track Case           (status timeline for a selected case)
├── Upload Evidence      (attach files to an existing complaint)
├── Notifications        (event feed)
└── Profile              (account details, password management)
```

Design principles: the interface must remain simple and non-technical, since victims may have limited digital literacy; status information should be presented visually (progress indicator) rather than as raw database values.

---

## 7. API Design

All endpoints are served by FastAPI and authenticated using JWT bearer tokens, except registration and login.

```text
POST   /auth/register              Register a new victim account
POST   /auth/login                 Authenticate and issue a JWT

POST   /complaints                 Submit a new complaint
GET    /complaints                 List complaints for the authenticated victim
GET    /complaints/{case_id}       Retrieve full complaint detail
PUT    /complaints/{case_id}       Update a complaint (where permitted)

POST   /evidence                   Upload evidence linked to a complaint
GET    /evidence/{case_id}         List evidence for a complaint

GET    /notifications              Retrieve notifications for the authenticated victim
```

Request and response payloads are validated using Pydantic schemas. These are the agreed logical endpoints; final route naming will be confirmed jointly with all four sector owners to maintain a single consistent API surface.

---

## 8. Database Responsibility

This sector owns the following tables in the shared MySQL database (full schema in the companion database design document):

| Table | Purpose |
|---|---|
| `users` | Shared identity table (co-owned with Sector 4 RBAC) |
| `victim_profiles` | Victim-specific profile attributes linked to `users` |
| `complaints` | Core complaint records, including category and status |
| `complaint_categories` | Lookup table of supported complaint types |
| `evidence` | Evidence metadata linked to complaints |
| `notifications` | Event notifications delivered to victims |

Relationships connect a victim (`users` → `victim_profiles`) to their `complaints`, each complaint to its `evidence` and `notifications`, and each complaint to a `complaint_categories` entry.

---

## 9. Security Considerations

- **Authentication:** All victim actions require a valid session/JWT; registration and login are the only anonymous endpoints.
- **Password Security:** Passwords are hashed (never stored or logged in plaintext) using an industry-standard algorithm.
- **Authorization / RBAC:** Victims may only access their own complaints, evidence, and notifications — never another victim's records.
- **Input Validation:** All form and file inputs are validated server-side via Pydantic and explicit file-type/size checks.
- **Evidence Protection:** Uploaded files are stored with access controls that prevent direct unauthenticated retrieval.
- **Secure Communication:** API traffic should be served over HTTPS in any deployed environment.
- **Audit Logging:** Key victim actions (registration, submission, evidence upload) are logged to the shared `audit_logs` table owned by Sector 4.

---

## 10. Integration with Other Sectors

```text
Sector 1 (Victim Portal)
        │  complaint + evidence + tracking ID
        ▼
Sector 2 (Officer Investigation Portal)
        │  indicators identified during investigation
        ▼
Sector 3 (Threat Intelligence, Monitoring & Analysis)
        │  significant findings
        ▼
Sector 4 (Incident Response, Security Operations & Administrative Control)
```

- **Sector 2** consumes newly submitted complaints directly as the starting point of every investigation, and writes status updates back to the `complaints` table, which Sector 1's dashboard reflects in real time.
- **Sector 3** may reuse victim-supplied indicators (suspect URL, email, phone number) as inputs for correlation against known threat intelligence.
- **Sector 4** consumes authentication events and complaint/evidence actions for the shared audit trail and RBAC enforcement.

---

## 11. Final Deliverables

1. Streamlit victim portal (registration, login, complaint submission, evidence upload, tracking, notifications, profile).
2. FastAPI backend implementing all endpoints listed in Section 7, with Pydantic validation and JWT authentication.
3. MySQL tables listed in Section 8, integrated into the shared project database.
4. Documented, testable complaint submission and tracking workflow.
5. Security controls: password hashing, input validation, evidence access control, and audit-log integration.
6. Sector documentation (this file) suitable for inclusion in the final project report.
