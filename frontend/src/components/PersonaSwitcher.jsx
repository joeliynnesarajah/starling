// Owner: Person 2
// Dropdown of demo personas (and any uploaded statements).
// Data: getAccounts(). Call onChange(accountId) when the user picks one.

import { useEffect, useState } from "react";
import { getAccounts } from "../api.js";

// An emoji for each demo person (covers both naming styles)
const EMOJI = {
  student: "🎓", student_renter: "🎓",
  commuter: "🚗", car_commuter: "🚗",
  family: "🏡", young_family: "🏡",
  retiree: "🌷",
};

export default function PersonaSwitcher({ accountId, onChange }) {
  const [accounts, setAccounts] = useState([]); // the list of people
  const [error, setError] = useState(null);

  // Load the accounts (again whenever the chosen account changes,
  // so a newly uploaded statement shows up in the list)
  useEffect(() => {
    getAccounts()
      .then(setAccounts)
      .catch(() => setError("Couldn't load accounts"));
  }, [accountId]);

  if (error) return <div style={styles.error}>{error}</div>;

  // Is the current account in the list? (A fresh upload might not be yet)
  const known = accounts.some((a) => String(a.id ?? a.account_id) === String(accountId));

  function handleChange(event) {
    // The dropdown gives back text, so find the real account to keep its id type
    const picked = accounts.find((a) => String(a.id ?? a.account_id) === event.target.value);
    onChange(picked ? (picked.id ?? picked.account_id) : event.target.value);
  }

  return (
    <select
      style={styles.picker}
      value={String(accountId)}
      onChange={handleChange}
      aria-label="Choose demo persona"
    >
      {!known && <option value={String(accountId)}>📄 Your statement</option>}
      {accounts.map((a) => {
        const id = a.id ?? a.account_id;
        return (
          <option key={id} value={String(id)}>
            {EMOJI[a.persona] ?? "📄"} {a.name}
          </option>
        );
      })}
    </select>
  );
}

// Styling to match the penny. design
const styles = {
  picker: {
    border: "1px solid #e5e0f0",
    background: "white",
    padding: "12px 14px",
    borderRadius: 13,
    color: "#4b426e",
    fontSize: 13,
    fontWeight: 700,
    minWidth: 240,
    outline: 0,
    cursor: "pointer",
  },
  error: { color: "#b5485d", fontSize: 13 },
};