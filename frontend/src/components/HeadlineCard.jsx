// Owner: Person 4
// Big personal rate, a "UK average" sticker, and the explanation in a
// speech bubble from a piggy bank.

import { useEffect, useState } from "react";
import { getPersonalRate } from "../api.js";

const pct = (x) => `${(x * 100).toFixed(1)}%`;

// "2026-01" -> "January 2026"
const monthName = (ym) => {
  const [y, m] = ym.split("-").map(Number);
  return new Date(y, m - 1, 1).toLocaleDateString("en-GB", { month: "long", year: "numeric" });
};

function Piggy() {
  return (
    <svg viewBox="0 0 170 130" width="160" aria-hidden="true">
      <g stroke="#4a2c2a" strokeWidth="4" strokeLinejoin="round">
        {/* coin */}
        <circle cx="78" cy="20" r="14" fill="#ffe17a" />
        <text x="78" y="27" textAnchor="middle" fontSize="18" fontWeight="800" fill="#4a2c2a" stroke="none" fontFamily="Fredoka, sans-serif">£</text>
        {/* legs */}
        <rect x="48" y="100" width="18" height="20" rx="8" fill="#ffa3c2" />
        <rect x="100" y="100" width="18" height="20" rx="8" fill="#ffa3c2" />
        {/* tail */}
        <path d="M18 72c-8-2-10-10-4-12s6 6 0 8" fill="none" />
        {/* body */}
        <ellipse cx="80" cy="78" rx="62" ry="40" fill="#ffa3c2" />
        {/* ear */}
        <path d="M108 44l10-18 6 22z" fill="#ffa3c2" />
        {/* slot */}
        <path d="M66 42h26" strokeLinecap="round" />
        {/* snout */}
        <ellipse cx="140" cy="80" rx="16" ry="13" fill="#ffc4d7" />
      </g>
      <circle cx="135" cy="80" r="2.6" fill="#4a2c2a" />
      <circle cx="145" cy="80" r="2.6" fill="#4a2c2a" />
      <circle cx="118" cy="62" r="4" fill="#4a2c2a" />
      <ellipse cx="104" cy="80" rx="8" ry="5" fill="#ff7aa2" opacity="0.7" />
    </svg>
  );
}

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

  return (
    <section className="card headline-card">
      <span className="headline-sparkle" aria-hidden="true">✦</span>

      <div className="headline-left">
        <h2>Your inflation rate</h2>
        <div className="headline-row">
          <span className="headline-number">{pct(data.personal_rate)}</span>
          <span className="uk-sticker">
            <small>UK average</small>
            <strong>{pct(data.headline_rate)}</strong>
          </span>
        </div>
        <p className="headline-month">Based on your spending in the 12 months to {monthName(data.month)}</p>
      </div>

      <div className="headline-right">
        <p className="speech-bubble">{data.explanation}</p>
        <Piggy />
      </div>

      <style>{`
        .headline-card {
          display: grid;
          grid-template-columns: 1.1fr 1fr;
          gap: 24px;
          align-items: center;
          padding: 40px 44px;
        }
        .headline-sparkle {
          position: absolute; top: -18px; left: 50%;
          transform: translateX(-50%);
          font-size: 2rem; color: #ffe17a;
          -webkit-text-stroke: 2px #4a2c2a;
        }
        .headline-row { display: flex; align-items: center; gap: 22px; flex-wrap: wrap; }
        .headline-number {
          font-family: "Fredoka", sans-serif;
          font-weight: 700;
          font-size: clamp(4rem, 9vw, 7.5rem);
          line-height: 1;
          color: var(--pink);
          text-shadow: 5px 5px 0 var(--ink);
          letter-spacing: -2px;
        }
        .uk-sticker {
          width: 118px; height: 118px;
          border-radius: 50%;
          background: var(--yellow);
          border: 2.5px solid var(--ink);
          display: flex; flex-direction: column; align-items: center; justify-content: center;
          transform: rotate(8deg);
          font-family: "Fredoka", sans-serif;
          color: var(--ink);
        }
        .uk-sticker small { font-size: 0.85rem; font-weight: 600; }
        .uk-sticker strong { font-size: 1.9rem; font-weight: 700; line-height: 1; }
        .headline-month { margin: 18px 0 0; color: var(--ink-soft); font-weight: 600; }
        .headline-right { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; }
        .speech-bubble {
          position: relative;
          margin: 0;
          background: var(--pink-pale);
          border: 2.5px solid var(--ink);
          border-radius: 24px;
          padding: 20px 26px;
          font-weight: 600;
          line-height: 1.55;
          max-width: 460px;
        }
        .speech-bubble::after {
          content: "";
          position: absolute; bottom: -14px; right: 80px;
          width: 22px; height: 22px;
          background: var(--pink-pale);
          border-right: 2.5px solid var(--ink);
          border-bottom: 2.5px solid var(--ink);
          transform: rotate(45deg);
        }
        @media (max-width: 760px) {
          .headline-card { grid-template-columns: 1fr; padding: 28px 22px; }
          .headline-right { align-items: center; }
        }
      `}</style>
    </section>
  );
}
