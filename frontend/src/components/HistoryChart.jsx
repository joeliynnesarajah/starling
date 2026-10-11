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
import { getInflationHistory, getPersonalHistory } from "../api.js";

const toPercent = (rate) => (rate == null ? null : Number((rate * 100).toFixed(2)));

export default function HistoryChart({ accountId }) {
  const [history, setHistory] = useState(null);
  const [personal, setPersonal] = useState(null);
  const [error, setError] = useState(null);

  // Headline: same for everyone, so only fetched once (Person 3)
  useEffect(() => {
    let cancelled = false;
    getInflationHistory(12)
      .then((data) => !cancelled && setHistory(data))
      .catch((e) => !cancelled && setError(e.message || "Could not load inflation history"));
    return () => {
      cancelled = true;
    };
  }, []);

  // Personal: fetched again whenever the persona changes (Person 4)
  useEffect(() => {
    let cancelled = false;
    setPersonal(null);
    getPersonalHistory(accountId)
      .then((data) => !cancelled && setPersonal(data))
      .catch((e) => !cancelled && setError(e.message || "Could not load your rate history"));
    return () => {
      cancelled = true;
    };
  }, [accountId]);

  if (error) return <section className="card"><h2>You vs the headline</h2><p className="error">{error}</p></section>;
  if (!history || !personal) return <section className="card"><h2>You vs the headline</h2><p>Loading…</p></section>;

  // Look up your rate by month, e.g. { "2025-02": 0.041, ... }
  const yourRateByMonth = Object.fromEntries(
    personal.points.map((p) => [p.month, p.personal_rate])
  );

  const data = history.points.map((p) => ({
    month: p.month,
    headline: toPercent(p.headline_rate),
    you: toPercent(yourRateByMonth[p.month]),
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
          <Line
            type="monotone"
            dataKey="you"
            name="You"
            stroke="var(--you)"
            strokeWidth={3}
            dot={false}
            connectNulls
          />
        </LineChart>
      </ResponsiveContainer>
    </section>
  );
}