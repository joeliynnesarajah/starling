// Owner: Person 4
// "Your inflation: X%. Headline: Y%." plus the one-sentence explanation.

import { useEffect, useState } from "react";
import { getPersonalRate } from "../api.js";

const pct = (x) => `${(x * 100).toFixed(1)}%`;

export default function HeadlineCard({ accountId }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    setData(null);
    setError(null);
    getPersonalRate(accountId)
      .then(setData)
      .catch((e) => setError(e.message));
  }, [accountId]);

  if (error) return <section className="card">Couldn't load your rate: {error}</section>;
  if (!data) return <section className="card">Loading…</section>;

  const above = data.personal_rate > data.headline_rate;

  return (
    <section className="card">
      <h2>Your inflation rate</h2>
      <div style={{ display: "flex", alignItems: "baseline", gap: 16, flexWrap: "wrap" }}>
        <span style={{ fontSize: "3rem", fontWeight: 700, color: above ? "var(--bad)" : "var(--good)" }}>
          {pct(data.personal_rate)}
        </span>
        <span style={{ color: "var(--muted)" }}>
          National average {pct(data.headline_rate)}
        </span>
      </div>
      <p style={{ marginBottom: 0 }}>{data.explanation}</p>
      <p style={{ color: "var(--muted)", fontSize: "0.85rem", marginBottom: 0 }}>
        Based on your spending in the 12 months to {data.month}
      </p>
    </section>
  );
}