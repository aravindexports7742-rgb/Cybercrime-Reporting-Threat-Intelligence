"""
seed_data.py
============
Populates all 36 tables in cyber_threat_platform with ~100 rows of
realistic cybercrime-domain data.  Inserts are done in FK-safe order.
Run:  python seed_data.py
"""

import os, random, hashlib, datetime
from dotenv import load_dotenv
import pymysql
from pymysql.cursors import DictCursor

load_dotenv("d:/Cyber-Threat2/.env")

conn = pymysql.connect(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "cyber_threat_platform"),
    port=int(os.getenv("DB_PORT", 3306)),
    autocommit=False,
    charset="utf8mb4",
)
cur = conn.cursor(DictCursor)

rng = random.Random(42)

def rand_dt(days_back=365):
    base = datetime.datetime.now()
    return base - datetime.timedelta(days=rng.randint(0, days_back),
                                     hours=rng.randint(0, 23),
                                     minutes=rng.randint(0, 59))

def rand_date(days_back=3650):
    base = datetime.date.today()
    return base - datetime.timedelta(days=rng.randint(365, days_back))

def fake_hash():
    return hashlib.sha256(os.urandom(16)).hexdigest()

def fake_ip():
    return f"{rng.randint(1,254)}.{rng.randint(0,254)}.{rng.randint(0,254)}.{rng.randint(1,254)}"

print("=" * 60)
print("  Cyber-Threat Platform - Database Seeder")
print("=" * 60)

# ──────────────────────────────────────────────
# 1. ROLES  (ENUM-constrained, keep existing)
# ──────────────────────────────────────────────
print("\n[1/36] roles ...")
role_names = ['Victim', 'Officer', 'Threat Analyst', 'Incident Responder', 'Administrator']
descs = [
    'Regular citizen reporting cybercrime',
    'Law-enforcement officer investigating cases',
    'Analyst monitoring threat intelligence feeds',
    'Responder handling live security incidents',
    'Platform administrator with full access',
]
for rn, rd in zip(role_names, descs):
    cur.execute("INSERT IGNORE INTO roles (role_name, description) VALUES (%s,%s)", (rn, rd))
conn.commit()
cur.execute("SELECT role_id, role_name FROM roles")
role_map = {r['role_name']: r['role_id'] for r in cur.fetchall()}
print(f"   role_map: {role_map}")

# ──────────────────────────────────────────────
# 2. PERMISSIONS
# ──────────────────────────────────────────────
print("[2/36] permissions ...")
perm_rows = [
    ('view_complaints',    'Read all complaints'),
    ('create_complaint',   'Submit a new complaint'),
    ('edit_complaint',     'Modify an existing complaint'),
    ('delete_complaint',   'Remove a complaint'),
    ('assign_case',        'Assign a case to an officer'),
    ('close_case',         'Mark a case as closed'),
    ('view_evidence',      'View uploaded evidence'),
    ('upload_evidence',    'Upload new evidence files'),
    ('manage_iocs',        'Create/edit IOC entries'),
    ('view_iocs',          'Read IOC data'),
    ('view_threat_feeds',  'Access threat feed data'),
    ('manage_incidents',   'Create and manage incidents'),
    ('view_incidents',     'Read incident details'),
    ('run_playbook',       'Execute a response playbook'),
    ('manage_users',       'Create and edit users'),
    ('view_audit_logs',    'Access system audit logs'),
    ('manage_roles',       'Assign roles to users'),
    ('view_reports',       'View generated reports'),
    ('export_data',        'Export platform data'),
    ('system_config',      'Modify platform configuration'),
    ('manage_campaigns',   'Handle threat campaigns'),
    ('view_campaigns',     'Read campaign data'),
    ('manage_playbooks',   'Create and edit playbooks'),
    ('coordinate_agency',  'Communicate with external agencies'),
    ('view_suspects',      'Read suspect profiles'),
    ('manage_suspects',    'Create/edit suspect records'),
    ('view_analytics',     'Access analytical dashboards'),
    ('manage_notifications','Send/manage notifications'),
    ('view_login_history', 'Read login history logs'),
    ('system_health_check','Check system component health'),
]
for pn, pd in perm_rows:
    cur.execute("INSERT IGNORE INTO permissions (permission_name, description) VALUES (%s,%s)", (pn, pd))
conn.commit()
cur.execute("SELECT permission_id FROM permissions")
perm_ids = [r['permission_id'] for r in cur.fetchall()]
print(f"   {len(perm_ids)} permissions ready")

# ──────────────────────────────────────────────
# 3. ROLE_PERMISSIONS
# ──────────────────────────────────────────────
print("[3/36] role_permissions ...")
cur.execute("SELECT role_id FROM roles")
all_role_ids = [r['role_id'] for r in cur.fetchall()]
rp_inserted = 0
for rid in all_role_ids:
    chosen = rng.sample(perm_ids, k=min(len(perm_ids), rng.randint(8, 20)))
    for pid in chosen:
        try:
            cur.execute("INSERT IGNORE INTO role_permissions (role_id,permission_id) VALUES (%s,%s)", (rid, pid))
            rp_inserted += 1
        except Exception:
            pass
conn.commit()
print(f"   {rp_inserted} role-permission pairs inserted")

# ──────────────────────────────────────────────
# 4. USERS
# ──────────────────────────────────────────────
print("[4/36] users ...")
first_names = ['Arjun','Priya','Ravi','Kavya','Suresh','Deepa','Vijay','Sneha','Arun','Meera',
               'Kiran','Lakshmi','Mohan','Nisha','Prasad','Rekha','Sanjay','Tanya','Uday','Vani',
               'Ajay','Bhavna','Chetan','Divya','Eshan','Falak','Ganesh','Hema','Ishaan','Jaya',
               'Kabir','Lavanya','Madan','Nalini','Omkar','Pooja','Qadir','Radha','Sahil','Trisha']
last_names  = ['Kumar','Sharma','Reddy','Singh','Nair','Patel','Iyer','Menon','Rao','Verma',
               'Gupta','Joshi','Das','Pillai','Bose','Chauhan','Desai','Fernandes','Gaikwad','Hegde',
               'Iyengar','Jain','Khanna','Lal','Malhotra','Naidu','Oberoi','Pandey','Qureshi','Rastogi']
statuses = ['Active','Active','Active','Active','Inactive','Suspended']

existing_emails = set()
cur.execute("SELECT email FROM users")
for r in cur.fetchall():
    existing_emails.add(r['email'])

pw_hash = hashlib.sha256(b"Password@123").hexdigest()
user_ids_by_role = {rid: [] for rid in all_role_ids}

cur.execute("SELECT user_id, role_id FROM users")
for row in cur.fetchall():
    user_ids_by_role[row['role_id']].append(row['user_id'])

target_users = 100
cur.execute("SELECT COUNT(*) as c FROM users")
existing_count = cur.fetchone()['c']
to_insert = max(0, target_users - existing_count)
print(f"   existing={existing_count}, inserting {to_insert} more users ...")

inserted_users = 0
attempts = 0
while inserted_users < to_insert and attempts < 500:
    attempts += 1
    fn = rng.choice(first_names)
    ln = rng.choice(last_names)
    full = f"{fn} {ln}"
    email = f"{fn.lower()}.{ln.lower()}{rng.randint(1,999)}@example.com"
    if email in existing_emails:
        continue
    phone = f"+91{rng.randint(7000000000, 9999999999)}"
    rid = rng.choice(all_role_ids)
    status = rng.choice(statuses)
    cur.execute(
        "INSERT INTO users (full_name,email,phone_number,password_hash,role_id,account_status) "
        "VALUES (%s,%s,%s,%s,%s,%s)",
        (full, email, phone, pw_hash, rid, status)
    )
    uid = cur.lastrowid
    existing_emails.add(email)
    user_ids_by_role[rid].append(uid)
    inserted_users += 1

conn.commit()
cur.execute("SELECT user_id, role_id FROM users")
all_users = cur.fetchall()
user_ids = [u['user_id'] for u in all_users]
for u in all_users:
    if u['user_id'] not in user_ids_by_role.get(u['role_id'], []):
        user_ids_by_role[u['role_id']].append(u['user_id'])
# deduplicate
for rid in user_ids_by_role:
    user_ids_by_role[rid] = list(set(user_ids_by_role[rid]))

officer_ids   = user_ids_by_role.get(role_map['Officer'], []) or user_ids
analyst_ids   = user_ids_by_role.get(role_map['Threat Analyst'], []) or user_ids
responder_ids = user_ids_by_role.get(role_map['Incident Responder'], []) or user_ids
victim_user_ids = user_ids_by_role.get(role_map['Victim'], []) or user_ids
print(f"   total users: {len(user_ids)}")

# ──────────────────────────────────────────────
# 5. VICTIM_PROFILES
# ──────────────────────────────────────────────
print("[5/36] victim_profiles ...")
cur.execute("SELECT user_id FROM victim_profiles")
existing_vp = {r['user_id'] for r in cur.fetchall()}

areas = ['MG Road','Park Street','Anna Nagar','Banjara Hills','Koramangala',
         'Connaught Place','Jubilee Hills','Salt Lake','Powai','Whitefield']

for uid in victim_user_ids:
    if uid in existing_vp:
        continue
    addr = f"{rng.randint(1,999)}, {rng.choice(areas)}, India"
    dob  = rand_date(16000)
    idr  = f"AADHAR{rng.randint(100000000000,999999999999)}"
    cur.execute("INSERT IGNORE INTO victim_profiles (user_id,address,date_of_birth,id_document_reference) VALUES (%s,%s,%s,%s)",
                (uid, addr, dob, idr))
    existing_vp.add(uid)
conn.commit()

# Top up to 100 total victim profiles using remaining users
cur.execute("SELECT user_id FROM victim_profiles")
current_vps = {r['user_id'] for r in cur.fetchall()}
extra_users = [u for u in user_ids if u not in current_vps]
rng.shuffle(extra_users)
needed = max(0, 100 - len(current_vps))
for uid in extra_users[:needed]:
    addr = f"{rng.randint(1,999)}, {rng.choice(areas)}, India"
    dob  = rand_date(16000)
    idr  = f"AADHAR{rng.randint(100000000000,999999999999)}"
    cur.execute("INSERT IGNORE INTO victim_profiles (user_id,address,date_of_birth,id_document_reference) VALUES (%s,%s,%s,%s)",
                (uid, addr, dob, idr))
conn.commit()
cur.execute("SELECT victim_id, user_id FROM victim_profiles")
victim_profiles = cur.fetchall()
victim_ids = [v['victim_id'] for v in victim_profiles]
print(f"   {len(victim_ids)} victim profiles total")

# ──────────────────────────────────────────────
# 6. COMPLAINT_CATEGORIES
# ──────────────────────────────────────────────
print("[6/36] complaint_categories ...")
cat_data = [
    ('Phishing','Fraudulent attempts to obtain sensitive information'),
    ('Ransomware','Malicious software encrypting victim data for ransom'),
    ('Online Fraud','Financial fraud conducted over the internet'),
    ('Identity Theft','Unauthorized use of another person identity'),
    ('Cyberbullying','Harassment and bullying through digital channels'),
    ('Data Breach','Unauthorized access to confidential data'),
    ('Hacking','Unauthorized intrusion into computer systems'),
    ('Malware','Malicious software infection on devices'),
    ('Vishing','Voice phishing via phone calls'),
    ('Smishing','SMS-based phishing attacks'),
    ('Credit Card Fraud','Unauthorized use of credit/debit card information'),
    ('Dark Web Activity','Illegal activities on dark web marketplaces'),
    ('Social Engineering','Psychological manipulation to gain access'),
    ('Crypto Fraud','Cryptocurrency-based scams and theft'),
    ('SIM Swapping','Illegitimate transfer of phone number to attacker SIM'),
    ('Business Email Compromise','Email fraud targeting business organizations'),
    ('Child Safety Online','Online exploitation or harm of minors'),
    ('IP Theft','Theft of patents, trade secrets, or copyrighted content'),
    ('Sextortion','Blackmail using intimate images'),
    ('DoS/DDoS Attack','Denial of service attack on systems or networks'),
]
for cn, cd in cat_data:
    cur.execute("INSERT IGNORE INTO complaint_categories (category_name,description) VALUES (%s,%s)", (cn, cd))
conn.commit()
cur.execute("SELECT category_id FROM complaint_categories")
cat_ids = [r['category_id'] for r in cur.fetchall()]
print(f"   {len(cat_ids)} categories ready")

# ──────────────────────────────────────────────
# 7. COMPLAINTS
# ──────────────────────────────────────────────
print("[7/36] complaints ...")
complaint_titles = [
    'Received fake bank SMS asking for OTP',
    'Unknown person used my Aadhaar to take loan',
    'Lost money in fake investment app',
    'Received threatening call demanding ransom',
    'My email account was hacked',
    'Fake job offer led to financial loss',
    'Received nude images of self being shared online',
    'Cryptocurrency wallet drained overnight',
    'Company server hit by ransomware',
    'Someone stole credit card details at ATM',
    'Phishing email impersonating HDFC Bank',
    'Unknown device logged into my Netflix account',
    'Online shopping fraud on fake e-commerce site',
    'UPI fraud - money debited without my consent',
    'Received morphed images used for blackmail',
]
complaint_statuses = ['Submitted','Under Review','Assigned','Investigation','Action Taken','Resolved','Closed']

cur.execute("SELECT COUNT(*) as c FROM complaints")
existing_complaints = cur.fetchone()['c']
to_insert_c = max(0, 100 - existing_complaints)
complaint_ids_new = []
for i in range(to_insert_c):
    vid  = rng.choice(victim_ids)
    cid  = rng.choice(cat_ids)
    tid  = f"TRK{rng.randint(1000000000,9999999999)}"
    title = rng.choice(complaint_titles) + f" #{rng.randint(100,999)}"
    inc_date = rand_date(365)
    desc = (f"The victim reported a cybercrime incident. "
            f"Financial loss estimated at INR {rng.randint(1000,500000)}. "
            f"Incident occurred on {inc_date}. Additional details are under investigation.")
    loss = round(rng.uniform(0, 500000), 2)
    sus_url   = rng.choice([None, f"http://fake-site-{rng.randint(100,999)}.com", f"https://phish{rng.randint(10,99)}.net"])
    sus_phone = rng.choice([None, f"+91{rng.randint(7000000000,9999999999)}"])
    sus_email = rng.choice([None, f"scammer{rng.randint(1,999)}@tempmail.com"])
    status    = rng.choice(complaint_statuses)
    try:
        cur.execute(
            "INSERT INTO complaints (tracking_id,victim_id,category_id,title,incident_date,"
            "description,financial_loss,suspected_url,suspected_phone,suspected_email,status) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (tid,vid,cid,title,inc_date,desc,loss,sus_url,sus_phone,sus_email,status)
        )
        complaint_ids_new.append(cur.lastrowid)
    except Exception:
        pass
conn.commit()
cur.execute("SELECT complaint_id FROM complaints")
complaint_ids = [r['complaint_id'] for r in cur.fetchall()]
print(f"   {len(complaint_ids)} complaints total")

# ──────────────────────────────────────────────
# 8. EVIDENCE
# ──────────────────────────────────────────────
print("[8/36] evidence ...")
ev_types = ['Screenshot','PDF Document','Email Header','Log File','Image','Video','Audio','Binary','Network Capture']
ev_statuses = ['Active','Under Review','Archived']
for _ in range(100):
    cid = rng.choice(complaint_ids)
    uid = rng.choice(user_ids)
    fname = f"evidence_{rng.randint(10000,99999)}.{rng.choice(['jpg','pdf','log','pcap','mp4'])}"
    cur.execute(
        "INSERT INTO evidence (complaint_id,uploaded_by,file_name,evidence_type,file_hash,status) "
        "VALUES (%s,%s,%s,%s,%s,%s)",
        (cid, uid, fname, rng.choice(ev_types), fake_hash(), rng.choice(ev_statuses))
    )
conn.commit()
cur.execute("SELECT evidence_id FROM evidence")
evidence_ids = [r['evidence_id'] for r in cur.fetchall()]
print(f"   {len(evidence_ids)} evidence records")

# ──────────────────────────────────────────────
# 9. NOTIFICATIONS
# ──────────────────────────────────────────────
print("[9/36] notifications ...")
event_types = ['complaint_submitted','status_update','case_assigned','evidence_uploaded','reminder']
messages = [
    'Your complaint has been received and is under review.',
    'Status updated: Your case is now under investigation.',
    'An officer has been assigned to your complaint.',
    'New evidence has been uploaded to your case.',
    'Action taken: Suspects have been identified.',
    'Your complaint has been resolved. Please review the outcome.',
    'Reminder: Please provide additional information for your case.',
    'Your account has been verified successfully.',
    'A new notification regarding your cybercrime complaint.',
    'Your complaint status has changed to Closed.',
]
for _ in range(100):
    uid = rng.choice(user_ids)
    cid = rng.choice([None] + complaint_ids[:50])
    cur.execute(
        "INSERT INTO notifications (user_id,complaint_id,message,event_type,is_read) "
        "VALUES (%s,%s,%s,%s,%s)",
        (uid, cid, rng.choice(messages), rng.choice(event_types), rng.choice([0,0,1]))
    )
conn.commit()
print("   100 notifications inserted")

# ──────────────────────────────────────────────
# 10. CASES
# ──────────────────────────────────────────────
print("[10/36] cases ...")
case_statuses  = ['New','Under Review','Assigned','Investigation','Pending External Response','Action Taken','Resolved','Closed']
case_priorities= ['Low','Medium','High','Critical']
for i in range(100):
    comp_id  = rng.choice(complaint_ids)
    officer  = rng.choice(officer_ids) if officer_ids else rng.choice(user_ids)
    ref      = f"CASE{rng.randint(10000000,99999999)}"
    priority = rng.choice(case_priorities)
    status   = rng.choice(case_statuses)
    opened   = rand_dt(300)
    closed   = (opened + datetime.timedelta(days=rng.randint(1,60))) if status in ('Resolved','Closed') else None
    try:
        cur.execute(
            "INSERT INTO cases (case_reference,complaint_id,lead_officer_id,priority,status,opened_at,closed_at) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (ref, comp_id, officer, priority, status, opened, closed)
        )
    except Exception:
        pass
conn.commit()
cur.execute("SELECT case_id FROM cases")
case_ids = [r['case_id'] for r in cur.fetchall()]
print(f"   {len(case_ids)} cases total")

# ──────────────────────────────────────────────
# 11. CASE_ASSIGNMENTS
# ──────────────────────────────────────────────
print("[11/36] case_assignments ...")
for _ in range(100):
    cid      = rng.choice(case_ids)
    officer  = rng.choice(officer_ids) if officer_ids else rng.choice(user_ids)
    assigner = rng.choice(user_ids)
    assigned = rand_dt(200)
    unassign = (assigned + datetime.timedelta(days=rng.randint(1,30))) if rng.random() < 0.3 else None
    cur.execute(
        "INSERT INTO case_assignments (case_id,officer_id,assigned_by,assigned_at,unassigned_at) "
        "VALUES (%s,%s,%s,%s,%s)",
        (cid, officer, assigner, assigned, unassign)
    )
conn.commit()
print("   100 case_assignments inserted")

# ──────────────────────────────────────────────
# 12. INVESTIGATION_NOTES
# ──────────────────────────────────────────────
print("[12/36] investigation_notes ...")
note_texts = [
    'Initial review of the complaint shows credible evidence of phishing activity.',
    'Contacted the victim for additional information regarding the incident.',
    'Performed OSINT on the suspected domain; found it registered 3 days before the attack.',
    'Coordinated with ISP to obtain IP logs for the suspect IP address.',
    'Evidence of financial transaction traced to a mule account.',
    'Victim identified the suspect from CCTV footage at the ATM.',
    'Malware sample extracted from victim device and sent for forensic analysis.',
    'Search warrant obtained; proceeding with digital forensics on confiscated devices.',
    'Interview with witness corroborates victim account of events.',
    'Suspect bank account frozen pending further investigation.',
    'Technical analysis confirms SIM swap attack vector.',
    'Dark web monitoring flagged victim credentials in a paste site.',
    'Victim employer contacted for corporate network logs.',
    'Case escalated to cyber cell headquarters for further action.',
    'Ransom payment traced through blockchain analytics tool.',
]
for _ in range(100):
    cid     = rng.choice(case_ids)
    officer = rng.choice(officer_ids) if officer_ids else rng.choice(user_ids)
    cur.execute(
        "INSERT INTO investigation_notes (case_id,officer_id,note_text,created_at) VALUES (%s,%s,%s,%s)",
        (cid, officer, rng.choice(note_texts) + f" [Note #{rng.randint(1000,9999)}]", rand_dt(180))
    )
conn.commit()
print("   100 investigation_notes inserted")

# ──────────────────────────────────────────────
# 13. INVESTIGATION_ACTIVITIES
# ──────────────────────────────────────────────
print("[13/36] investigation_activities ...")
actions  = ['OSINT Research','Victim Interview','Suspect Surveillance','Digital Forensics','Network Log Analysis',
            'Warrant Obtained','Suspect Arrested','Evidence Collected','ISP Contacted','Social Media Monitoring',
            'Financial Trace','Witness Statement','Search Warrant Executed','Device Seized','Forensic Report Filed']
results  = ['Positive lead found','No new information','Evidence secured','Suspect identified',
            'Lead inconclusive','Forwarded to legal team','Pending response','Completed successfully','Under review']
for _ in range(100):
    cid     = rng.choice(case_ids)
    officer = rng.choice(officer_ids) if officer_ids else rng.choice(user_ids)
    cur.execute(
        "INSERT INTO investigation_activities (case_id,officer_id,action,result,activity_date) "
        "VALUES (%s,%s,%s,%s,%s)",
        (cid, officer, rng.choice(actions), rng.choice(results), rand_dt(200))
    )
conn.commit()
print("   100 investigation_activities inserted")

# ──────────────────────────────────────────────
# 14. SUSPECTS
# ──────────────────────────────────────────────
print("[14/36] suspects ...")
suspect_aliases = ['CyberGhost','PhishKing','DarkHorse','ShadowHacker','CryptoThief','RansomBot','SkimmerPro',
                   'VoicePhisher','SMSBomber','FakeJobster','IdentityCloner','DataLeaker','BotnetMaster',
                   'SIMSwapper','CardCracker','DarkWebDealer','MalwareAuthor','ScammerX','PhantomNet','ZeroDay']
sus_statuses = ['Person of Interest','Confirmed','Cleared']
for i in range(100):
    alias   = rng.choice(suspect_aliases) + str(rng.randint(10,99))
    contact = rng.choice([
        f"+91{rng.randint(7000000000,9999999999)}",
        f"suspect{rng.randint(1,999)}@darkmail.example",
        f"TG: @{alias.lower()}",
        None
    ])
    notes = (f"Linked to {rng.randint(1,5)} prior cybercrime cases. "
             f"Operates primarily via {rng.choice(['Telegram','Dark Web','WhatsApp','Email','Phone'])}. "
             f"Last known location: {rng.choice(['Mumbai','Delhi','Bengaluru','Hyderabad','Unknown'])}.")
    cur.execute(
        "INSERT INTO suspects (name_alias,contact_info,status,notes) VALUES (%s,%s,%s,%s)",
        (alias, contact, rng.choice(sus_statuses), notes)
    )
conn.commit()
cur.execute("SELECT suspect_id FROM suspects")
suspect_ids = [r['suspect_id'] for r in cur.fetchall()]
print(f"   {len(suspect_ids)} suspects inserted")

# ──────────────────────────────────────────────
# 15. CASE_SUSPECTS
# ──────────────────────────────────────────────
print("[15/36] case_suspects ...")
cs_pairs = set()
attempts = 0
while len(cs_pairs) < 100 and attempts < 500:
    attempts += 1
    pair = (rng.choice(case_ids), rng.choice(suspect_ids))
    if pair not in cs_pairs:
        try:
            cur.execute("INSERT IGNORE INTO case_suspects (case_id,suspect_id) VALUES (%s,%s)", pair)
            cs_pairs.add(pair)
        except Exception:
            pass
conn.commit()
print(f"   {len(cs_pairs)} case_suspect links inserted")

# ──────────────────────────────────────────────
# 16. CHAIN_OF_CUSTODY
# ──────────────────────────────────────────────
print("[16/36] chain_of_custody ...")
coc_actions = ['Received','Transferred','Analyzed','Archived','Returned','Destroyed','Digitized']
for _ in range(100):
    ev_id   = rng.choice(evidence_ids)
    ca_id   = rng.choice(case_ids)
    uid     = rng.choice(user_ids)
    action  = rng.choice(coc_actions)
    notes   = f"Evidence {action.lower()} by user {uid} as part of case processing."
    cur.execute(
        "INSERT INTO chain_of_custody (evidence_id,case_id,user_id,action,event_time,notes) "
        "VALUES (%s,%s,%s,%s,%s,%s)",
        (ev_id, ca_id, uid, action, rand_dt(200), notes)
    )
conn.commit()
print("   100 chain_of_custody records inserted")

# ──────────────────────────────────────────────
# 17. EVIDENCE_ACCESS_HISTORY
# ──────────────────────────────────────────────
print("[17/36] evidence_access_history ...")
access_types = ['View','Download','Analyze']
for _ in range(100):
    ev_id = rng.choice(evidence_ids)
    uid   = rng.choice(user_ids)
    cur.execute(
        "INSERT INTO evidence_access_history (evidence_id,user_id,access_time,access_type) VALUES (%s,%s,%s,%s)",
        (ev_id, uid, rand_dt(180), rng.choice(access_types))
    )
conn.commit()
print("   100 evidence_access_history records inserted")

# ──────────────────────────────────────────────
# 18. AGENCY_COORDINATION
# ──────────────────────────────────────────────
print("[18/36] agency_coordination ...")
orgs = ['CERT-In','Interpol','CBI Cyber Cell','State Cyber Police','RBI Fraud Desk','SEBI','NCPCR',
        'Income Tax Dept Cyber Wing','NIA','I4C',
        'TRAI','MHA Cyber Division','Google Trust and Safety','Meta Law Enforcement','Microsoft DCCU']
req_types = ['Log Request','Account Freeze','IP Attribution','Mutual Legal Assistance','Asset Recovery',
             'Evidence Request','Witness Cooperation','Jurisdiction Transfer','Technical Assistance','Advisory']
coord_statuses = ['Pending','Responded','Closed']
for _ in range(100):
    ca_id   = rng.choice(case_ids)
    officer = rng.choice(officer_ids) if officer_ids else rng.choice(user_ids)
    org     = rng.choice(orgs)
    status  = rng.choice(coord_statuses)
    resp    = f"Response received from {org}: {rng.choice(['Approved','Under processing','Forwarded','No record found','Partial data provided'])}." if status != 'Pending' else None
    cur.execute(
        "INSERT INTO agency_coordination (case_id,officer_id,organization_name,request_type,request_date,status,response) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (ca_id, officer, org, rng.choice(req_types), rand_dt(180), status, resp)
    )
conn.commit()
print("   100 agency_coordination records inserted")

# ──────────────────────────────────────────────
# 19. THREAT_SOURCES
# ──────────────────────────────────────────────
print("[19/36] threat_sources ...")
ts_data = [
    ('CERT-In Daily Feed',       'Government Feed',     'High'),
    ('AlienVault OTX',           'Open Source Feed',    'High'),
    ('Shodan Exposure Monitor',  'Scan Feed',           'Medium'),
    ('VirusTotal API',           'Commercial Feed',     'High'),
    ('Abuse.ch MalwareBazaar',   'Open Source Feed',    'High'),
    ('SpamHaus',                 'Email Reputation',    'High'),
    ('PhishTank',                'Phishing Feed',       'High'),
    ('ThreatConnect',            'Commercial Feed',     'Medium'),
    ('Mandiant Threat Intel',    'Commercial Feed',     'High'),
    ('CrowdStrike Falcon Intel', 'Commercial Feed',     'High'),
    ('Recorded Future',          'Commercial Feed',     'High'),
    ('IBM X-Force Exchange',     'Commercial Feed',     'Medium'),
    ('US-CERT Alerts',           'Government Feed',     'High'),
    ('ShadowServer',             'Nonprofit Feed',      'Medium'),
    ('DarkOwl Vision',           'Dark Web Monitor',    'Medium'),
    ('Kaspersky TIP',            'Commercial Feed',     'High'),
    ('Palo Alto Unit42',         'Commercial Feed',     'High'),
    ('Check Point Research',     'Commercial Feed',     'Medium'),
    ('Anomali STIX/TAXII',       'STIX/TAXII Feed',     'Medium'),
    ('Internal Honeypot Logs',   'Internal Sensor',     'Medium'),
]
for sn, st, sr in ts_data:
    cur.execute("INSERT IGNORE INTO threat_sources (source_name,source_type,reliability_rating) VALUES (%s,%s,%s)", (sn, st, sr))
for i in range(80):
    sn = f"ThreatSource_{i+1:04d}"
    st = rng.choice(['Open Source Feed','Commercial Feed','Government Feed','Dark Web Monitor','Internal Sensor'])
    sr = rng.choice(['Low','Medium','High'])
    cur.execute("INSERT IGNORE INTO threat_sources (source_name,source_type,reliability_rating) VALUES (%s,%s,%s)", (sn, st, sr))
conn.commit()
cur.execute("SELECT source_id FROM threat_sources")
source_ids = [r['source_id'] for r in cur.fetchall()]
print(f"   {len(source_ids)} threat_sources ready")

# ──────────────────────────────────────────────
# 20. THREAT_FEEDS
# ──────────────────────────────────────────────
print("[20/36] threat_feeds ...")
feed_statuses = ['Success','Partial','Failed']
for _ in range(100):
    sid = rng.choice(source_ids)
    cur.execute(
        "INSERT INTO threat_feeds (source_id,ingested_at,record_count,status) VALUES (%s,%s,%s,%s)",
        (sid, rand_dt(180), rng.randint(50,5000), rng.choice(feed_statuses))
    )
conn.commit()
print("   100 threat_feeds inserted")

# ──────────────────────────────────────────────
# 21. THREAT_CATEGORIES
# ──────────────────────────────────────────────
print("[21/36] threat_categories ...")
tc_data = [
    ('Phishing',        'Credential harvesting via fake sites or emails'),
    ('Ransomware',      'Malware encrypting data and demanding ransom'),
    ('APT',             'Advanced Persistent Threat actor activity'),
    ('Botnet',          'Network of compromised machines'),
    ('Credential Theft','Stealing login credentials'),
    ('Data Exfiltration','Unauthorized data transfer out of network'),
    ('Exploit Kit',     'Automated exploitation framework'),
    ('Keylogger',       'Software capturing keystrokes'),
    ('Rootkit',         'Stealthy malware achieving persistent access'),
    ('Spyware',         'Software covertly monitoring user activity'),
    ('Trojan',          'Malware disguised as legitimate software'),
    ('Worm',            'Self-replicating malware spreading via networks'),
    ('Zero Day',        'Exploitation of previously unknown vulnerability'),
    ('Supply Chain',    'Attack via compromised third-party software'),
    ('Insider Threat',  'Malicious activity from within the organization'),
    ('DDoS',            'Distributed Denial of Service attack'),
    ('SQL Injection',   'Database attack via malicious SQL queries'),
    ('Cross-Site Scripting','XSS vulnerability exploitation'),
    ('Man in the Middle','Intercepting communications between two parties'),
    ('Cryptojacking',   'Unauthorized use of computing resources for mining'),
]
for cn, cd in tc_data:
    cur.execute("INSERT IGNORE INTO threat_categories (category_name,description) VALUES (%s,%s)", (cn, cd))
conn.commit()
cur.execute("SELECT category_id FROM threat_categories")
tc_ids = [r['category_id'] for r in cur.fetchall()]
print(f"   {len(tc_ids)} threat_categories ready")

# ──────────────────────────────────────────────
# 22. IOCS
# ──────────────────────────────────────────────
print("[22/36] iocs ...")
ioc_types = ['IP','Domain','URL','Hash','Email']
risk_levels = ['Low','Medium','High','Critical']
ioc_values_set = set()

def gen_ioc_value(ioc_type):
    if ioc_type == 'IP':
        return fake_ip()
    elif ioc_type == 'Domain':
        words = ['evil','phish','dark','hack','malware','ransom','crypto','scam','fake','threat']
        return f"{rng.choice(words)}{rng.randint(1,9999)}.{rng.choice(['com','net','xyz','top','online'])}"
    elif ioc_type == 'URL':
        base = gen_ioc_value('Domain')
        return f"http://{base}/{''.join(rng.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=12))}"
    elif ioc_type == 'Hash':
        return fake_hash()[:32]
    else:
        return f"attacker{rng.randint(1,99999)}@{rng.choice(['tempmail.com','disposable.io','guerrillamail.com','mailnull.com'])}"

for _ in range(100):
    itype = rng.choice(ioc_types)
    for attempt2 in range(20):
        val = gen_ioc_value(itype)
        key = (itype, val)
        if key not in ioc_values_set:
            ioc_values_set.add(key)
            cat_id = rng.choice(tc_ids + [None])
            src_id = rng.choice(source_ids + [None])
            try:
                cur.execute(
                    "INSERT IGNORE INTO iocs (ioc_type,ioc_value,category_id,source_id,risk_level) "
                    "VALUES (%s,%s,%s,%s,%s)",
                    (itype, val, cat_id, src_id, rng.choice(risk_levels))
                )
            except Exception:
                pass
            break
conn.commit()
cur.execute("SELECT ioc_id FROM iocs")
ioc_ids = [r['ioc_id'] for r in cur.fetchall()]
print(f"   {len(ioc_ids)} IOCs inserted")

# ──────────────────────────────────────────────
# 23. MALWARE_INDICATORS
# ──────────────────────────────────────────────
print("[23/36] malware_indicators ...")
malware_families = ['LockBit','Emotet','TrickBot','Ryuk','Conti','BlackMatter','REvil','Cerber',
                    'WannaCry','NotPetya','Lazarus','DarkSide','Maze','NetWalker','Dharma',
                    'Ragnar Locker','Egregor','Cl0p','Hive','BlackCat']
cur.execute("SELECT ioc_id FROM iocs WHERE ioc_type='Hash'")
hash_ioc_ids = [r['ioc_id'] for r in cur.fetchall()]
if not hash_ioc_ids:
    hash_ioc_ids = ioc_ids

for _ in range(100):
    iid   = rng.choice(hash_ioc_ids)
    fam   = rng.choice(malware_families)
    sig   = f"SIG-{fam.upper().replace(' ','')}-{rng.randint(1000,9999)}"
    desc  = f"{fam} malware variant. Uses {rng.choice(['AES-256','RSA-2048','ChaCha20'])} encryption."
    cur.execute(
        "INSERT INTO malware_indicators (ioc_id,malware_family,signature,description) VALUES (%s,%s,%s,%s)",
        (iid, fam, sig, desc)
    )
conn.commit()
print("   100 malware_indicators inserted")

# ──────────────────────────────────────────────
# 24. CAMPAIGNS
# ──────────────────────────────────────────────
print("[24/36] campaigns ...")
campaign_names = ['Operation Shadow Storm','PhishWave 2025','CryptoHarvest','BankBot Surge',
                  'Operation Dark Net','SIM Swap Blitz','Ransomwave Alpha','IdentityFlood',
                  'Operation CyberBazaar','DataDrain 2024','VoicePhish Campaign','Operation Zero Trust',
                  'MalSpam Blizzard','Operation Ghost Protocol','SextortionNet']
for i in range(100):
    name    = rng.choice(campaign_names) + f" v{rng.randint(1,9)}.{rng.randint(0,9)}"
    desc    = f"Threat campaign targeting {rng.choice(['banking sector','government portals','e-commerce platforms','crypto exchanges','individual users'])}."
    rl      = rng.choice(risk_levels)
    det_at  = rand_dt(365)
    cur.execute(
        "INSERT INTO campaigns (campaign_name,description,risk_level,detected_at) VALUES (%s,%s,%s,%s)",
        (name, desc, rl, det_at)
    )
conn.commit()
cur.execute("SELECT campaign_id FROM campaigns")
campaign_ids = [r['campaign_id'] for r in cur.fetchall()]
print(f"   {len(campaign_ids)} campaigns inserted")

# ──────────────────────────────────────────────
# 25. CAMPAIGN_IOCS
# ──────────────────────────────────────────────
print("[25/36] campaign_iocs ...")
ci_pairs = set()
attempts = 0
while len(ci_pairs) < 100 and attempts < 500:
    attempts += 1
    pair = (rng.choice(campaign_ids), rng.choice(ioc_ids))
    if pair not in ci_pairs:
        try:
            cur.execute("INSERT IGNORE INTO campaign_iocs (campaign_id,ioc_id) VALUES (%s,%s)", pair)
            ci_pairs.add(pair)
        except Exception:
            pass
conn.commit()
print(f"   {len(ci_pairs)} campaign_ioc links inserted")

# ──────────────────────────────────────────────
# 26. COMPLAINT_IOCS
# ──────────────────────────────────────────────
print("[26/36] complaint_iocs ...")
comp_ioc_pairs = set()
attempts = 0
while len(comp_ioc_pairs) < 100 and attempts < 500:
    attempts += 1
    pair = (rng.choice(complaint_ids), rng.choice(ioc_ids))
    if pair not in comp_ioc_pairs:
        try:
            cur.execute("INSERT IGNORE INTO complaint_iocs (complaint_id,ioc_id) VALUES (%s,%s)", pair)
            comp_ioc_pairs.add(pair)
        except Exception:
            pass
conn.commit()
print(f"   {len(comp_ioc_pairs)} complaint_ioc links inserted")

# ──────────────────────────────────────────────
# 27. THREAT_RELATIONSHIPS
# ──────────────────────────────────────────────
print("[27/36] threat_relationships ...")
rel_types = ['resolves_to','communicates_with','hosted_on','drops','associated_with',
             'redirects_to','belongs_to','c2_for','observed_with','linked_campaign']
conf_levels = ['Low','Medium','High']
for _ in range(100):
    ioc_a = rng.choice(ioc_ids)
    ioc_b = rng.choice(ioc_ids)
    if ioc_a != ioc_b:
        cur.execute(
            "INSERT INTO threat_relationships (ioc_id_a,ioc_id_b,relationship_type,confidence_level) "
            "VALUES (%s,%s,%s,%s)",
            (ioc_a, ioc_b, rng.choice(rel_types), rng.choice(conf_levels))
        )
conn.commit()
print("   ~100 threat_relationships inserted")

# ──────────────────────────────────────────────
# 28. THREAT_ANALYSIS_RESULTS
# ──────────────────────────────────────────────
print("[28/36] threat_analysis_results ...")
analysis_types = ['IOC Correlation','Campaign Attribution','Behavioral Analysis','Forensic Report',
                  'Threat Hunting Result','OSINT Summary','Dark Web Monitoring','Network Traffic Analysis',
                  'Malware Sandbox Report','Geo-attribution Analysis']
summaries = [
    'Multiple IOCs linked to a known APT group operating from East Asia.',
    'Phishing campaign attributed to a financially motivated threat actor group.',
    'Ransomware sample exhibits code overlap with LockBit 3.0 variants.',
    'IP address cluster linked to a bulletproof hosting provider.',
    'Victim network exhibits signs of lateral movement using stolen credentials.',
    'Dark web post found offering victim organization data for sale.',
    'C2 infrastructure identified; takedown request submitted.',
    'Malware beacon identified using Domain Generation Algorithm (DGA).',
    'Threat actor TTPs match MITRE ATT&CK T1566 (Phishing).',
    'Cryptocurrency wallets traced to exchanges registered in anonymous jurisdictions.',
]
for _ in range(100):
    cid = rng.choice(case_ids + [None])
    cur.execute(
        "INSERT INTO threat_analysis_results (related_case_id,analysis_type,summary,generated_at) "
        "VALUES (%s,%s,%s,%s)",
        (cid, rng.choice(analysis_types), rng.choice(summaries) + f" [Ref:{rng.randint(1000,9999)}]", rand_dt(180))
    )
conn.commit()
print("   100 threat_analysis_results inserted")

# ──────────────────────────────────────────────
# 29. INCIDENTS
# ──────────────────────────────────────────────
print("[29/36] incidents ...")
inc_types = ['Phishing Attack','Ransomware Infection','Data Breach','DDoS Attack','Insider Threat',
             'Account Compromise','Malware Outbreak','Credential Theft','Supply Chain Attack',
             'Zero Day Exploitation','Social Engineering','SQL Injection','Cryptojacking','BEC Fraud']
inc_statuses  = ['Detected','Triage','Investigating','Containing','Remediating','Recovering','Resolved','Closed']
inc_severities= ['Low','Medium','High','Critical']
for _ in range(100):
    ref       = f"INC{rng.randint(10000000,99999999)}"
    ca_id     = rng.choice(case_ids + [None])
    ioc_id    = rng.choice(ioc_ids + [None])
    resp_id   = rng.choice(responder_ids) if responder_ids else rng.choice(user_ids)
    inc_type  = rng.choice(inc_types)
    desc      = f"{inc_type} detected. Affected systems: {rng.randint(1,50)} hosts."
    sev       = rng.choice(inc_severities)
    status    = rng.choice(inc_statuses)
    det_at    = rand_dt(180)
    try:
        cur.execute(
            "INSERT INTO incidents (incident_reference,case_id,ioc_id,responder_id,incident_type,"
            "description,severity,status,detected_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (ref, ca_id, ioc_id, resp_id, inc_type, desc, sev, status, det_at)
        )
    except Exception:
        pass
conn.commit()
cur.execute("SELECT incident_id FROM incidents")
incident_ids = [r['incident_id'] for r in cur.fetchall()]
print(f"   {len(incident_ids)} incidents inserted")

# ──────────────────────────────────────────────
# 30. INCIDENT_ACTIVITIES
# ──────────────────────────────────────────────
print("[30/36] incident_activities ...")
inc_actions = ['Incident Detected','Alert Triggered','Initial Triage','Scope Assessment','Containment Action',
               'Malware Quarantined','Network Isolated','Password Reset','System Reimaged','Patch Applied',
               'User Notified','Management Escalated','Forensic Copy Made','Firewall Rule Updated','Case Closed']
for _ in range(100):
    iid  = rng.choice(incident_ids)
    uid  = rng.choice(user_ids + [None])
    cur.execute(
        "INSERT INTO incident_activities (incident_id,performed_by,action,activity_time) VALUES (%s,%s,%s,%s)",
        (iid, uid, rng.choice(inc_actions), rand_dt(120))
    )
conn.commit()
print("   100 incident_activities inserted")

# ──────────────────────────────────────────────
# 31. RESPONSE_ACTIONS
# ──────────────────────────────────────────────
print("[31/36] response_actions ...")
action_types = ['Block IP','Takedown Domain','Account Suspension','Network Isolation',
                'Malware Removal','Patch Deployment','Password Reset','Data Restore',
                'Legal Notice','Arrest Warrant','Evidence Seizure','User Training','Firewall Update','CDN Flush']
for _ in range(100):
    iid   = rng.choice(incident_ids)
    atype = rng.choice(action_types)
    desc  = f"Action performed. Result: {rng.choice(['Successful','Partial','Pending','Failed'])}. Systems affected: {rng.randint(1,20)}."
    uid   = rng.choice(user_ids + [None])
    cur.execute(
        "INSERT INTO response_actions (incident_id,action_type,description,performed_by,performed_at) "
        "VALUES (%s,%s,%s,%s,%s)",
        (iid, atype, desc, uid, rand_dt(120))
    )
conn.commit()
print("   100 response_actions inserted")

# ──────────────────────────────────────────────
# 32. PLAYBOOKS
# ──────────────────────────────────────────────
print("[32/36] playbooks ...")
playbook_data = [
    ('Ransomware Response Playbook',     'Ransomware',        'Step-by-step guide to contain and recover from ransomware.'),
    ('Phishing Incident Playbook',       'Phishing Attack',   'Actions to identify and remediate phishing attacks.'),
    ('Data Breach Response Playbook',    'Data Breach',       'Procedures for containing and reporting a data breach.'),
    ('DDoS Mitigation Playbook',         'DDoS Attack',       'Mitigation strategies for distributed denial of service.'),
    ('Insider Threat Response Playbook', 'Insider Threat',    'Steps to investigate and contain insider threat incidents.'),
    ('Account Compromise Playbook',      'Account Compromise','Procedures to recover compromised user accounts.'),
    ('Malware Outbreak Playbook',        'Malware Outbreak',  'Containment and eradication steps for malware outbreaks.'),
    ('BEC Fraud Response Playbook',      'BEC Fraud',         'Actions to take when Business Email Compromise is detected.'),
    ('Supply Chain Attack Playbook',     'Supply Chain Attack','Steps for investigating supply chain attacks.'),
    ('Zero Day Response Playbook',       'Zero Day Exploitation','Emergency procedures for zero day exploitation.'),
    ('Cryptojacking Response Playbook',  'Cryptojacking',     'Detection and removal of unauthorized cryptocurrency miners.'),
    ('Social Engineering Playbook',      'Social Engineering','Awareness and response to social engineering attacks.'),
    ('Credential Theft Playbook',        'Credential Theft',  'Steps to identify stolen credentials and prevent misuse.'),
    ('Network Intrusion Playbook',       'Network Intrusion', 'Procedures for detecting and isolating network intrusions.'),
    ('Mobile Device Compromise Playbook','Mobile Threat',     'Response procedures for compromised mobile devices.'),
]
for i in range(85):
    playbook_data.append((f"Security Playbook {i+1:03d}", f"Incident Type {i+1}", f"Generic response playbook {i+1} for security incidents."))

for pn, pit, pd in playbook_data[:100]:
    cur.execute("INSERT INTO playbooks (playbook_name,incident_type,description) VALUES (%s,%s,%s)", (pn, pit, pd))
conn.commit()
cur.execute("SELECT playbook_id FROM playbooks")
playbook_ids = [r['playbook_id'] for r in cur.fetchall()]
print(f"   {len(playbook_ids)} playbooks inserted")

# ──────────────────────────────────────────────
# 33. PLAYBOOK_STEPS
# ──────────────────────────────────────────────
print("[33/36] playbook_steps ...")
step_templates = [
    'Identify and isolate affected systems from the network.',
    'Notify the Incident Response team and management.',
    'Preserve evidence: take memory dumps and disk images.',
    'Analyse threat indicators using sandbox tools.',
    'Block identified IOCs at firewall and endpoint level.',
    'Reset all potentially compromised credentials.',
    'Restore systems from clean, verified backups.',
    'Apply available security patches to vulnerabilities.',
    'Conduct post-incident review and document lessons learned.',
    'Submit final incident report to regulatory authorities.',
    'Communicate incident status to affected stakeholders.',
    'Perform full antivirus and EDR scan on all endpoints.',
    'Review and update firewall and access control rules.',
    'Train staff on lessons learned from the incident.',
    'Close incident ticket and archive all evidence securely.',
]
pb_step_tracker = {pid: 1 for pid in playbook_ids}
inserted_steps = 0
for _ in range(100):
    pid = rng.choice(playbook_ids)
    order = pb_step_tracker[pid]
    desc  = step_templates[(order - 1) % len(step_templates)]
    try:
        cur.execute(
            "INSERT IGNORE INTO playbook_steps (playbook_id,step_order,step_description) VALUES (%s,%s,%s)",
            (pid, order, desc)
        )
        inserted_steps += 1
    except Exception:
        pass
    pb_step_tracker[pid] = order + 1
conn.commit()
print(f"   {inserted_steps} playbook_steps inserted")

# ──────────────────────────────────────────────
# 34. AUDIT_LOGS
# ──────────────────────────────────────────────
print("[34/36] audit_logs ...")
audit_actions = ['LOGIN','LOGOUT','VIEW_COMPLAINT','UPDATE_COMPLAINT','CREATE_CASE','ASSIGN_CASE',
                 'UPLOAD_EVIDENCE','VIEW_EVIDENCE','CREATE_IOC','DELETE_IOC','VIEW_REPORT',
                 'EXPORT_DATA','UPDATE_USER','DELETE_USER','ACCESS_AUDIT_LOG','RUN_PLAYBOOK',
                 'VIEW_INCIDENT','CREATE_INCIDENT','RESOLVE_INCIDENT','MANAGE_CAMPAIGN']
resources = ['complaints','cases','users','evidence','iocs','incidents','campaigns','playbooks','reports','audit_logs']
for _ in range(100):
    uid = rng.choice(user_ids + [None])
    cur.execute(
        "INSERT INTO audit_logs (user_id,action,resource,resource_id,event_time,ip_address,result) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (uid, rng.choice(audit_actions), rng.choice(resources),
         str(rng.randint(1, 1000)), rand_dt(90), fake_ip(), rng.choice(['Success','Failure']))
    )
conn.commit()
print("   100 audit_logs inserted")

# ──────────────────────────────────────────────
# 35. LOGIN_HISTORY
# ──────────────────────────────────────────────
print("[35/36] login_history ...")
lh_event_types = ['Login Success','Login Failed','Logout']
cur.execute("SELECT COUNT(*) as c FROM login_history")
existing_lh = cur.fetchone()['c']
to_insert_lh = max(0, 100 - existing_lh)
for _ in range(to_insert_lh):
    uid = rng.choice(user_ids + [None])
    cur.execute(
        "INSERT INTO login_history (user_id,event_type,event_time,ip_address) VALUES (%s,%s,%s,%s)",
        (uid, rng.choice(lh_event_types), rand_dt(90), fake_ip())
    )
conn.commit()
cur.execute("SELECT COUNT(*) as c FROM login_history")
print(f"   {cur.fetchone()['c']} login_history records total")

# ──────────────────────────────────────────────
# 36. SYSTEM_HEALTH
# ──────────────────────────────────────────────
print("[36/36] system_health ...")
components = ['API Gateway','Database Server','Authentication Service','File Storage Service',
              'Threat Feed Ingestion','Notification Service','Audit Logger','Search Engine',
              'Email Service','Cache Layer','Load Balancer','VPN Gateway','SIEM Connector',
              'Backup Service','Monitoring Agent','ML Anomaly Detector','IOC Enrichment Service',
              'Case Management Module','Evidence Vault','Reporting Engine']
health_statuses = ['Healthy','Healthy','Healthy','Warning','Down']
details_list = [
    'All checks passed. Response time: {}ms.',
    'CPU utilization at {}%. Memory normal.',
    'Warning: Disk usage at {}%.',
    'Service degraded. Latency spike detected.',
    'Component offline. Failover initiated.',
    'Heartbeat received. No anomalies detected.',
    'Connection pool at {}% capacity.',
    'Backup completed successfully in {}s.',
]
for _ in range(100):
    comp   = rng.choice(components)
    status = rng.choice(health_statuses)
    dtmpl  = rng.choice(details_list)
    detail = dtmpl.format(rng.randint(10, 99)) if '{}' in dtmpl else dtmpl
    cur.execute(
        "INSERT INTO system_health (component_name,status,checked_at,details) VALUES (%s,%s,%s,%s)",
        (comp, status, rand_dt(30), detail)
    )
conn.commit()
print("   100 system_health records inserted")

# ──────────────────────────────────────────────
# FINAL SUMMARY
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("  SEEDING COMPLETE - Final row counts")
print("=" * 60)
cur.execute("SHOW TABLES")
tables = [list(t.values())[0] for t in cur.fetchall()]
total_rows = 0
for t in sorted(tables):
    cur.execute(f"SELECT COUNT(*) as c FROM `{t}`")
    count = cur.fetchone()['c']
    total_rows += count
    icon = "OK" if count >= 20 else ("LOW" if count > 0 else "EMPTY")
    print(f"  [{icon:5}]  {t:<35} {count:>5} rows")
print(f"\n  Total rows across all tables: {total_rows}")
print("=" * 60)

cur.close()
conn.close()
