/* Applies the one-time account-approval schema migration. */
const fs = require("fs");
const mysql = require("mysql2/promise");

const env = Object.fromEntries(fs.readFileSync(".env", "utf8").split(/\r?\n/)
  .filter(line => line.includes("=") && !line.trim().startsWith("#"))
  .map(line => { const i = line.indexOf("="); return [line.slice(0, i).trim(), line.slice(i + 1).trim()]; }));

async function main() {
  const db = await mysql.createConnection({ host: env.DB_HOST, user: env.DB_USER, password: env.DB_PASSWORD, database: env.DB_NAME, port: Number(env.DB_PORT || 3306) });
  await db.query("ALTER TABLE users MODIFY account_status ENUM('Pending','Active','Inactive','Suspended') NOT NULL DEFAULT 'Active'");
  console.log("Account approval migration applied successfully.");
  await db.end();
}

main().catch(error => { console.error(`Migration failed: ${error.message}`); process.exitCode = 1; });
