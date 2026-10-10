// Owners: Person 3 (headline line) and Person 4 (your line)
// You vs the headline rate over the last 12 months.
// Data: getInflationHistory() for the headline, getPersonalHistory(accountId) for you.
// Colours: var(--you) and var(--headline) from styles.css
// Chart library: recharts (LineChart)

import { useEffect, useState } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { getInflationHistory } from "../api.js";

const toPercent = (rate) => (rate == null ? null : Number((rate * 100).toFixed(2)));

export default function HistoryChart({ accountId }) {
  const [history, setHistory] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    getInflationHistory(12)
      .then((data) => !cancelled && setHistory(data))
      .catch((e) => !cancelled && setError(e.message || "Could not load inflation history"));
    return () => {
      cancelled = true;
    };
  }, []);

  // TODO(Person 4): fetch getPersonalHistory(accountId) the same way and merge
  // each point's personal rate into `data` below as `you`.

  if (error) return <section className="card"><h2>You vs the headline</h2><p className="error">{error}</p></section>;
  if (!history) return <section className="card"><h2>You vs the headline</h2><p>Loading…</p></section>;

  const data = history.points.map((p) => ({
    month: p.month,
    headline: toPercent(p.headline_rate),
    // TODO(Person 4): you: toPercent(personalRateForThisMonth),
  }));

  return (
    <section className="card">
      <h2>You vs the headline</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 8, right: 16, bottom: 0, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis unit="%" />
          <Tooltip formatter={(v) => `${v}%`} />
          <Legend />
          <Line
            type="monotone"
            dataKey="headline"
            name="Headline (ONS)"
            stroke="var(--headline)"
            strokeWidth={2}
            dot={false}
          />
          {/* TODO(Person 4): <Line dataKey="you" name="You" stroke="var(--you)" ... /> */}
        </LineChart>
      </ResponsiveContainer>
    </section>
  );
}