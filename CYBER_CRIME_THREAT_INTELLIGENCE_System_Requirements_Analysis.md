# System Requirements Analysis
## Project: CYBER CRIME & THREAT INTELLIGENCE

## 1. Project Overview

**CYBER CRIME & THREAT INTELLIGENCE** is an integrated cybercrime management and threat intelligence platform designed to connect four major sectors:

1. Victim Portal & Cybercrime Complaint Management
2. Officer / Cybercrime Response & Investigation Portal
3. Threat Intelligence, Monitoring & Analysis
4. Incident Response, Security Operations & Administrative Control

The system uses **Python**, **FastAPI**, **Streamlit**, and **MySQL** to provide a centralized platform for complaint management, investigation, threat analysis, incident response, and administrative security.

---

# 2. Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Programming Language | Python | Main application development |
| Backend | FastAPI | REST API, authentication, and business logic |
| Frontend | Streamlit | Web-based user interface and dashboards |
| Database | MySQL | Store users, complaints, evidence, investigations, threats, incidents, and logs |
| API Format | JSON | Communication between frontend and backend |
| Authentication | JWT / Token-based authentication | Secure user authentication |
| Authorization | RBAC | Role-based access control |
| Database Connectivity | SQLAlchemy / MySQL Driver | Connect FastAPI with MySQL |
| Data Validation | Pydantic | Validate API request and response data |
| Version Control | Git/GitHub | Source-code management |

---

# 3. Functional Requirements

Functional requirements describe **what the system must do**.

## Sector 1 — Victim Portal & Complaint Management

### FR-01: User Registration

The system shall allow victims to create an account using required information such as:

- Name
- Email
- Phone number
- Password

### FR-02: User Login

The system shall authenticate registered users before allowing access to protected features.

### FR-03: Submit Cybercrime Complaint

Victims shall be able to submit complaints for incidents such as:

- Online fraud
- Hacking
- Phishing
- Cyber harassment
- Identity theft
- Financial fraud
- Account compromise
- Social-media-related cybercrime

### FR-04: Generate Tracking ID

After successful complaint submission, the system shall generate a unique case/tracking ID.

Example:

`CYB-2026-000125`

### FR-05: Evidence Upload

Victims shall be able to attach supporting evidence such as:

- Images
- Screenshots
- Documents
- Transaction information
- URLs
- Other permitted digital evidence

### FR-06: Complaint Status Tracking

Victims shall be able to view the current status of their complaints.

Example:

```text
Submitted
    ↓
Under Review
    ↓
Investigation
    ↓
Action Taken
    ↓
Resolved
    ↓
Closed
```

### FR-07: Notifications

The system shall notify victims when important changes occur in their case.

---

# 4. Officer / Cybercrime Investigation Requirements

## FR-08: Officer Login

Authorized officers shall be able to securely log into the investigation portal.

## FR-09: View Assigned Cases

Officers shall be able to view complaints assigned to them.

## FR-10: Case Management

Officers shall be able to:

- View case details
- Update case status
- Add investigation notes
- Assign cases
- Set case priority
- Record investigation activities

## FR-11: Evidence Review

Officers shall be able to access evidence associated with authorized cases.

## FR-12: Evidence Chain of Custody

The system shall maintain a record of evidence handling.

The record can contain:

- Evidence ID
- Case ID
- Person who uploaded it
- Person who accessed it
- Date/time
- Action performed
- Evidence status

## FR-13: Suspect Management

Officers shall be able to create and manage suspect profiles.

A suspect profile may contain:

- Suspect ID
- Name/alias
- Contact information
- Associated cases
- Associated indicators
- Investigation notes

## FR-14: Agency Coordination

The system shall allow officers to record coordination actions with relevant agencies or financial institutions.

---

# 5. Threat Intelligence Requirements

## FR-15: Threat Feed Management

Authorized analysts shall be able to ingest and manage threat intelligence information.

Examples include:

- Malicious IP addresses
- Domains
- URLs
- File hashes
- Malware indicators
- Email indicators

## FR-16: IOC Management

The system shall store and manage **Indicators of Compromise (IOCs)**.

Example:

```text
IOC Type: IP
Value: 192.xxx.xxx.xxx
Threat Type: Malware
Risk: High
```

## FR-17: IOC Searching

Threat analysts shall be able to search for specific indicators.

## FR-18: Complaint–Threat Correlation

The system shall compare indicators found in complaints with available threat intelligence.

Example:

```text
Complaint A
      ↓
Suspicious IP
      ↓
Threat Intelligence Database
      ↓
Known Malicious IP
      ↓
Possible Threat Connection
```

## FR-19: Campaign Detection

The system shall identify possible relationships between multiple complaints based on common:

- IP addresses
- Domains
- URLs
- Email addresses
- File hashes
- Other indicators

## FR-20: Threat Analysis Dashboard

Threat analysts shall be able to view information such as:

- Number of threats
- High-risk indicators
- Threat categories
- Active campaigns
- Threat trends

## FR-21: Threat Forecasting

The system may analyze historical threat information to identify emerging threat patterns and provide risk indicators.

---

# 6. Incident Response & Security Operations Requirements

## FR-22: Incident Creation

Authorized users shall be able to create incident records when a security incident is identified.

## FR-23: Incident Classification

Incidents shall be categorized according to type and severity.

| Severity | Example |
|---|---|
| Low | Suspicious activity |
| Medium | Account compromise |
| High | Malware infection |
| Critical | Major coordinated attack |

## FR-24: Incident Tracking

The system shall track incidents through different stages.

```text
Detected
   ↓
Investigating
   ↓
Containing
   ↓
Remediating
   ↓
Resolved
```

## FR-25: Automated Response Playbooks

The system shall support predefined response workflows for selected incident types.

## FR-26: Incident Notifications

The system shall notify authorized personnel when critical incidents occur.

---

# 7. Administrative Requirements

## FR-27: Role-Based Access Control

The system shall support different roles.

| Role | Main Access |
|---|---|
| Victim | Own complaints and evidence |
| Officer | Cases and investigations |
| Threat Analyst | Threat intelligence |
| Incident Responder | Security incidents |
| Administrator | System administration |

## FR-28: User Management

Administrators shall be able to:

- Create users
- View users
- Activate/deactivate accounts
- Assign roles
- Manage permissions

## FR-29: Audit Logging

The system shall record important system activities.

Example:

```text
User: Officer01
Action: Updated Case
Case: CYB-2026-000125
Time: 10:35 AM
```

## FR-30: System Health Monitoring

Administrators shall be able to monitor:

- Backend/API status
- Database status
- Threat-feed processing
- Background processes
- System errors

---

# 8. Database Requirements

MySQL will act as the **central database**.

The database should store information related to:

### User Management

- Users
- Roles
- Permissions

### Victim Management

- Victim profiles
- Complaints
- Complaint status
- Notifications

### Evidence

- Evidence metadata
- Evidence access history
- Chain-of-custody records

### Investigation

- Cases
- Suspects
- Investigation notes
- Agency coordination

### Threat Intelligence

- Threat feeds
- IOCs
- Malware information
- Threat campaigns
- Threat relationships

### Incident Response

- Incidents
- Incident activities
- Response actions
- Playbooks

### Security

- Audit logs
- Login history
- System health information

---

# 9. API Requirements — FastAPI

FastAPI will act as the **backend layer** between Streamlit and MySQL.

The backend should provide APIs such as:

```text
POST   /auth/login
POST   /auth/register

POST   /complaints
GET    /complaints
GET    /complaints/{case_id}
PUT    /complaints/{case_id}

POST   /evidence
GET    /evidence/{case_id}

GET    /cases
PUT    /cases/{case_id}

POST   /suspects
GET    /suspects

POST   /threats
GET    /threats
POST   /iocs
GET    /iocs

POST   /incidents
GET    /incidents
PUT    /incidents/{incident_id}

GET    /notifications
GET    /audit-logs
GET    /system-health
```

These are logical API examples. The exact endpoints can be finalized during implementation.

---

# 10. Frontend Requirements — Streamlit

Streamlit will provide the user interface.

The application can contain separate dashboards.

## Victim Dashboard

```text
Dashboard
├── My Complaints
├── New Complaint
├── Upload Evidence
├── Track Case
└── Notifications
```

## Officer Dashboard

```text
Dashboard
├── Assigned Cases
├── Case Investigation
├── Evidence
├── Suspects
├── Chain of Custody
└── Agency Coordination
```

## Threat Intelligence Dashboard

```text
Dashboard
├── Threat Overview
├── IOC Search
├── Threat Feeds
├── Campaign Analysis
├── Threat Trends
└── Threat Forecast
```

## Admin/SOC Dashboard

```text
Dashboard
├── Active Incidents
├── Response Playbooks
├── Users & Roles
├── Audit Logs
└── System Health
```

---

# 11. Non-Functional Requirements

Non-functional requirements describe **how well the system should operate**.

## 11.1 Security

The system should:

- Authenticate users securely.
- Use password hashing.
- Implement RBAC.
- Protect APIs.
- Restrict access to sensitive evidence.
- Maintain audit logs.
- Validate uploaded files.
- Protect sensitive information.
- Use secure communication in deployment.

## 11.2 Performance

The system should provide:

- Fast API responses.
- Efficient database queries.
- Efficient complaint searching.
- Efficient IOC searching.
- Reasonable dashboard loading time.

## 11.3 Reliability

The system should:

- Handle invalid requests safely.
- Prevent accidental data loss.
- Maintain database consistency.
- Handle API/database failures gracefully.

## 11.4 Scalability

The architecture should allow future expansion to:

- More users
- More complaints
- More threat feeds
- More IOCs
- More officers
- More incidents

## 11.5 Maintainability

The Python project should be modular.

Example:

```text
backend/
├── routers/
├── models/
├── schemas/
├── services/
├── database/
└── security/

frontend/
├── pages/
├── components/
└── services/
```

This allows each team member to work on a separate sector without unnecessarily modifying other modules.

## 11.6 Usability

The interface should be:

- Simple
- Professional
- Consistent
- Easy to navigate
- Role-specific
- Suitable for non-technical users such as victims

---

# 12. Hardware Requirements

## Minimum Development System

| Component | Requirement |
|---|---|
| Processor | Intel Core i3 / equivalent |
| RAM | 8 GB |
| Storage | 10 GB+ free space |
| Operating System | Windows 10/11, Linux, or macOS |
| Network | Internet connection |
| Display | 1366 × 768 or higher |

## Recommended

| Component | Recommendation |
|---|---|
| Processor | Intel Core i5 / Ryzen 5 or better |
| RAM | 16 GB |
| Storage | SSD with 20 GB+ free space |
| Network | Stable broadband |
| OS | Windows 11 / Ubuntu |

---

# 13. Software Requirements

## Required

- Python 3.x
- FastAPI
- Uvicorn
- Streamlit
- MySQL Server
- MySQL Workbench
- Git
- GitHub
- PyCharm

## Python Libraries

Typical libraries for the project include:

```text
fastapi
uvicorn
streamlit
sqlalchemy
pymysql
pydantic
python-jose
passlib/bcrypt
python-multipart
requests
pandas
plotly
```

The exact libraries can be finalized based on the features implemented by the team.

---

# 14. Security Requirements

Because the project handles cybercrime complaints and evidence, security is one of the most important requirements.

The system should implement:

```text
Authentication
      ↓
Authorization
      ↓
RBAC
      ↓
Input Validation
      ↓
Secure Database Access
      ↓
Evidence Protection
      ↓
Audit Logging
```

Important security controls include:

- Password hashing
- JWT/token-based authentication
- Role-based authorization
- API input validation
- SQL injection prevention
- File-upload validation
- Access control for evidence
- Audit logging
- Session management
- Error handling without exposing sensitive information

---

# 15. Overall System Requirement

The final system should provide a **centralized and secure cybercrime management platform** where:

```text
Victim
  ↓
Complaint
  ↓
Tracking ID
  ↓
Officer Investigation
  ↓
Evidence + Suspect Analysis
  ↓
Threat Intelligence
  ↓
IOC Correlation
  ↓
Campaign Detection
  ↓
Incident Response
  ↓
Resolution
  ↓
Victim Notification
  ↓
Audit Trail
```

## Summary

The technology stack fits the project as follows:

- **Python** → Core programming language
- **FastAPI** → Backend/API and business logic
- **Streamlit** → Frontend dashboards and user interfaces
- **MySQL** → Central relational database

All four sectors should communicate through the **FastAPI backend** and share the centralized **MySQL database**, while **Streamlit** provides role-specific interfaces for victims, officers, threat analysts, incident responders, and administrators.
