// Owner: Person 4
// Which categories drive your rate: one outlined pill bar per category,
// with the percentage points it adds. Negative contributions go left, in mint.

import { useEffect, useState } from "react";
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

// 2.2 -> "+2.2", 0.16 -> "+0.16", 0 -> "0.00", -0.02 -> "−0.02"
function formatPoints(p) {
  if (Math.abs(p) < 0.005) return "0.00";
  const digits = Math.abs(p) >= 0.5 ? 1 : 2;
  const text = Math.abs(p).toFixed(digits);
  return p > 0 ? `+${text}` : `−${text}`;
}

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
            code: w.code,
            name: SHORT_NAMES[w.code] ?? w.name,
            points: w.contribution * 100, // percentage points
            weight: w.weight,
            rate: w.rate,
          }))
        )
      )
      .catch((e) => setError(e.message));
  }, [accountId]);

  if (error) return <section className="card">Couldn't load the breakdown: {error}</section>;
  if (!rows) return <section className="card">Loading…</section>;

  // Scale bars so the biggest one fills about 85% of the track
  const maxPos = Math.max(0.01, ...rows.map((r) => r.points));
  const maxNeg = Math.max(0, ...rows.map((r) => -r.points));
  const zeroAt = maxNeg > 0 ? 6 : 0; // % from the left where the zero line sits
  const scale = (85 - zeroAt) / maxPos;

  return (
    <section className="card breakdown-card">
      <span className="tape" aria-hidden="true" />
      <h2>What's driving it</h2>

      <div className="bd-rows">
        {rows.map((r) => {
          const width = Math.abs(r.points) * scale;
          const isZero = Math.abs(r.points) < 0.005;
          const negative = r.points < 0;
          return (
            <div
              className="bd-row"
              key={r.code}
              title={`${(r.weight * 100).toFixed(0)}% of your spending, prices up ${(r.rate * 100).toFixed(1)}%`}
            >
              <span className="bd-label">{r.name}</span>
              <span className="bd-track">
                <span className="bd-zero" style={{ left: `${zeroAt}%` }} />
                {!isZero && (
                  <span
                    className={`bd-bar ${negative ? "neg" : ""}`}
                    style={
                      negative
                        ? { right: `${100 - zeroAt}%`, width: `max(${width}%, 18px)` }
                        : { left: `${zeroAt}%`, width: `max(${width}%, 22px)` }
                    }
                  />
                )}
                <span
                  className="bd-value"
                  style={{
                    left: negative || isZero
                      ? `calc(${zeroAt}% + 10px)`
                      : `calc(${zeroAt}% + max(${width}%, 22px) + 8px)`,
                  }}
                >
                  {formatPoints(r.points)}
                </span>
              </span>
            </div>
          );
        })}
      </div>

      <p className="bd-note">Percentage points each category adds to your rate.</p>

      <style>{`
        .tape {
          position: absolute; top: -14px; left: 36px;
          width: 120px; height: 28px;
          background: repeating-linear-gradient(135deg, #ffe17a 0 10px, #fff1b0 10px 20px);
          transform: rotate(-4deg);
          opacity: 0.9;
        }
        .bd-rows { display: flex; flex-direction: column; gap: 10px; }
        .bd-row { display: grid; grid-template-columns: 140px 1fr; align-items: center; gap: 14px; }
        .bd-label { text-align: right; font-weight: 700; font-size: 0.95rem; }
        .bd-track { position: relative; height: 26px; }
        .bd-zero {
          position: absolute; top: -6px; bottom: -6px;
          border-left: 2px dashed #c9a9a6;
        }
        .bd-bar {
          position: absolute; top: 2px; height: 22px;
          background: var(--pink);
          border: 2.5px solid var(--ink);
          border-radius: 999px;
          box-sizing: border-box;
        }
        .bd-bar.neg { background: var(--mint); }
        .bd-value {
          position: absolute; top: 3px;
          font-weight: 800; font-size: 0.85rem; white-space: nowrap;
        }
        .bd-note { margin: 20px 0 0; color: var(--ink-soft); font-weight: 600; font-size: 0.9rem; }
      `}</style>
    </section>
  );
}
