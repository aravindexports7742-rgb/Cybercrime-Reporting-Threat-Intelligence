# Cybercrime Reporting & Threat Intelligence Platform

## Four-Member Database Table Assignment

The project has 36 database tables. They are split equally: **9 tables per member**.

| Member | Module | Tables |
|---|---|---|
| Member 1 | Victim Portal and Authentication | `roles`, `permissions`, `role_permissions`, `users`, `victim_profiles`, `complaint_categories`, `complaints`, `evidence`, `notifications` |
| Member 2 | Officer Investigation and Case Management | `cases`, `case_assignments`, `investigation_notes`, `investigation_activities`, `suspects`, `case_suspects`, `chain_of_custody`, `agency_coordination`, `evidence_access_history` |
| Member 3 | Threat Intelligence | `threat_sources`, `threat_feeds`, `threat_categories`, `iocs`, `malware_indicators`, `campaigns`, `campaign_iocs`, `complaint_iocs`, `threat_relationships` |
| Member 4 | Incident Response, Monitoring and Administration | `threat_analysis_results`, `incidents`, `incident_activities`, `response_actions`, `playbooks`, `playbook_steps`, `audit_logs`, `login_history`, `system_health` |

## Member 1: Victim Portal and Authentication

**Main responsibility:** Manage public users, complaint submission, evidence, and victim notifications.

### What to explain

- Victims register and log in to the portal.
- A victim files a complaint with category, incident information, financial loss, and suspicious contact details.
- The victim can upload evidence such as screenshots, PDFs, or transaction records.
- The victim tracks case progress and receives notifications when an officer changes status.
- Internal roles require Administrator approval before accessing the system.

## Member 2: Officer Investigation and Case Management

**Main responsibility:** Investigate complaints after they become cases.

### What to explain

- A complaint automatically creates a linked case for officers.
- The officer assigns priority and moves the case through its workflow.
- Officers record investigation notes, completed actions, outcomes, suspects, and agency coordination.
- Chain of custody protects evidence history and accountability.
- A critical case can be escalated into an incident for the Incident Responder.

### Case workflow

```text
New → Under Review → Assigned → Investigation → Action Taken → Resolved → Closed
```

## Member 3: Threat Intelligence

**Main responsibility:** Identify cybercrime patterns and malicious indicators across reports and threat feeds.

### What to explain

- Analysts manage threat sources and incoming threat feeds.
- They register and search IOCs: IP addresses, URLs, domains, hashes, and malicious emails.
- They connect related IOCs to campaigns and complaints.
- They analyse malware, relationships, and repeated attack patterns.
- Critical IOCs can create an incident for the response team.

## Member 4: Incident Response, Monitoring and Administration

**Main responsibility:** Respond to serious incidents and manage platform security and governance.

### What to explain

- Incident Responders handle escalated cases and critical threat indicators.
- They track response actions, playbooks, containment, remediation, recovery, and closure.
- Administrators approve internal access requests and monitor user activity.
- Audit logs and login history provide accountability.
- System-health records show whether important platform components are healthy.

### Incident workflow

```text
Detected → Triage → Investigating → Containing → Remediating → Recovering → Resolved → Closed
```

## Complete System Flow

```text
Victim files complaint
        ↓
Officer investigates linked case
        ↓
Threat Analyst finds wider attack patterns and malicious indicators
        ↓
Critical case or threat is escalated to an incident
        ↓
Incident Responder contains, remediates, recovers, and closes the incident
        ↓
Administrator monitors access, audit activity, and system health
```
