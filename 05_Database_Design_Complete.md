# CYBER CRIME & THREAT INTELLIGENCE PLATFORM
## Complete Shared MySQL Database Design

This document defines the **single, integrated MySQL database** shared by all four project sectors. There is one schema, not four — ownership below indicates which team member is responsible for developing and maintaining a given table, not a separate database.

---

## 1. Database Ownership Table

| # | Table | Owner |
|---|---|---|
| 1 | `users` | Shared (Member 1 & Member 4) |
| 2 | `roles` | Member 4 |
| 3 | `permissions` | Member 4 |
| 4 | `role_permissions` | Member 4 |
| 5 | `victim_profiles` | Member 1 |
| 6 | `complaints` | Member 1 |
| 7 | `complaint_categories` | Member 1 |
| 8 | `evidence` | Member 1 |
| 9 | `notifications` | Member 1 |
| 10 | `cases` | Member 2 |
| 11 | `case_assignments` | Member 2 |
| 12 | `investigation_notes` | Member 2 |
| 13 | `investigation_activities` | Member 2 |
| 14 | `suspects` | Member 2 |
| 15 | `case_suspects` | Member 2 |
| 16 | `chain_of_custody` | Member 2 |
| 17 | `evidence_access_history` | Member 2 |
| 18 | `agency_coordination` | Member 2 |
| 19 | `threat_sources` | Member 3 |
| 20 | `threat_feeds` | Member 3 |
| 21 | `threat_categories` | Member 3 |
| 22 | `iocs` | Member 3 |
| 23 | `malware_indicators` | Member 3 |
| 24 | `campaigns` | Member 3 |
| 25 | `campaign_iocs` | Member 3 |
| 26 | `complaint_iocs` | Member 3 |
| 27 | `threat_relationships` | Member 3 |
| 28 | `threat_analysis_results` | Member 3 |
| 29 | `incidents` | Member 4 |
| 30 | `incident_activities` | Member 4 |
| 31 | `response_actions` | Member 4 |
| 32 | `playbooks` | Member 4 |
| 33 | `playbook_steps` | Member 4 |
| 34 | `audit_logs` | Member 4 |
| 35 | `login_history` | Member 4 |
| 36 | `system_health` | Member 4 |

---

## 2. Database Relationship Diagram

```text
users
│
├── roles ── role_permissions ── permissions
│
├── victim_profiles
│
├── complaints
│      ├── complaint_categories
│      ├── evidence
│      │      └── evidence_access_history
│      ├── notifications
│      ├── complaint_iocs ── iocs
│      │
│      └── cases
│              ├── case_assignments
│              ├── investigation_notes
│              ├── investigation_activities
│              ├── case_suspects ── suspects
│              ├── chain_of_custody
│              └── agency_coordination
│
├── threat_sources ── threat_feeds
│
├── iocs
│      ├── malware_indicators
│      ├── threat_categories
│      ├── threat_relationships
│      └── campaign_iocs ── campaigns
│
├── threat_analysis_results
│
├── incidents
│      ├── incident_activities
│      ├── response_actions
│      └── playbooks ── playbook_steps
│
├── audit_logs
├── login_history
└── system_health
```

---

## 3. Table Specifications

Below, every table lists purpose, owner, primary key, foreign keys, key columns, relationships, and constraints. Full `CREATE TABLE` SQL is provided in Section 4.

### 3.1 Shared Identity & RBAC

**`users`** — Purpose: central identity record for every account on the platform, regardless of role. Owner: Shared (Member 1 / Member 4). PK: `user_id`. FK: `role_id → roles.role_id`. Key columns: `full_name`, `email` (unique), `phone_number`, `password_hash`, `role_id`, `account_status`, `created_at`, `updated_at`. Relationships: one-to-one with `victim_profiles`; one-to-many with `complaints`, `cases` (as officer), `login_history`, `audit_logs`. Constraints: `email` UNIQUE NOT NULL; `password_hash` NOT NULL; `account_status` ENUM.

**`roles`** — Purpose: defines platform roles. Owner: Member 4. PK: `role_id`. Key columns: `role_name` (Victim, Officer, Threat Analyst, Incident Responder, Administrator), `description`. Relationships: one-to-many with `users`; many-to-many with `permissions` via `role_permissions`.

**`permissions`** — Purpose: defines granular platform permissions. Owner: Member 4. PK: `permission_id`. Key columns: `permission_name`, `description`. Relationships: many-to-many with `roles`.

**`role_permissions`** — Purpose: junction table mapping roles to permissions. Owner: Member 4. PK: composite (`role_id`, `permission_id`). FKs: `role_id → roles.role_id`, `permission_id → permissions.permission_id`.

### 3.2 Member 1 — Victim Portal & Complaint Management

**`victim_profiles`** — Purpose: victim-specific profile data. Owner: Member 1. PK: `victim_id`. FK: `user_id → users.user_id`. Key columns: `address`, `date_of_birth`, `id_document_reference`. Constraints: `user_id` UNIQUE (one profile per user).

**`complaints`** — Purpose: core complaint/case-intake record. Owner: Member 1. PK: `complaint_id`. FKs: `victim_id → victim_profiles.victim_id`, `category_id → complaint_categories.category_id`. Key columns: `tracking_id` (unique, e.g. `CYB-2026-000125`), `title`, `incident_date`, `description`, `financial_loss`, `suspected_url`, `suspected_phone`, `suspected_email`, `status`, `created_at`, `updated_at`. Relationships: one-to-many with `evidence`, `notifications`, `complaint_iocs`; one-to-one/one-to-many with `cases`. Constraints: `tracking_id` UNIQUE NOT NULL; `status` ENUM (Submitted, Under Review, Assigned, Investigation, Action Taken, Resolved, Closed).

**`complaint_categories`** — Purpose: lookup table of supported complaint types. Owner: Member 1. PK: `category_id`. Key columns: `category_name`, `description`.

**`evidence`** — Purpose: evidence metadata linked to a complaint. Owner: Member 1. PK: `evidence_id`. FKs: `complaint_id → complaints.complaint_id`, `uploaded_by → users.user_id`. Key columns: `file_name`, `evidence_type`, `file_hash`, `upload_date`, `status`. Relationships: one-to-many with `chain_of_custody`, `evidence_access_history`.

**`notifications`** — Purpose: victim-facing case event notifications. Owner: Member 1. PK: `notification_id`. FKs: `user_id → users.user_id`, `complaint_id → complaints.complaint_id`. Key columns: `message`, `event_type`, `is_read`, `created_at`.

### 3.3 Member 2 — Officer Investigation Portal

**`cases`** — Purpose: formal investigation case derived from a complaint. Owner: Member 2. PK: `case_id`. FKs: `complaint_id → complaints.complaint_id`, `lead_officer_id → users.user_id`. Key columns: `case_reference`, `priority`, `status`, `opened_at`, `closed_at`. Constraints: `priority` ENUM (Low, Medium, High, Critical); `status` ENUM matching Section 4.7 of Sector 2 documentation.

**`case_assignments`** — Purpose: officer-to-case assignment history. Owner: Member 2. PK: `assignment_id`. FKs: `case_id → cases.case_id`, `officer_id → users.user_id`. Key columns: `assigned_at`, `unassigned_at`, `assigned_by`.

**`investigation_notes`** — Purpose: structured investigator observations. Owner: Member 2. PK: `note_id`. FKs: `case_id → cases.case_id`, `officer_id → users.user_id`. Key columns: `note_text`, `created_at`.

**`investigation_activities`** — Purpose: chronological activity/action log per case. Owner: Member 2. PK: `activity_id`. FKs: `case_id → cases.case_id`, `officer_id → users.user_id`. Key columns: `action`, `result`, `activity_date`.

**`suspects`** — Purpose: suspect profile records. Owner: Member 2. PK: `suspect_id`. Key columns: `name_alias`, `contact_info`, `status`, `notes`.

**`case_suspects`** — Purpose: many-to-many link between cases and suspects. Owner: Member 2. PK: composite (`case_id`, `suspect_id`). FKs: `case_id → cases.case_id`, `suspect_id → suspects.suspect_id`.

**`chain_of_custody`** — Purpose: timestamped custody events for evidence. Owner: Member 2. PK: `custody_id`. FKs: `evidence_id → evidence.evidence_id`, `user_id → users.user_id`, `case_id → cases.case_id`. Key columns: `action`, `event_time`, `notes`.

**`evidence_access_history`** — Purpose: access log for evidence records. Owner: Member 2. PK: `access_id`. FKs: `evidence_id → evidence.evidence_id`, `user_id → users.user_id`. Key columns: `access_time`, `access_type`.

**`agency_coordination`** — Purpose: external agency/bank coordination requests. Owner: Member 2. PK: `coordination_id`. FKs: `case_id → cases.case_id`, `officer_id → users.user_id`. Key columns: `organization_name`, `request_type`, `request_date`, `status`, `response`.

### 3.4 Member 3 — Threat Intelligence

**`threat_sources`** — Purpose: registered authorized intelligence sources. Owner: Member 3. PK: `source_id`. Key columns: `source_name`, `source_type`, `reliability_rating`.

**`threat_feeds`** — Purpose: ingested feed batches. Owner: Member 3. PK: `feed_id`. FK: `source_id → threat_sources.source_id`. Key columns: `ingested_at`, `record_count`, `status`.

**`threat_categories`** — Purpose: lookup table of threat classification types. Owner: Member 3. PK: `category_id`. Key columns: `category_name`, `description`.

**`iocs`** — Purpose: Indicators of Compromise. Owner: Member 3. PK: `ioc_id`. FKs: `category_id → threat_categories.category_id`, `source_id → threat_sources.source_id`. Key columns: `ioc_type` (IP, Domain, URL, Hash, Email), `ioc_value`, `risk_level`, `first_seen`, `last_seen`. Constraints: unique composite (`ioc_type`, `ioc_value`).

**`malware_indicators`** — Purpose: malware-specific indicator detail. Owner: Member 3. PK: `malware_id`. FK: `ioc_id → iocs.ioc_id`. Key columns: `malware_family`, `signature`, `description`.

**`campaigns`** — Purpose: detected/tracked campaigns. Owner: Member 3. PK: `campaign_id`. Key columns: `campaign_name`, `description`, `risk_level`, `detected_at`.

**`campaign_iocs`** — Purpose: many-to-many link between campaigns and IOCs. Owner: Member 3. PK: composite (`campaign_id`, `ioc_id`). FKs: `campaign_id → campaigns.campaign_id`, `ioc_id → iocs.ioc_id`.

**`complaint_iocs`** — Purpose: link between complaints and extracted indicators. Owner: Member 3. PK: composite (`complaint_id`, `ioc_id`). FKs: `complaint_id → complaints.complaint_id`, `ioc_id → iocs.ioc_id`.

**`threat_relationships`** — Purpose: relationships identified between indicators or cases. Owner: Member 3. PK: `relationship_id`. FKs: `ioc_id_a → iocs.ioc_id`, `ioc_id_b → iocs.ioc_id`. Key columns: `relationship_type`, `confidence_level`.

**`threat_analysis_results`** — Purpose: stored output of correlation/analysis runs. Owner: Member 3. PK: `result_id`. FK: `related_case_id → cases.case_id` (nullable). Key columns: `analysis_type`, `summary`, `generated_at`.

### 3.5 Member 4 — Incident Response, Security Operations & Admin

**`incidents`** — Purpose: formal security incident records. Owner: Member 4. PK: `incident_id`. FKs: `case_id → cases.case_id` (nullable), `ioc_id → iocs.ioc_id` (nullable), `responder_id → users.user_id`. Key columns: `incident_reference`, `incident_type`, `description`, `severity`, `status`, `detected_at`. Constraints: `severity` ENUM (Low, Medium, High, Critical); `status` ENUM per Sector 4 lifecycle.

**`incident_activities`** — Purpose: chronological activity log per incident. Owner: Member 4. PK: `activity_id`. FK: `incident_id → incidents.incident_id`. Key columns: `action`, `performed_by`, `activity_time`.

**`response_actions`** — Purpose: response actions taken for an incident. Owner: Member 4. PK: `action_id`. FK: `incident_id → incidents.incident_id`. Key columns: `action_type`, `description`, `performed_at`, `performed_by`.

**`playbooks`** — Purpose: predefined response workflows. Owner: Member 4. PK: `playbook_id`. Key columns: `playbook_name`, `incident_type`, `description`.

**`playbook_steps`** — Purpose: ordered steps within a playbook. Owner: Member 4. PK: `step_id`. FK: `playbook_id → playbooks.playbook_id`. Key columns: `step_order`, `step_description`.

**`audit_logs`** — Purpose: platform-wide audit trail. Owner: Member 4. PK: `log_id`. FK: `user_id → users.user_id`. Key columns: `action`, `resource`, `resource_id`, `event_time`, `ip_address`, `result`.

**`login_history`** — Purpose: authentication event history. Owner: Member 4. PK: `login_id`. FK: `user_id → users.user_id`. Key columns: `event_type` (Login Success, Login Failed, Logout), `event_time`, `ip_address`.

**`system_health`** — Purpose: recorded system/service health snapshots. Owner: Member 4. PK: `health_id`. Key columns: `component_name`, `status`, `checked_at`, `details`.

---

## 4. SQL Schema — CREATE TABLE Statements

```sql
-- =========================================================
-- SHARED: IDENTITY & RBAC
-- =========================================================

CREATE TABLE roles (
    role_id        INT AUTO_INCREMENT PRIMARY KEY,
    role_name      ENUM('Victim','Officer','Threat Analyst','Incident Responder','Administrator') NOT NULL UNIQUE,
    description    VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE permissions (
    permission_id   INT AUTO_INCREMENT PRIMARY KEY,
    permission_name VARCHAR(100) NOT NULL UNIQUE,
    description     VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE role_permissions (
    role_id        INT NOT NULL,
    permission_id  INT NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(permission_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE users (
    user_id        INT AUTO_INCREMENT PRIMARY KEY,
    full_name      VARCHAR(150) NOT NULL,
    email          VARCHAR(150) NOT NULL UNIQUE,
    phone_number   VARCHAR(20),
    password_hash  VARCHAR(255) NOT NULL,
    role_id        INT NOT NULL,
    account_status ENUM('Active','Inactive','Suspended') NOT NULL DEFAULT 'Active',
    created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_users_email (email)
) ENGINE=InnoDB;

-- =========================================================
-- MEMBER 1: VICTIM PORTAL & COMPLAINT MANAGEMENT
-- =========================================================

CREATE TABLE victim_profiles (
    victim_id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id             INT NOT NULL UNIQUE,
    address             VARCHAR(255),
    date_of_birth       DATE,
    id_document_reference VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE complaint_categories (
    category_id    INT AUTO_INCREMENT PRIMARY KEY,
    category_name  VARCHAR(100) NOT NULL UNIQUE,
    description    VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE complaints (
    complaint_id     INT AUTO_INCREMENT PRIMARY KEY,
    tracking_id      VARCHAR(20) NOT NULL UNIQUE,
    victim_id        INT NOT NULL,
    category_id      INT NOT NULL,
    title            VARCHAR(200) NOT NULL,
    incident_date    DATE,
    description      TEXT,
    financial_loss   DECIMAL(12,2) DEFAULT 0.00,
    suspected_url    VARCHAR(255),
    suspected_phone  VARCHAR(20),
    suspected_email  VARCHAR(150),
    status           ENUM('Submitted','Under Review','Assigned','Investigation','Action Taken','Resolved','Closed')
                     NOT NULL DEFAULT 'Submitted',
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (victim_id) REFERENCES victim_profiles(victim_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (category_id) REFERENCES complaint_categories(category_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_complaints_status (status),
    INDEX idx_complaints_tracking (tracking_id)
) ENGINE=InnoDB;

CREATE TABLE evidence (
    evidence_id    INT AUTO_INCREMENT PRIMARY KEY,
    complaint_id   INT NOT NULL,
    uploaded_by    INT NOT NULL,
    file_name      VARCHAR(255) NOT NULL,
    evidence_type  VARCHAR(50),
    file_hash      VARCHAR(128),
    upload_date    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status         ENUM('Active','Under Review','Archived') NOT NULL DEFAULT 'Active',
    FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    complaint_id    INT,
    message         VARCHAR(255) NOT NULL,
    event_type      VARCHAR(50),
    is_read         BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================================================
-- MEMBER 2: OFFICER / INVESTIGATION PORTAL
-- =========================================================

CREATE TABLE cases (
    case_id          INT AUTO_INCREMENT PRIMARY KEY,
    case_reference   VARCHAR(30) NOT NULL UNIQUE,
    complaint_id     INT NOT NULL,
    lead_officer_id  INT,
    priority         ENUM('Low','Medium','High','Critical') NOT NULL DEFAULT 'Medium',
    status           ENUM('New','Under Review','Assigned','Investigation','Pending External Response',
                           'Action Taken','Resolved','Closed') NOT NULL DEFAULT 'New',
    opened_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at        DATETIME NULL,
    FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (lead_officer_id) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_cases_status (status)
) ENGINE=InnoDB;

CREATE TABLE case_assignments (
    assignment_id  INT AUTO_INCREMENT PRIMARY KEY,
    case_id        INT NOT NULL,
    officer_id     INT NOT NULL,
    assigned_by    INT,
    assigned_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    unassigned_at  DATETIME NULL,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (officer_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE investigation_notes (
    note_id      INT AUTO_INCREMENT PRIMARY KEY,
    case_id      INT NOT NULL,
    officer_id   INT NOT NULL,
    note_text    TEXT NOT NULL,
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (officer_id) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE investigation_activities (
    activity_id    INT AUTO_INCREMENT PRIMARY KEY,
    case_id        INT NOT NULL,
    officer_id     INT NOT NULL,
    action         VARCHAR(255) NOT NULL,
    result         VARCHAR(255),
    activity_date  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (officer_id) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE suspects (
    suspect_id   INT AUTO_INCREMENT PRIMARY KEY,
    name_alias   VARCHAR(150),
    contact_info VARCHAR(255),
    status       ENUM('Person of Interest','Confirmed','Cleared') NOT NULL DEFAULT 'Person of Interest',
    notes        TEXT
) ENGINE=InnoDB;

CREATE TABLE case_suspects (
    case_id    INT NOT NULL,
    suspect_id INT NOT NULL,
    PRIMARY KEY (case_id, suspect_id),
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (suspect_id) REFERENCES suspects(suspect_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE chain_of_custody (
    custody_id   INT AUTO_INCREMENT PRIMARY KEY,
    evidence_id  INT NOT NULL,
    case_id      INT NOT NULL,
    user_id      INT NOT NULL,
    action       VARCHAR(100) NOT NULL,
    event_time   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes        VARCHAR(255),
    FOREIGN KEY (evidence_id) REFERENCES evidence(evidence_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE evidence_access_history (
    access_id    INT AUTO_INCREMENT PRIMARY KEY,
    evidence_id  INT NOT NULL,
    user_id      INT NOT NULL,
    access_time  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    access_type  ENUM('View','Download','Analyze') NOT NULL DEFAULT 'View',
    FOREIGN KEY (evidence_id) REFERENCES evidence(evidence_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE agency_coordination (
    coordination_id  INT AUTO_INCREMENT PRIMARY KEY,
    case_id          INT NOT NULL,
    officer_id       INT NOT NULL,
    organization_name VARCHAR(150) NOT NULL,
    request_type     VARCHAR(100),
    request_date     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status           ENUM('Pending','Responded','Closed') NOT NULL DEFAULT 'Pending',
    response         TEXT,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (officer_id) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================================================
-- MEMBER 3: THREAT INTELLIGENCE
-- =========================================================

CREATE TABLE threat_sources (
    source_id           INT AUTO_INCREMENT PRIMARY KEY,
    source_name         VARCHAR(150) NOT NULL,
    source_type         VARCHAR(100),
    reliability_rating  ENUM('Low','Medium','High') DEFAULT 'Medium'
) ENGINE=InnoDB;

CREATE TABLE threat_feeds (
    feed_id       INT AUTO_INCREMENT PRIMARY KEY,
    source_id     INT NOT NULL,
    ingested_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    record_count  INT DEFAULT 0,
    status        ENUM('Success','Partial','Failed') NOT NULL DEFAULT 'Success',
    FOREIGN KEY (source_id) REFERENCES threat_sources(source_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE threat_categories (
    category_id   INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description   VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE iocs (
    ioc_id       INT AUTO_INCREMENT PRIMARY KEY,
    ioc_type     ENUM('IP','Domain','URL','Hash','Email') NOT NULL,
    ioc_value    VARCHAR(255) NOT NULL,
    category_id  INT,
    source_id    INT,
    risk_level   ENUM('Low','Medium','High','Critical') NOT NULL DEFAULT 'Low',
    first_seen   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES threat_categories(category_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (source_id) REFERENCES threat_sources(source_id) ON DELETE SET NULL ON UPDATE CASCADE,
    UNIQUE KEY uq_ioc_type_value (ioc_type, ioc_value),
    INDEX idx_iocs_risk (risk_level)
) ENGINE=InnoDB;

CREATE TABLE malware_indicators (
    malware_id     INT AUTO_INCREMENT PRIMARY KEY,
    ioc_id         INT NOT NULL,
    malware_family VARCHAR(150),
    signature      VARCHAR(255),
    description    TEXT,
    FOREIGN KEY (ioc_id) REFERENCES iocs(ioc_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE campaigns (
    campaign_id   INT AUTO_INCREMENT PRIMARY KEY,
    campaign_name VARCHAR(150) NOT NULL,
    description   TEXT,
    risk_level    ENUM('Low','Medium','High','Critical') NOT NULL DEFAULT 'Medium',
    detected_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE campaign_iocs (
    campaign_id INT NOT NULL,
    ioc_id      INT NOT NULL,
    PRIMARY KEY (campaign_id, ioc_id),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ioc_id) REFERENCES iocs(ioc_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE complaint_iocs (
    complaint_id INT NOT NULL,
    ioc_id       INT NOT NULL,
    PRIMARY KEY (complaint_id, ioc_id),
    FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ioc_id) REFERENCES iocs(ioc_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE threat_relationships (
    relationship_id   INT AUTO_INCREMENT PRIMARY KEY,
    ioc_id_a          INT NOT NULL,
    ioc_id_b          INT NOT NULL,
    relationship_type VARCHAR(100),
    confidence_level  ENUM('Low','Medium','High') NOT NULL DEFAULT 'Medium',
    FOREIGN KEY (ioc_id_a) REFERENCES iocs(ioc_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ioc_id_b) REFERENCES iocs(ioc_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE threat_analysis_results (
    result_id        INT AUTO_INCREMENT PRIMARY KEY,
    related_case_id  INT NULL,
    analysis_type     VARCHAR(100),
    summary           TEXT,
    generated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (related_case_id) REFERENCES cases(case_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================================================
-- MEMBER 4: INCIDENT RESPONSE, SECURITY OPS & ADMIN
-- =========================================================

CREATE TABLE incidents (
    incident_id        INT AUTO_INCREMENT PRIMARY KEY,
    incident_reference VARCHAR(30) NOT NULL UNIQUE,
    case_id            INT NULL,
    ioc_id             INT NULL,
    responder_id       INT,
    incident_type      VARCHAR(100) NOT NULL,
    description        TEXT,
    severity           ENUM('Low','Medium','High','Critical') NOT NULL DEFAULT 'Low',
    status             ENUM('Detected','Triage','Investigating','Containing','Remediating',
                             'Recovering','Resolved','Closed') NOT NULL DEFAULT 'Detected',
    detected_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (ioc_id) REFERENCES iocs(ioc_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (responder_id) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_incidents_status (status),
    INDEX idx_incidents_severity (severity)
) ENGINE=InnoDB;

CREATE TABLE incident_activities (
    activity_id   INT AUTO_INCREMENT PRIMARY KEY,
    incident_id   INT NOT NULL,
    performed_by  INT,
    action        VARCHAR(255) NOT NULL,
    activity_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (incident_id) REFERENCES incidents(incident_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE response_actions (
    action_id     INT AUTO_INCREMENT PRIMARY KEY,
    incident_id   INT NOT NULL,
    action_type   VARCHAR(100) NOT NULL,
    description   TEXT,
    performed_by  INT,
    performed_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (incident_id) REFERENCES incidents(incident_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE playbooks (
    playbook_id   INT AUTO_INCREMENT PRIMARY KEY,
    playbook_name VARCHAR(150) NOT NULL,
    incident_type VARCHAR(100),
    description   TEXT
) ENGINE=InnoDB;

CREATE TABLE playbook_steps (
    step_id          INT AUTO_INCREMENT PRIMARY KEY,
    playbook_id      INT NOT NULL,
    step_order       INT NOT NULL,
    step_description VARCHAR(255) NOT NULL,
    FOREIGN KEY (playbook_id) REFERENCES playbooks(playbook_id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY uq_playbook_step_order (playbook_id, step_order)
) ENGINE=InnoDB;

CREATE TABLE audit_logs (
    log_id       BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT,
    action       VARCHAR(150) NOT NULL,
    resource     VARCHAR(100),
    resource_id  VARCHAR(50),
    event_time   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address   VARCHAR(45),
    result       ENUM('Success','Failure') NOT NULL DEFAULT 'Success',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_audit_event_time (event_time)
) ENGINE=InnoDB;

CREATE TABLE login_history (
    login_id    BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT,
    event_type  ENUM('Login Success','Login Failed','Logout') NOT NULL,
    event_time  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address  VARCHAR(45),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE system_health (
    health_id      INT AUTO_INCREMENT PRIMARY KEY,
    component_name VARCHAR(100) NOT NULL,
    status         ENUM('Healthy','Warning','Down') NOT NULL DEFAULT 'Healthy',
    checked_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    details        VARCHAR(255)
) ENGINE=InnoDB;
```

---

## 5. Indexing Notes

Beyond the primary/foreign key indexes MySQL creates automatically, explicit secondary indexes are added on high-traffic lookup columns: `complaints.status`, `complaints.tracking_id`, `cases.status`, `iocs.risk_level`, `incidents.status`, `incidents.severity`, `users.email`, and `audit_logs.event_time`. These support the dashboard filters and search functions used across all four sectors without full-table scans.

---

## 6. ON DELETE / ON UPDATE Rules — Rationale

- **CASCADE** is used where a child record has no meaning without its parent (e.g., `evidence` without a `complaint`, `case_assignments` without a `case`). Deleting the parent correctly removes dependent history.
- **RESTRICT** is used where the referenced row represents an accountable actor (e.g., a `user_id` who authored a note or performed an action) — an officer record should not be deletable while investigation notes still attribute work to them.
- **SET NULL** is used where the relationship is informative but optional (e.g., an `incident` may exist without a `case_id`, a `response_action.performed_by` should remain informative even if the acting user account is later removed).
- **ON UPDATE CASCADE** is applied throughout so that if any primary key value is intentionally changed, dependent foreign keys remain consistent automatically.

---

## 7. ENUM Definitions Summary

| Column | Values |
|---|---|
| `users.account_status` | Active, Inactive, Suspended |
| `complaints.status` | Submitted, Under Review, Assigned, Investigation, Action Taken, Resolved, Closed |
| `cases.priority` | Low, Medium, High, Critical |
| `cases.status` | New, Under Review, Assigned, Investigation, Pending External Response, Action Taken, Resolved, Closed |
| `suspects.status` | Person of Interest, Confirmed, Cleared |
| `evidence_access_history.access_type` | View, Download, Analyze |
| `agency_coordination.status` | Pending, Responded, Closed |
| `iocs.ioc_type` | IP, Domain, URL, Hash, Email |
| `iocs.risk_level` / `campaigns.risk_level` | Low, Medium, High, Critical |
| `threat_relationships.confidence_level` | Low, Medium, High |
| `incidents.severity` | Low, Medium, High, Critical |
| `incidents.status` | Detected, Triage, Investigating, Containing, Remediating, Recovering, Resolved, Closed |
| `audit_logs.result` | Success, Failure |
| `login_history.event_type` | Login Success, Login Failed, Logout |
| `system_health.status` | Healthy, Warning, Down |

---

## 8. Suggested Data Types Rationale

- **Identifiers:** `INT AUTO_INCREMENT` for standard-volume tables; `BIGINT AUTO_INCREMENT` for high-write tables (`audit_logs`, `login_history`) that can grow into the millions of rows.
- **Free text:** `VARCHAR(n)` for bounded fields (names, references), `TEXT` for unbounded narrative content (descriptions, notes, summaries).
- **Money:** `DECIMAL(12,2)` for `financial_loss` to avoid floating-point rounding errors.
- **Timestamps:** `DATETIME` with `DEFAULT CURRENT_TIMESTAMP` (and `ON UPDATE CURRENT_TIMESTAMP` where a row is mutable) for consistent, timezone-naive audit trails suitable for an academic deployment.
- **Controlled vocabularies:** `ENUM` for status/severity/priority fields to enforce valid values at the database layer, reducing reliance on application-only validation.

---

## 9. Database Normalization Notes

The schema is designed to **Third Normal Form (3NF)**:

- **1NF:** Every column holds a single atomic value; no repeating groups (e.g., multiple suspects per case are modeled via the `case_suspects` junction table, not a comma-separated column).
- **2NF:** All non-key attributes depend on the whole primary key. Junction tables (`role_permissions`, `case_suspects`, `campaign_iocs`, `complaint_iocs`) use composite keys strictly for the relationship itself, with no partial-key dependent attributes.
- **3NF:** No transitive dependencies — e.g., `complaints` references `complaint_categories` by foreign key rather than repeating the category description inline; `iocs` references `threat_categories` and `threat_sources` rather than duplicating source metadata per indicator.
- **Controlled denormalization:** None is applied in the base schema. If reporting performance becomes a concern during implementation, the team may introduce read-optimized views (e.g., a `case_summary` view joining `cases`, `complaints`, and `users`) rather than denormalizing the base tables themselves.

---

## 10. Entity-Relationship (ER) Diagram — Textual Form

```text
users (1) ───< (M) complaints [via victim_profiles]
users (1) ───< (M) cases [as lead_officer]
users (M) >─── (1) roles
roles (M) ──── (M) permissions   [via role_permissions]

complaints (1) ───< (M) evidence
complaints (1) ───< (M) notifications
complaints (1) ───< (1) cases
complaints (M) ──── (M) iocs   [via complaint_iocs]

cases (1) ───< (M) case_assignments
cases (1) ───< (M) investigation_notes
cases (1) ───< (M) investigation_activities
cases (1) ───< (M) chain_of_custody
cases (1) ───< (M) agency_coordination
cases (M) ──── (M) suspects   [via case_suspects]
cases (0..1) ───< (M) incidents

evidence (1) ───< (M) chain_of_custody
evidence (1) ───< (M) evidence_access_history

iocs (1) ───< (M) malware_indicators
iocs (M) ──── (M) campaigns   [via campaign_iocs]
iocs (M) ──── (M) iocs   [via threat_relationships, self-referencing]
iocs (0..1) ───< (M) incidents

incidents (1) ───< (M) incident_activities
incidents (1) ───< (M) response_actions
playbooks (1) ───< (M) playbook_steps

users (1) ───< (M) audit_logs
users (1) ───< (M) login_history
```

---

## 11. Suggested Folder Structure

```text
project-root/
├── backend/
│   ├── main.py
│   ├── database/
│   │   ├── connection.py
│   │   └── init_schema.sql          ← Section 4 SQL lives here
│   ├── models/
│   │   ├── sector1_victim.py
│   │   ├── sector2_officer.py
│   │   ├── sector3_threat.py
│   │   └── sector4_admin.py
│   ├── schemas/                     ← Pydantic request/response models
│   │   ├── sector1_victim.py
│   │   ├── sector2_officer.py
│   │   ├── sector3_threat.py
│   │   └── sector4_admin.py
│   ├── routers/
│   │   ├── sector1_victim.py
│   │   ├── sector2_officer.py
│   │   ├── sector3_threat.py
│   │   └── sector4_admin.py
│   ├── services/                    ← business logic per sector
│   └── security/                    ← auth, RBAC, hashing, JWT
│
├── frontend/
│   ├── app.py
│   ├── pages/
│   │   ├── victim/
│   │   ├── officer/
│   │   ├── threat_intel/
│   │   └── admin/
│   ├── components/
│   └── services/                    ← API client wrappers
│
├── docs/
│   ├── 01_Victim_Portal_Cybercrime_Complaint_Management.md
│   ├── 02_Officer_Cybercrime_Response_Investigation_Portal.md
│   ├── 03_Threat_Intelligence_Monitoring_Analysis.md
│   ├── 04_Incident_Response_Security_Operations_Administrative_Control.md
│   └── 05_Database_Design_Complete.md
│
└── README.md
```

This structure lets each member work within their own `models/`, `schemas/`, `routers/`, `services/`, and `pages/` files without routinely modifying another member's modules, while all four share the same `database/init_schema.sql` and the same running MySQL instance.
