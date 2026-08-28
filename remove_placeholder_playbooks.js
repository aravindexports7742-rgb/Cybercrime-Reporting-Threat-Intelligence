/* Removes only the generic Security Playbook 001-085 demo placeholders. */
const fs = require("fs");
const mysql = require("mysql2/promise");

const env = Object.fromEntries(fs.readFileSync(".env", "utf8").split(/\r?\n/)
  .filter(line => line.includes("=") && !line.trim().startsWith("#"))
  .map(line => { const i = line.indexOf("="); return [line.slice(0, i).trim(), line.slice(i + 1).trim()]; }));

async function main() {
  const db = await mysql.createConnection({ host: env.DB_HOST, user: env.DB_USER, password: env.DB_PASSWORD, database: env.DB_NAME, port: Number(env.DB_PORT || 3306) });
  await db.beginTransaction();
  try {
    const [items] = await db.query("SELECT playbook_id FROM playbooks WHERE playbook_name LIKE 'Security Playbook %'");
    const ids = items.map(item => item.playbook_id);
    if (ids.length) {
      const placeholders = ids.map(() => "?").join(",");
      await db.query(`DELETE FROM playbook_steps WHERE playbook_id IN (${placeholders})`, ids);
      await db.query(`DELETE FROM playbooks WHERE playbook_id IN (${placeholders})`, ids);
    }
    await db.commit();
    console.log(`Removed ${ids.length} placeholder playbooks and their linked steps.`);
  } catch (error) {
    await db.rollback();
    throw error;
  } finally {
    await db.end();
  }
}

main().catch(error => { console.error(`Cleanup failed: ${error.message}`); process.exitCode = 1; });
