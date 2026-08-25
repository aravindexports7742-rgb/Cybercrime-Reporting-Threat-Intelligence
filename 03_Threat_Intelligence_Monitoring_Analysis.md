# Sector 3: Threat Intelligence, Monitoring & Analysis

**CYBER CRIME & THREAT INTELLIGENCE PLATFORM — Final Year Project**
**Module Owner:** Team Member 3
**Technology Stack:** FastAPI (Backend) · Streamlit (Frontend) · MySQL (Database)

---

## 1. Sector Overview

The **Threat Intelligence, Monitoring & Analysis** sector is the analytical core of the platform. It collects, normalizes, and correlates cyber threat information with data arising from investigated complaints, allowing the system to move beyond individual case management toward identifying broader cybercrime patterns and coordinated campaigns.

This sector answers questions such as: is a given indicator already known to be malicious; does the same IP or domain reappear across multiple complaints; is there evidence of a coordinated campaign; and which indicators currently represent the greatest risk.

---

## 2. Objectives

1. Ingest and normalize threat intelligence from authorized, legally obtained sources.
2. Maintain a structured, searchable repository of Indicators of Compromise (IOCs).
3. Correlate indicators discovered during investigation (Sector 2) with known threat intelligence.
4. Identify potential relationships between otherwise unconnected complaints.
5. Detect possible coordinated campaigns based on shared indicators or attack patterns.
6. Present threat trends and analytical forecasts to support proactive decision-making.

---

## 3. Member Responsibility

Team Member 3 owns:

- The Streamlit threat intelligence dashboard
- The FastAPI endpoints listed in Section 8
- The database tables listed in Section 9
- Threat feed ingestion, normalization, and deduplication logic
- Correlation and campaign-detection logic
- Coordination with Sector 2 (indicator intake) and Sector 4 (escalation of significant findings)

---

## 4. Functional Modules

### 4.1 Threat Intelligence Sources

The system ingests intelligence from authorized sources only, including threat feeds, malware intelligence, IP/domain/URL reputation feeds, file-hash intelligence, security advisories, and organization-provided intelligence. Any inclusion of dark-web-sourced intelligence must be limited to lawful, controlled, authorized collection used strictly for defensive analysis.

### 4.2 IOC Management

**IOC (Indicator of Compromise)** types supported include IP addresses, domains, URLs, file hashes, email addresses, and malware indicators. Each IOC record captures its type, value, associated threat type, assessed risk level, and source.

### 4.3 Threat Feed Ingestion Pipeline

```text
Threat Source
      │
      ▼
Data Collection
      │
      ▼
Validation
      │
      ▼
Normalization
      │
      ▼
Duplicate Check
      │
      ▼
Store in MySQL
      │
      ▼
Analysis
```

### 4.4 IOC Search

Authorized threat analysts can search for a specific indicator and retrieve its type, risk level, threat category, source, first/last observed timestamps, and any related cases or campaigns.

### 4.5 Complaint–Threat Correlation

```text
Complaint (Sector 2)
      │
      ▼
Suspicious Indicator Extracted
      │
      ▼
Threat Intelligence Lookup
      │
      ▼
Match Against Known Malicious Indicator
      │
      ▼
Related Threat Information Returned to Investigator
```

### 4.6 Cross-Case Correlation & Campaign Detection

The system compares indicators across multiple complaints to surface shared infrastructure:

```text
Complaint A → IP X          ┐
Complaint B → IP X          ├── Common Indicators ──► Possible Relationship ──► Potential Campaign
Complaint C → Domain Y      │
Complaint D → Domain Y      ┘
```

Relationship signals include a shared IP, domain, URL, email address, file hash, or a similar attack pattern or timing. Correlation output is presented as an **analytical finding or risk indicator**, never as automatic proof of criminal responsibility.

### 4.7 Threat Risk Classification

| Risk | Meaning |
|---|---|
| Low | Limited or uncertain threat information |
| Medium | Suspicious or potentially harmful |
| High | Strong malicious indicators |
| Critical | Significant active threat requiring urgent attention |

### 4.8 Threat Trend Analysis & Forecasting

```text
Historical Threat Data → Data Analysis → Trend Identification → Risk Indicators → Possible Emerging Threat
```

Analytical dashboards (built with Pandas/Plotly) surface metrics such as threats by category, high-risk IOC counts, activity over time, most frequently observed indicators, related complaint counts, and campaign activity. Forecasts are presented as analytical projections, not guaranteed outcomes.

---

## 5. Workflow

```text
Sector 1 (Victim Complaint)
        │
        ▼
Sector 2 (Investigation)
        │
        ▼
Indicators Identified
        │
        ▼
Sector 3 (Threat Intelligence)
        │
        ▼
Correlation / Analysis
        │
        ▼
Finding Returned to Investigation (Sector 2)
        │
        ▼
Significant Findings Escalated (Sector 4)
```

---

## 6. Dashboard Design

```text
Threat Intelligence Dashboard
├── Threat Overview
├── IOC Search
├── Threat Feeds
├── High-Risk Indicators
├── Related Cases
├── Campaigns
├── Threat Trends
└── Threat Forecast
```

---

## 7. API Design

```text
POST   /threat-feeds                Ingest a new threat feed batch
GET    /threat-feeds                List configured/ingested threat feeds

POST   /iocs                        Register a new IOC
GET    /iocs                        List IOCs
GET    /iocs/{ioc_id}               Retrieve IOC detail
GET    /iocs/search                 Search for an indicator value

GET    /threats                     List threat records
GET    /threats/{threat_id}         Retrieve threat detail

GET    /campaigns                   List detected campaigns
GET    /campaigns/{campaign_id}     Retrieve campaign detail

GET    /threat-trends               Trend analytics data
GET    /threat-forecast             Forecast analytics data
```

---

## 8. Database Responsibility

| Table | Purpose |
|---|---|
| `threat_sources` | Registered authorized intelligence sources |
| `threat_feeds` | Ingested feed batches |
| `threat_categories` | Lookup table of threat classification types |
| `iocs` | Indicators of Compromise |
| `malware_indicators` | Malware-specific indicator detail |
| `campaigns` | Detected/tracked campaigns |
| `campaign_iocs` | Many-to-many link between campaigns and IOCs |
| `complaint_iocs` | Link between complaints and extracted indicators |
| `threat_relationships` | Relationships identified between indicators/cases |
| `threat_analysis_results` | Stored output of correlation/analysis runs |

---

## 9. Security Considerations

- **Authentication & RBAC:** Threat intelligence functions are restricted to authenticated analyst/administrator roles.
- **Analyst-Only Access:** Raw feed ingestion and IOC management are limited to the Threat Analyst role.
- **Input Validation:** All ingested feed data and search inputs are validated before processing.
- **API Security:** All endpoints require valid JWTs and enforce role checks server-side.
- **Audit Logging:** Feed ingestion, IOC creation, and correlation actions are logged to the shared `audit_logs` table.
- **Source Tracking:** Every IOC retains a reference to its originating source for provenance and trust assessment.
- **Data Integrity:** Duplicate-checking and normalization protect against corrupted or conflicting intelligence records.

---

## 10. Integration with Other Sectors

- **Receives** investigation-derived indicators from **Sector 2** for correlation.
- **Returns** correlation findings and risk assessments back to Sector 2's case records.
- **Escalates** significant findings (e.g., confirmed campaign, critical-risk IOC) to **Sector 4** for incident creation.
- **Shares** the RBAC and audit infrastructure owned by **Sector 4**.

---

## 11. Final Deliverables

1. Streamlit threat intelligence dashboard covering IOC search, feeds, campaigns, trends, and forecasting.
2. FastAPI backend implementing all endpoints listed in Section 7.
3. MySQL tables listed in Section 8, integrated into the shared project database.
4. A working correlation pipeline linking complaint indicators to threat intelligence.
5. A campaign-detection mechanism based on shared indicators.
6. Sector documentation (this file) suitable for inclusion in the final project report.
