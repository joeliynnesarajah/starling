// Owner: Person 2
// Upload a bank statement CSV, then switch to the new account.
// Data: uploadStatement(file, accountName) -> { account_id, inserted, summary }
// Call onImported(account_id) when done.

import { useState } from "react";
import { uploadStatement } from "../api.js";

export default function UploadStatement({ onImported }) {
  const [file, setFile] = useState(null);       // the chosen CSV
  const [name, setName] = useState("");         // name for the new account
  const [status, setStatus] = useState("idle"); // idle | uploading | done | error
  const [message, setMessage] = useState("");

  function handleFile(event) {
    const chosen = event.target.files[0];
    setFile(chosen ?? null);
    // Suggest a name from the file name, e.g. "statement.csv" -> "statement"
    if (chosen && !name) setName(chosen.name.replace(/\.csv$/i, ""));
    setStatus("idle");
  }

  async function handleUpload() {
    if (!file) return;
    setStatus("uploading");
    try {
      const result = await uploadStatement(file, name || "My statement");
      const s = result.summary ?? {};
      const pct = s.spend_pence ? Math.round((s.categorised_pence / s.spend_pence) * 100) : 100;
      setMessage(`Imported ${result.inserted} transactions · ${pct}% categorised`);
      setStatus("done");
      onImported(result.account_id); // switch the whole page to the new account
    } catch (err) {
      setMessage("That didn't work. Is it a Starling or Monzo CSV export?");
      setStatus("error");
    }
  }

  return (
    <section className="card" style={styles.card}>
      <h3 style={styles.title}>Try it with your own statement 📄</h3>
      <p style={styles.text}>
        Upload a Starling or Monzo CSV export. Nothing leaves this demo.
      </p>

      <input type="file" accept=".csv" onChange={handleFile} style={styles.file} />

      <input
        type="text"
        placeholder="Account name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={styles.input}
      />

      <button
        onClick={handleUpload}
        disabled={!file || status === "uploading"}
        style={{ ...styles.button, opacity: !file || status === "uploading" ? 0.5 : 1 }}
      >
        {status === "uploading" ? "Uploading…" : "Upload statement"}
      </button>

      {status === "done" && <p style={styles.ok}>✓ {message}</p>}
      {status === "error" && <p style={styles.bad}>{message}</p>}
    </section>
  );
}

// Styling to match the penny. design
const styles = {
  card: { background: "white", border: "1px solid #efedf4", borderRadius: 22, padding: "22px 23px" },
  title: { fontFamily: "Outfit, sans-serif", fontSize: 18, margin: "0 0 6px", color: "#292843" },
  text: { fontSize: 12, color: "#9996a7", margin: "0 0 14px" },
  file: { display: "block", fontSize: 12, marginBottom: 10 },
  input: {
    display: "block",
    width: "100%",
    border: "1px solid #e5e0f0",
    borderRadius: 12,
    padding: "10px 12px",
    fontSize: 13,
    marginBottom: 12,
    boxSizing: "border-box",
  },
  button: {
    background: "#745cde",
    color: "white",
    border: 0,
    borderRadius: 13,
    padding: "11px 16px",
    fontWeight: 700,
    fontSize: 13,
    cursor: "pointer",
  },
  ok: { color: "#21875f", fontSize: 12, fontWeight: 700, marginTop: 10 },
  bad: { color: "#b5485d", fontSize: 12, fontWeight: 700, marginTop: 10 },
};