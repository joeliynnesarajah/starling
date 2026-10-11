// Owners: Person 3 (headline line) and Person 4 (your line)
// You vs the headline rate over the last 12 months.
// Data: getInflationHistory() for the headline, getPersonalHistory(accountId) for you.
// Chart library: recharts

import { useEffect, useState } from "react";
import {
  Area,
  CartesianGrid,
  ComposedChart,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { getInflationHistory, getPersonalHistory } from "../api.js";

const INK = "#4a2c2a";
const PINK = "#e8336d";

const toPercent = (rate) => (rate == null ? null : Number((rate * 100).toFixed(2)));

// "2025-02" -> "Feb 25"
const shortMonth = (ym) => {
  const [y, m] = ym.split("-").map(Number);
  return `${new Date(y, m - 1, 1).toLocaleDateString("en-GB", { month: "short" })} ${String(y).slice(2)}`;
};

// Your line: white dots, and a heart with a label on the latest month
function YouDot({ cx, cy, index, payload, lastIndex }) {
  if (cx == null || cy == null) return null;
  if (index !== lastIndex) {
    return <circle cx={cx} cy={cy} r={4.5} fill="#fff" stroke={INK} strokeWidth={2} />;
  }
  return (
    <g>
      <path
        transform={`translate(${cx - 11}, ${cy - 10}) scale(0.92)`}
        d="M12 21.5C5 16.5 0.5 12.4 0.5 7.2 0.5 3.6 3.2 1 6.5 1c2.2 0 4.2 1.2 5.5 3 1.3-1.8 3.3-3 5.5-3 3.3 0 6 2.6 6 6.2 0 5.2-4.5 9.3-11.5 14.3z"
        fill={PINK}
        stroke={INK}
        strokeWidth={2}
      />
      <text x={cx + 16} y={cy + 5} fontSize={13} fontWeight={800} fill={INK}>
        {payload.you.toFixed(1)}%
      </text>
    </g>
  );
}

// Headline line: no dots, just a label on the latest month
function HeadlineDot({ cx, cy, index, payload, lastIndex }) {
  if (cx == null || cy == null || index !== lastIndex) return null;
  return (
    <text x={cx + 12} y={cy + 16} fontSize={11} fontWeight={700} fill={INK}>
      {payload.headline.toFixed(1)}%
    </text>
  );
}

function LegendPill({ dashed, label }) {
  return (
    <span className="hc-pill">
      <svg width="22" height="8" aria-hidden="true">
        <line x1="1" y1="4" x2="21" y2="4" stroke={dashed ? INK : PINK} strokeWidth="3"
              strokeDasharray={dashed ? "3 3" : undefined} strokeLinecap="round" />
      </svg>
      {label}
    </span>
  );
}

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

  const title = <h2 style={{ margin: 0 }}>You vs the headline</h2>;
  if (error) return <section className="card">{title}<p className="error">{error}</p></section>;
  if (!history || !personal) return <section className="card">{title}<p>Loading…</p></section>;

  // Look up your rate by month, e.g. { "2025-02": 0.041, ... }
  const yourRateByMonth = Object.fromEntries(personal.points.map((p) => [p.month, p.personal_rate]));

  const data = history.points.map((p) => ({
    month: p.month,
    headline: toPercent(p.headline_rate),
    you: toPercent(yourRateByMonth[p.month]),
  }));
  const lastIndex = data.length - 1;

  return (
    <section className="card">
      <div className="hc-head">
        {title}
        <div className="hc-legend">
          <LegendPill label="You" />
          <LegendPill dashed label="Headline (ONS)" />
        </div>
      </div>

      <ResponsiveContainer width="100%" height={260}>
        <ComposedChart data={data} margin={{ top: 16, right: 58, bottom: 0, left: -12 }}>
          <defs>
            <linearGradient id="youFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={PINK} stopOpacity={0.18} />
              <stop offset="100%" stopColor={PINK} stopOpacity={0.08} />
            </linearGradient>
          </defs>
          <CartesianGrid vertical={false} stroke="#f1d4dc" />
          <XAxis
            dataKey="month"
            tickFormatter={shortMonth}
            tick={{ fill: INK, fontSize: 12, fontWeight: 700 }}
            axisLine={{ stroke: INK, strokeWidth: 2 }}
            tickLine={false}
            interval="preserveStartEnd"
            minTickGap={24}
          />
          <YAxis
            unit="%"
            tick={{ fill: INK, fontSize: 11, fontWeight: 700 }}
            axisLine={false}
            tickLine={false}
            domain={[(min) => Math.max(0, Math.floor(min - 1)), (max) => Math.ceil(max + 0.5)]}
            allowDecimals={false}
          />
          <Tooltip
            formatter={(v, name) => [`${v}%`, name === "you" ? "You" : "Headline (ONS)"]}
            labelFormatter={shortMonth}
            contentStyle={{ borderRadius: 14, border: `2px solid ${INK}`, fontWeight: 700 }}
          />
          <Area type="linear" dataKey="you" stroke="none" fill="url(#youFill)" connectNulls isAnimationActive={false} />
          <Line
            type="linear"
            dataKey="headline"
            stroke={INK}
            strokeWidth={2}
            strokeDasharray="6 5"
            dot={(props) => <HeadlineDot key={`h${props.index}`} {...props} lastIndex={lastIndex} />}
            activeDot={false}
            isAnimationActive={false}
          />
          <Line
            type="linear"
            dataKey="you"
            stroke={PINK}
            strokeWidth={4}
            connectNulls
            dot={(props) => <YouDot key={`y${props.index}`} {...props} lastIndex={lastIndex} />}
            isAnimationActive={false}
          />
        </ComposedChart>
      </ResponsiveContainer>

      <style>{`
        .hc-head { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 14px; }
        .hc-legend { display: flex; gap: 8px; flex-wrap: wrap; }
        .hc-pill {
          display: inline-flex; align-items: center; gap: 8px;
          border: 2px solid var(--ink); border-radius: 999px;
          padding: 4px 12px; font-weight: 700; font-size: 0.85rem; background: #fff;
        }
      `}</style>
    </section>
  );
}
