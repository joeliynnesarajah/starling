// Owner: Person 2
// "94% of your spending categorised" so judges can see the mapping is honest.
// Data: getCategorisedSummary(accountId) -> categorised_pence / spend_pence etc.
// Styled as a slightly tilted receipt with an "Honest mapping" stamp.

import { useEffect, useState } from "react";
import { getCategorisedSummary } from "../api.js";

// Turn pence into "£1,234.56"
const pounds = (pence) =>
  (pence / 100).toLocaleString("en-GB", { style: "currency", currency: "GBP" });

// The receipt lines, in order: [label, key in by_method]
const METHOD_ROWS = [
  ["By card code", "mcc"],
  ["By shop name", "keyword"],
  ["By bank label", "bank_category"],
  ["By AI", "llm"],
  ["Unknown", "unmapped"],
];

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

  if (error) return <section className="card">{error}</section>;
  if (!summary) return <section className="card">Loading…</section>;

  const spend = summary.spend_pence ?? 0;
  const categorised = summary.categorised_pence ?? 0;
  const methods = summary.by_method ?? {};

  // Percentage of spending we put into a category
  const pct = spend ? (categorised / spend) * 100 : 100;
  const pctText = pct >= 99.95 ? "100%" : `${pct.toFixed(1)}%`;

  return (
    <section className="card receipt">
      <span className="receipt-stamp" aria-hidden="true">
        HONEST
        <br />
        MAPPING
      </span>

      <h2>How much we could categorise</h2>
      <div className="receipt-big">{pctText}</div>
      <p className="receipt-text">
        {pounds(categorised)} of {pounds(spend)} spending sorted into the 12 ONS categories.
      </p>

      <div className="receipt-lines">
        {METHOD_ROWS.map(([label, key]) => (
          <div className="receipt-line" key={key}>
            <span>{label}</span>
            <span className="receipt-dots" />
            <span>{(methods[key] ?? 0).toLocaleString("en-GB")}</span>
          </div>
        ))}
      </div>

      <style>{`
        .receipt {
          transform: rotate(-1.2deg);
          border-radius: 6px;
          padding-right: 150px;
        }
        .receipt h2 { font-size: 1.5rem; }
        .receipt-stamp {
          position: absolute; top: 26px; right: 26px;
          width: 104px; height: 104px;
          border: 3px dashed var(--pink);
          border-radius: 50%;
          display: flex; align-items: center; justify-content: center;
          text-align: center;
          color: var(--pink);
          font-family: "Fredoka", sans-serif;
          font-weight: 700; font-size: 0.85rem; letter-spacing: 1.5px; line-height: 1.2;
          transform: rotate(-14deg);
        }
        .receipt-big {
          font-family: "Fredoka", sans-serif;
          font-weight: 700;
          font-size: clamp(3rem, 7vw, 4.5rem);
          line-height: 1;
          color: var(--pink);
        }
        .receipt-text { font-weight: 600; margin: 10px 0 14px; }
        .receipt-lines {
          border-top: 3px dotted var(--ink);
          padding-top: 12px;
          margin-right: -120px;
          display: flex; flex-direction: column; gap: 8px;
          font-weight: 700; font-size: 0.95rem;
        }
        .receipt-line { display: flex; align-items: baseline; gap: 6px; }
        .receipt-dots { flex: 1; border-bottom: 2px dotted #c9a9a6; transform: translateY(-4px); }
        @media (max-width: 760px) {
          .receipt { padding-right: 20px; }
          .receipt-stamp { position: static; margin-bottom: 10px; }
          .receipt-lines { margin-right: 0; }
        }
      `}</style>
    </section>
  );
}