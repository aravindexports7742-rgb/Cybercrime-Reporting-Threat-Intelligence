# Sector 2: Officer / Cybercrime Response & Investigation Portal

**CYBER CRIME & THREAT INTELLIGENCE PLATFORM — Final Year Project**
**Module Owner:** Team Member 2
**Technology Stack:** FastAPI (Backend) · Streamlit (Frontend) · MySQL (Database)

---

## 1. Sector Overview

The **Officer / Cybercrime Response & Investigation Portal** is the internal investigation workspace used by authorized cybercrime officers. Its purpose is to transform raw victim complaints (received from Sector 1) into structured, evidence-backed investigation cases.

Within this sector, officers review complaints, manage case assignment and priority, examine evidence under a documented chain of custody, build suspect profiles, record investigation activity, coordinate with external agencies or banks, and progress each case toward resolution. All of this is consolidated into one centralized workspace so that officers are not required to maintain investigation records outside the platform.

---

## 2. Objectives

1. Provide officers with a single, centralized system covering the complete investigation lifecycle.
2. Ensure every investigative action is recorded, attributable, and auditable.
3. Maintain a legally defensible chain of custody for all digital evidence.
4. Support structured suspect and indicator tracking that feeds directly into threat correlation (Sector 3).
5. Enable documented coordination with banks and external agencies for financial fraud cases.
6. Guarantee that only authorized officers can access investigation-sensitive data.

---

## 3. Member Responsibility

Team Member 2 owns:

- The Streamlit officer dashboard and all investigation-facing views
- The FastAPI endpoints listed in Section 8
- The database tables listed in Section 9
- Enforcement of case-level and evidence-level access control
- Coordination with Sector 1 for complaint intake and status synchronization
- Coordination with Sector 3 for indicator hand-off
- Coordination with Sector 4 for incident escalation and audit logging

---

## 4. Functional Modules

### 4.1 Officer Authentication & Access Control

Only authenticated, authorized officers may access the investigation portal. The backend verifies user identity, account status, assigned role, and permissions on every request. RBAC strictly prevents victims and unauthorized accounts from viewing investigation data.

### 4.2 Case Management

Officers can view assigned cases, review the originating complaint, set case priority (`Low`, `Medium`, `High`, `Critical`), assign cases where permitted, update case status, add investigation notes, and review the full history of prior actions on a case.

### 4.3 Evidence Review

Officers may review all evidence linked to cases they are authorized to investigate. Evidence records include the evidence ID, case ID, evidence type, file name, upload date, uploading party, an optional hash/checksum, and current status. Unauthorized access attempts are blocked and logged.

### 4.4 Chain of Custody

Every meaningful interaction with a piece of evidence — registration, access, review, transfer for analysis — is recorded as a discrete, timestamped custody event, producing a fully auditable evidence history:

```text
Victim Uploads Evidence
        │
        ▼
Evidence Registered
        │
        ▼
Officer A Accesses Evidence
        │
        ▼
Officer B Reviews Evidence
        │
        ▼
Evidence Sent for Authorized Analysis
        │
        ▼
Investigation Completed
```

Each custody record stores: evidence ID, acting user, action performed, timestamp, associated case ID, and optional notes.

### 4.5 Suspect Management

Officers can create suspect profiles based on authorized investigation findings, including name/alias, contact information, associated cases, associated indicators (IPs, domains, emails), investigation notes, and current status.

### 4.6 Investigation Notes & Activity Log

Officers record structured investigation activities (date, officer, action taken, result), preserving a complete history of investigative steps for each case.

### 4.7 Agency and Bank Coordination

For financial fraud cases, officers can log coordination requests with banks or authorized agencies, including organization, request type, case ID, request date, status, response received, and the responsible officer. The platform documents this coordination; the underlying external actions remain governed by the relevant authority's own procedures.

### 4.8 Case Status Management

```text
New → Under Review → Assigned → Investigation → Pending External Response → Action Taken → Resolved → Closed
```

---

## 5. Workflow

```text
Complaint Received (from Sector 1)
        │
        ▼
Officer Reviews Complaint
        │
        ▼
Case Assigned
        │
        ▼
Evidence Examined
        │
        ▼
Investigation Activities Recorded
        │
        ▼
Suspects / Indicators Identified
        │
        ▼
Threat Intelligence Checked (Sector 3)
        │
        ▼
Agency / Bank Coordination (where required)
        │
        ▼
Investigation Result Determined
        │
        ▼
Case Resolved / Closed
```

---

## 6. Dashboard Design

```text
Officer Dashboard
├── Overview                (assigned case summary, priority breakdown)
├── Assigned Cases           (cases owned by the logged-in officer)
├── All Authorized Cases     (cases visible per RBAC scope)
├── Case Details             (full case record and timeline)
├── Evidence                 (evidence list per case)
├── Chain of Custody         (audit trail per evidence item)
├── Suspects                 (suspect profile management)
├── Investigation Notes      (chronological activity log)
├── Agency Coordination      (external request tracking)
└── Notifications            (case events relevant to the officer)
```

---

## 7. API Design

```text
GET    /cases                              List cases visible to the officer
GET    /cases/{case_id}                    Retrieve full case detail
PUT    /cases/{case_id}                    Update case status/priority

POST   /investigations                     Record a new investigation activity
GET    /investigations/{case_id}           Retrieve investigation history

GET    /evidence/{case_id}                 List evidence for a case
POST   /evidence/{evidence_id}/access      Log a chain-of-custody access event

POST   /suspects                           Create a suspect profile
GET    /suspects                           List suspects
GET    /suspects/{suspect_id}              Retrieve suspect detail

POST   /coordination                       Log an agency/bank coordination request
GET    /coordination/{case_id}             List coordination records for a case
```

Final route naming is confirmed jointly across all four sector owners.

---

## 8. Database Responsibility

| Table | Purpose |
|---|---|
| `cases` | Core investigation case records, linked to `complaints` |
| `case_assignments` | Officer-to-case assignment history |
| `investigation_notes` | Structured investigator observations |
| `investigation_activities` | Chronological activity log per case |
| `suspects` | Suspect profile records |
| `case_suspects` | Many-to-many link between cases and suspects |
| `chain_of_custody` | Timestamped evidence handling events |
| `evidence_access_history` | Access log for evidence records |
| `agency_coordination` | External agency/bank coordination requests |

---

## 9. Security Considerations

- **Officer Authentication & RBAC:** All access requires an authenticated officer account with the appropriate role/permission set.
- **Case-Level Access Control:** Officers see only cases they are assigned to or otherwise authorized for.
- **Evidence Access Restrictions:** Every evidence access is authenticated, authorized, and logged to the chain of custody.
- **Audit Logging:** All case, evidence, and suspect actions are written to the shared `audit_logs` table (Sector 4).
- **Secure API Endpoints:** All investigation endpoints require valid JWTs and enforce RBAC server-side.
- **Input Validation:** All submitted case, note, and coordination data is validated via Pydantic schemas.
- **Secure File Handling:** Evidence files inherit the access-controlled storage strategy defined in Sector 1.

---

## 10. Integration with Other Sectors

```text
Sector 1 (Victim Complaint)
        ▼
Sector 2 (Officer Investigation)
        ▼
Sector 3 (Threat Intelligence)
        ▼
Sector 4 (Incident Response)
```

- **Receives** newly submitted complaints from Sector 1 and writes status updates back so victims see accurate progress.
- **Sends** investigation-derived indicators (IPs, domains, emails, hashes) to Sector 3 for correlation and campaign detection.
- **Escalates** significant findings to Sector 4 for formal incident creation and response.
- **Consumes** the shared RBAC/audit infrastructure owned by Sector 4.

---

## 11. Final Deliverables

1. Streamlit officer investigation portal covering case management, evidence review, chain of custody, suspects, notes, and coordination.
2. FastAPI backend implementing all endpoints listed in Section 7 with RBAC enforcement.
3. MySQL tables listed in Section 8, integrated into the shared project database.
4. A fully auditable chain-of-custody mechanism for evidence.
5. Documented indicator hand-off pathway to Sector 3.
6. Sector documentation (this file) suitable for inclusion in the final project report.
