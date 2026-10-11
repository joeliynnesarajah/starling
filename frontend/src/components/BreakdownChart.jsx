// Owner: Person 4
// Which categories drive your rate: one bar per category, by contribution.

import { useEffect, useState } from "react";
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getPersonalRate } from "../api.js";

// Short names so the labels fit (same idea as calc/explain.py)
const SHORT_NAMES = {
  "01": "Food",
  "02": "Alcohol & tobacco",
  "03": "Clothing",
  "04": "Housing & bills",
  "05": "Household goods",
  "06": "Health",
  "07": "Transport",
  "08": "Phone & internet",
  "09": "Leisure",
  "10": "Education",
  "11": "Eating out",
  "12": "Other",
};

const pct = (x) => `${(x * 100).toFixed(1)}%`;

export default function BreakdownChart({ accountId }) {
  const [rows, setRows] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    setRows(null);
    setError(null);
    getPersonalRate(accountId)
      .then((data) =>
        setRows(
          data.weights.map((w) => ({
            name: SHORT_NAMES[w.code] ?? w.name,
            contribution: w.contribution * 100, // percentage points
            weight: w.weight,
            rate: w.rate,
          }))
        )
      )
      .catch((e) => setError(e.message));
  }, [accountId]);

  if (error) return <section className="card">Couldn't load the breakdown: {error}</section>;
  if (!rows) return <section className="card">Loading…</section>;

  return (
    <section className="card">
      <h2>What's driving it</h2>
      <ResponsiveContainer width="100%" height={rows.length * 36 + 20}>
        <BarChart data={rows} layout="vertical" margin={{ left: 10, right: 20 }}>
          <XAxis type="number" tickFormatter={(v) => `${v.toFixed(1)}`} />
          <YAxis type="category" dataKey="name" width={120} />
          <Tooltip
            formatter={(value, _name, item) => [
              `${value.toFixed(2)} points (${pct(item.payload.weight)} of spending, prices up ${pct(item.payload.rate)})`,
              "Adds",
            ]}
          />
          <Bar dataKey="contribution" fill="var(--you)" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <p style={{ color: "var(--muted)", fontSize: "0.85rem", marginBottom: 0 }}>
        Percentage points each category adds to your rate.
      </p>
    </section>
  );
}