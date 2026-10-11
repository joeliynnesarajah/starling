// Owner: Person 2
// "94% of your spending categorised" so judges can see the mapping is honest.
// Data: getCategorisedSummary(accountId) -> categorised_pence / spend_pence etc.

import { useEffect, useState } from "react";
import { getCategorisedSummary } from "../api.js";

// Turn pence into "£1,234.56"
const pounds = (pence) =>
  (pence / 100).toLocaleString("en-GB", { style: "currency", currency: "GBP" });

export default function CategorisedBadge({ accountId }) {
  const [summary, setSummary] = useState(null); // the numbers from the backend
  const [error, setError] = useState(null);

  // Load the summary whenever the chosen person changes
  useEffect(() => {
    setSummary(null);
    setError(null);
    getCategorisedSummary(accountId)
      .then(setSummary)
      .catch(() => setError("Couldn't load the summary"));
  }, [accountId]);

  if (error) return <section className="card" style={styles.card}>{error}</section>;
  if (!summary) return <section className="card" style={styles.card}>Loading…</section>;

  const spend = summary.spend_pence ?? 0;
  const categorised = summary.categorised_pence ?? 0;
  const methods = summary.by_method ?? {};

  // Percentage of spending we put into a category
  const pct = spend ? (categorised / spend) * 100 : 100;
  const pctText = pct >= 99.95 ? "100%" : `${pct.toFixed(1)}%`;

  return (
    <section className="card" style={styles.card}>
      <div style={styles.tag}>✓ HONEST MAPPING</div>
      <h3 style={styles.title}>How much we could categorise</h3>
      <div style={styles.big}>{pctText}</div>
      <p style={styles.text}>
        {pounds(categorised)} of {pounds(spend)} spending sorted into the 12 ONS categories.
      </p>
      <p style={styles.small}>
        {methods.mcc ?? 0} by card code · {methods.keyword ?? 0} by shop name ·{" "}
        {methods.bank_category ?? 0} by bank label · {methods.llm ?? 0} by AI ·{" "}
        {methods.unmapped ?? 0} unknown
      </p>
    </section>
  );
}

// Styling to match the penny. design
const styles = {
  card: {
    background: "#f3efff",
    border: "1px solid #e6defd",
    borderRadius: 22,
    padding: "22px 23px",
  },
  tag: {
    display: "inline-block",
    borderRadius: 12,
    background: "#e8e0ff",
    color: "#6d59d8",
    fontSize: 11,
    fontWeight: 800,
    padding: "7px 10px",
  },
  title: { fontFamily: "Outfit, sans-serif", fontSize: 18, margin: "12px 0 4px", color: "#292843" },
  big: { fontFamily: "Outfit, sans-serif", fontSize: 40, fontWeight: 800, color: "#745cde", letterSpacing: -1.4 },
  text: { fontSize: 12, color: "#6d618d", margin: "4px 0 8px" },
  small: { fontSize: 11, color: "#9996a7", margin: 0 },
};