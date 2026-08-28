/* Approves one pending internal-access request. Run: node approve_user.js user@example.com */
const fs = require("fs");
const mysql = require("mysql2/promise");
const email = process.argv[2];

if (!email) throw new Error("Provide the exact registered email address.");
const env = Object.fromEntries(fs.readFileSync(".env", "utf8").split(/\r?\n/)
  .filter(line => line.includes("=") && !line.trim().startsWith("#"))
  .map(line => { const i = line.indexOf("="); return [line.slice(0, i).trim(), line.slice(i + 1).trim()]; }));

async function main() {
  const db = await mysql.createConnection({ host: env.DB_HOST, user: env.DB_USER, password: env.DB_PASSWORD, database: env.DB_NAME, port: Number(env.DB_PORT || 3306) });
  const [users] = await db.execute("SELECT u.user_id, u.email, u.account_status, r.role_name FROM users u JOIN roles r ON r.role_id = u.role_id WHERE u.email = ?", [email]);
  if (!users.length) throw new Error("No account was found with that exact email address.");
  const user = users[0];
  if (user.account_status === "Pending") await db.execute("UPDATE users SET account_status = 'Active' WHERE user_id = ?", [user.user_id]);
  console.log(`Account ${user.email} (${user.role_name}) is ${user.account_status === "Pending" ? "now approved and active" : `already ${user.account_status}`}.`);
  await db.end();
}

main().catch(error => { console.error(`Approval failed: ${error.message}`); process.exitCode = 1; });
