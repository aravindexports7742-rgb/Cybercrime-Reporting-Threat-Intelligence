# Sector 4: Incident Response, Security Operations & Administrative Control

**CYBER CRIME & THREAT INTELLIGENCE PLATFORM — Final Year Project**
**Module Owner:** Team Member 4
**Technology Stack:** FastAPI (Backend) · Streamlit (Frontend) · MySQL (Database)

---

## 1. Sector Overview

The **Incident Response, Security Operations & Administrative Control** sector is responsible for the security backbone of the entire platform. It has three tightly related responsibilities: managing formal security incidents, operating platform-wide security monitoring, and administering user roles, permissions, and audit controls for all four sectors.

Where Sectors 1–3 handle the case-facing workflow, Sector 4 protects and governs the platform itself — recording incidents, coordinating response, enforcing access control, and maintaining the audit trail that underpins accountability across the system.

---

## 2. Objectives

1. Record and track security incidents through a defined lifecycle.
2. Coordinate response actions and support predefined response playbooks.
3. Enforce Role-Based Access Control (RBAC) for every user across all sectors.
4. Maintain a comprehensive, tamper-evident audit log of platform activity.
5. Monitor system health across the API, database, authentication, and background services.
6. Provide administrators with centralized oversight of users, roles, and permissions.

---

## 3. Member Responsibility

Team Member 4 owns:

- The Streamlit Admin/SOC dashboard
- The FastAPI endpoints listed in Section 8
- The database tables listed in Section 9, plus shared ownership of `users`, `roles`, `permissions`, and `role_permissions`
- The RBAC enforcement layer used by all other sectors
- The audit-logging and login-history mechanism used by all other sectors
- Coordination with Sectors 1–3 for incident escalation

---

## 4. Functional Modules

### Part A — Incident Response

#### 4.1 Incident Creation

Authorized responders can create an incident whenever a security event requires investigation or response. An incident record captures: incident ID, title, type, description, severity, detected date/time, assigned responder, current status, related case, and related IOC.

```text
INC-2026-00015
Type: Malware
Severity: High
Status: Investigating
```

#### 4.2 Incident Classification

| Severity | Example |
|---|---|
| Low | Suspicious activity |
| Medium | Account compromise |
| High | Malware infection |
| Critical | Major coordinated security incident |

Severity is assigned according to documented organizational rules.

#### 4.3 Incident Lifecycle

```text
Detected → Triage → Investigating → Containing → Remediating → Recovering → Resolved → Closed
```

The lifecycle may be simplified for the scope of the academic implementation.

### Part B — Automated Response Playbooks

#### 4.4 Playbook Concept

A playbook is a predefined sequence of actions for a known incident type. Automated actions execute strictly within the permissions and controls defined by the system.

```text
Incident Detected
      │
      ▼
Classify Incident
      │
      ▼
Create Incident Record
      │
      ▼
Notify Responsible Team
      │
      ▼
Perform Authorized Containment Action
      │
      ▼
Collect Relevant Logs
      │
      ▼
Update Incident
      │
      ▼
Close After Review
```

#### 4.5 Example Playbooks

**Malware Incident**

```text
Detect Malware IOC → Create Incident → Assign Responder → Record IOC →
Notify Security Team → Containment Workflow → Investigation
```

**Suspicious Account Activity**

```text
Suspicious Activity → Create Incident → Check Related Events →
Notify Authorized Officer → Apply Approved Response → Record Result
```

### Part C — Security Operations

#### 4.6 Security Monitoring

The platform provides an overview of system health and security events across: API availability, database availability, authentication service, threat-feed processing, background jobs, application errors, and active incidents.

#### 4.7 System Health Dashboard

```text
System Health
├── API Status
├── Database Status
├── Authentication Status
├── Threat Feed Status
├── Background Job Status
└── Active Incidents
```

Example:

```text
API              → Healthy
Database         → Healthy
Authentication   → Healthy
Threat Feed      → Warning
```

### Part D — Administrative Control

#### 4.8 Role-Based Access Control (RBAC)

| Role | Main Access |
|---|---|
| Victim | Own complaints and evidence |
| Officer | Authorized cases and investigations |
| Threat Analyst | Threat intelligence |
| Incident Responder | Security incidents |
| Administrator | System administration |

#### 4.9 User Management

Administrators manage user accounts, roles, account status, permissions, and access settings.

```text
Create User → Assign Role → Activate Account → User Logs In → RBAC Determines Access
```

#### 4.10 Audit Logging

```text
User: Officer01
Action: Updated Case
Case: CYB-2026-000125
Time: 10:35 AM
Result: Success
```

Audit fields: log ID, user ID, action, resource, resource ID, timestamp, IP address (where applicable), and result.

#### 4.11 Login & Security Monitoring

The system records successful logins, failed logins, logouts, account activation/deactivation, and role changes, supporting administrator investigation of suspicious access.

---

## 5. Workflow

```text
Sector 1 (Victim Complaint)
        │
        ▼
Sector 2 (Investigation)
        │
        ▼
Sector 3 (Threat Intelligence)
        │
        ▼
Threat / Incident Finding
        │
        ▼
Sector 4 (Incident Response)
        │
        ▼
Response + Audit
```

Sector 4 also governs access to the entire platform via RBAC, independent of the case-processing flow above.

---

## 6. Dashboard Design

```text
Admin / SOC Dashboard
├── Overview
├── Active Incidents
├── Response Playbooks
├── Users
├── Roles & Permissions
├── Audit Logs
├── Login Activity
└── System Health
```

---

## 7. API Design

```text
POST   /incidents                              Create an incident
GET    /incidents                              List incidents
GET    /incidents/{incident_id}                Retrieve incident detail
PUT    /incidents/{incident_id}                Update incident

GET    /playbooks                              List playbooks
POST   /playbooks                              Create a playbook
POST   /incidents/{incident_id}/execute-playbook   Execute a playbook against an incident

GET    /users                                  List users
POST   /users                                  Create a user
PUT    /users/{user_id}                        Update a user

GET    /roles                                  List roles
PUT    /users/{user_id}/role                   Assign a role to a user

GET    /audit-logs                             Retrieve audit log entries
GET    /system-health                          Retrieve current system health status
```

---

## 8. Database Responsibility

| Table | Purpose |
|---|---|
| `incidents` | Core incident records |
| `incident_activities` | Chronological activity log per incident |
| `response_actions` | Actions taken in response to an incident |
| `playbooks` | Predefined response workflows |
| `playbook_steps` | Ordered steps within a playbook |
| `audit_logs` | Platform-wide audit trail (shared across all sectors) |
| `login_history` | Authentication event history |
| `system_health` | Recorded system/service health snapshots |

Shared identity/RBAC tables co-owned with Sector 1: `users`, `roles`, `permissions`, `role_permissions`.

---

## 9. Security Considerations

This sector is directly responsible for platform-wide security controls:

- Secure authentication and password hashing
- RBAC enforcement for every endpoint across all four sectors
- Authorization checks on every protected route
- API protection and input validation
- Comprehensive audit logging
- Session management
- Secure error handling that avoids leaking sensitive internals
- Database access control

---

## 10. Integration with Other Sectors

Sector 4 sits downstream of the case-processing pipeline and underneath all other sectors simultaneously:

```text
Sector 1 → Sector 2 → Sector 3 → Sector 4 (escalation path)
Sector 4 → Sectors 1, 2, 3 (RBAC + audit logging, foundational)
```

- **Receives** escalated findings and incidents from Sectors 2 and 3.
- **Provides** the RBAC and audit-logging infrastructure consumed by every other sector.
- **Provides** the shared `users`/`roles`/`permissions` schema that anchors identity across the platform.

---

## 11. Final Deliverables

1. Streamlit Admin/SOC dashboard covering incidents, playbooks, users, roles, audit logs, login activity, and system health.
2. FastAPI backend implementing all endpoints listed in Section 7.
3. MySQL tables listed in Section 8, integrated into the shared project database.
4. A working RBAC enforcement layer used across all four sectors.
5. A platform-wide audit-logging mechanism.
6. Sector documentation (this file) suitable for inclusion in the final project report.
