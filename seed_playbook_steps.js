/* Ensures every existing response playbook has at least five visible steps. */
const fs = require("fs");
const mysql = require("mysql2/promise");

const env = Object.fromEntries(fs.readFileSync(".env", "utf8").split(/\r?\n/)
  .filter(line => line.includes("=") && !line.trim().startsWith("#"))
  .map(line => { const i = line.indexOf("="); return [line.slice(0, i).trim(), line.slice(i + 1).trim()]; }));

const steps = [
  "Triage the alert and confirm the incident scope.",
  "Preserve relevant logs and evidence for investigation.",
  "Contain affected accounts, systems, domains, or network access.",
  "Remediate the cause and validate that the threat is removed.",
  "Document the outcome, notify stakeholders, and close after review.",
];

async function main() {
  const db = await mysql.createConnection({ host: env.DB_HOST, user: env.DB_USER, password: env.DB_PASSWORD, database: env.DB_NAME, port: Number(env.DB_PORT || 3306) });
  const [playbooks] = await db.query("SELECT playbook_id FROM playbooks");
  let inserted = 0;
  for (const playbook of playbooks) {
    const [existing] = await db.execute("SELECT COUNT(*) AS total FROM playbook_steps WHERE playbook_id = ?", [playbook.playbook_id]);
    for (let order = existing[0].total + 1; order <= 5; order++) {
      await db.execute("INSERT INTO playbook_steps (playbook_id,step_order,step_description) VALUES (?,?,?)", [playbook.playbook_id, order, steps[order - 1]]);
      inserted++;
    }
  }
  console.log(`Added ${inserted} playbook steps; every playbook now has at least five steps.`);
  await db.end();
}

main().catch(error => { console.error(`Playbook seeding failed: ${error.message}`); process.exitCode = 1; });
