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
    account_status ENUM('Pending','Active','Inactive','Suspended') NOT NULL DEFAULT 'Active',
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
