/*
 * Adds exactly 500 linked, fictional demo records for presentation/testing.
 * Run: node seed_500_demo_data.js
 */
const fs = require("fs");
const mysql = require("mysql2/promise");

const env = Object.fromEntries(
  fs.readFileSync(".env", "utf8").split(/\r?\n/)
    .filter(line => line && !line.trim().startsWith("#") && line.includes("="))
    .map(line => { const index = line.indexOf("="); return [line.slice(0, index).trim(), line.slice(index + 1).trim()]; })
);

const config = {
  host: env.DB_HOST || "127.0.0.1",
  user: env.DB_USER || "root",
  password: env.DB_PASSWORD || "",
  database: env.DB_NAME || "cyber_threat_platform",
  port: Number(env.DB_PORT || 3306),
};

const complaintTitles = [
  "UPI payment sent to a fraudulent account", "Suspicious banking link received by SMS",
  "Fake online shopping website took payment", "Social-media account was taken over",
  "Fraudulent job offer requested an advance fee", "Unknown caller requested an OTP",
];
const caseStatuses = ["New", "Under Review", "Assigned", "Investigation", "Action Taken", "Resolved", "Closed"];
const priorities = ["Low", "Medium", "High", "Critical"];
const activityActions = ["Reviewed complaint and available evidence", "Contacted affected financial institution", "Requested preservation of transaction records", "Validated reported malicious indicator", "Prepared victim status update"];

async function main() {
  const db = await mysql.createConnection(config);
  try {
    const [victims] = await db.query("SELECT victim_id, user_id FROM victim_profiles LIMIT 100");
    const [categories] = await db.query("SELECT category_id FROM complaint_categories LIMIT 100");
    const [officers] = await db.query("SELECT u.user_id FROM users u JOIN roles r ON r.role_id = u.role_id WHERE r.role_name = 'Officer' AND u.account_status = 'Active'");
    const [responders] = await db.query("SELECT u.user_id FROM users u JOIN roles r ON r.role_id = u.role_id WHERE r.role_name = 'Incident Responder' AND u.account_status = 'Active'");
    if (!victims.length || !categories.length || !officers.length) throw new Error("Seed prerequisites are missing: victims, categories, or active officers.");

    const stamp = Date.now().toString().slice(-8);
    const complaintIds = [];
    const caseIds = [];
    await db.beginTransaction();

    // 100 complaints + 100 linked cases.
    for (let i = 0; i < 100; i++) {
      const victim = victims[i % victims.length];
      const category = categories[i % categories.length];
      const status = caseStatuses[i % caseStatuses.length];
      const complaintStatus = status === "New" ? "Submitted" : status;
      const tracking = `DM${stamp}${String(i).padStart(4, "0")}`;
      const [complaint] = await db.execute(
        "INSERT INTO complaints (tracking_id,victim_id,category_id,title,incident_date,description,financial_loss,suspected_url,suspected_phone,suspected_email,status) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        [tracking, victim.victim_id, category.category_id, complaintTitles[i % complaintTitles.length], new Date(Date.now() - i * 86400000), `Demo complaint ${i + 1}: reported for investigation during the project presentation.`, (i + 1) * 1250, i % 2 ? `https://suspicious-demo-${i}.example` : null, i % 3 ? `+9198${String(10000000 + i).slice(-8)}` : null, i % 4 ? `report-${i}@example.test` : null, complaintStatus]
      );
      complaintIds.push({ id: complaint.insertId, victimUserId: victim.user_id, status: complaintStatus });
      const [caseRow] = await db.execute(
        "INSERT INTO cases (case_reference,complaint_id,lead_officer_id,priority,status,opened_at) VALUES (?,?,?,?,?,?)",
        [`DEMO-${stamp}-${String(i).padStart(3, "0")}`, complaint.insertId, officers[i % officers.length].user_id, priorities[i % priorities.length], status, new Date(Date.now() - i * 86400000)]
      );
      caseIds.push(caseRow.insertId);
    }

    // 100 investigation activities + 75 victim notifications.
    for (let i = 0; i < 100; i++) {
      await db.execute("INSERT INTO investigation_activities (case_id,officer_id,action,result,activity_date) VALUES (?,?,?,?,?)", [caseIds[i], officers[i % officers.length].user_id, activityActions[i % activityActions.length], "Demo progress recorded; follow-up scheduled.", new Date()]);
      if (i < 75) await db.execute("INSERT INTO notifications (user_id,complaint_id,message,event_type) VALUES (?,?,?,?)", [complaintIds[i].victimUserId, complaintIds[i].id, `Your complaint is currently marked '${complaintIds[i].status}'.`, "Status Update"]);
    }

    // 75 threat indicators + 50 incidents = 500 total new rows.
    for (let i = 0; i < 75; i++) await db.execute("INSERT INTO iocs (ioc_type,ioc_value,risk_level) VALUES (?,?,?)", [i % 3 === 0 ? "Domain" : i % 3 === 1 ? "URL" : "Email", i % 3 === 0 ? `fraud-demo-${stamp}-${i}.example` : i % 3 === 1 ? `https://fraud-demo-${stamp}-${i}.example` : `abuse-${stamp}-${i}@example.test`, priorities[i % priorities.length]]);
    for (let i = 0; i < 50; i++) await db.execute("INSERT INTO incidents (incident_reference,case_id,responder_id,incident_type,description,severity,status) VALUES (?,?,?,?,?,?,?)", [`INC-D${stamp}-${String(i).padStart(3, "0")}`, caseIds[i], responders.length ? responders[i % responders.length].user_id : null, "Escalated demo cybercrime case", "Demo incident created from a high-priority case for response workflow testing.", priorities[(i + 2) % priorities.length], i % 2 ? "Investigating" : "Triage"]);

    await db.commit();
    console.log("Inserted exactly 500 linked demo records: 100 complaints, 100 cases, 100 activities, 75 notifications, 75 IOCs, and 50 incidents.");
  } catch (error) {
    await db.rollback();
    throw error;
  } finally {
    await db.end();
  }
}

main().catch(error => { console.error(`Seeding failed: ${error.message}`); process.exitCode = 1; });
