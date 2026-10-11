// Owner: Person 4
// One switch: "Inflation-proof my savings". Shows the monthly top-up when on.
// On load it asks the backend whether inflation-proofing is already on,
// so the button shows the real state after a page refresh.

import { useEffect, useState } from "react";
import { getInflationProof, getPersonalRate, setInflationProof } from "../api.js";

const pounds = (pence) => `£${(pence / 100).toFixed(2)}`;

// A little stack of coins with a heart, drawn in the same style as the piggy
function CoinStack() {
  return (
    <svg viewBox="0 0 90 90" width="84" aria-hidden="true">
      <g stroke="#4a2c2a" strokeWidth="3.5">
        <ellipse cx="42" cy="74" rx="32" ry="10" fill="#ffe17a" />
        <rect x="10" y="62" width="64" height="12" fill="#ffe17a" stroke="none" />
        <path d="M10 62v12M74 62v12" />
        <ellipse cx="42" cy="62" rx="32" ry="10" fill="#ffe17a" />
        <rect x="10" y="50" width="64" height="12" fill="#ffe17a" stroke="none" />
        <path d="M10 50v12M74 50v12" />
        <ellipse cx="42" cy="50" rx="32" ry="10" fill="#ffe17a" />
        <path d="M42 36c-6-4-10-7-10-11 0-3 2-5 5-5 2 0 4 1 5 3 1-2 3-3 5-3 3 0 5 2 5 5 0 4-4 7-10 11z" fill="#e8336d" />
      </g>
      <text x="70" y="22" fontSize="18" fill="#4a2c2a">✦</text>
    </svg>
  );
}

export default function InflationProofToggle({ accountId }) {
  const [enabled, setEnabled] = useState(false);
  const [topUp, setTopUp] = useState(null); // amount in pence: the active standing order if on, else the suggestion
  const [rate, setRate] = useState(null); // personal inflation rate, to explain a £0 top-up
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  // Whenever the persona changes, load the suggestion AND the current on/off state
  useEffect(() => {
    let cancelled = false;
    setEnabled(false);
    setTopUp(null);
    setRate(null);
    setError(null);

    Promise.all([getPersonalRate(accountId), getInflationProof(accountId)])
      .then(([rateData, status]) => {
        if (cancelled) return;
        setRate(rateData.personal_rate);
        setEnabled(status.enabled);
        // If it's already on, show the amount actually being paid in
        setTopUp(status.enabled ? status.monthly_top_up_pence : rateData.suggested_monthly_top_up_pence);
      })
      .catch((e) => !cancelled && setError(e.message));

    return () => {
      cancelled = true;
    };
  }, [accountId]);

  async function toggle() {
    setSaving(true);
    setError(null);
    try {
      const result = await setInflationProof(accountId, !enabled);
      setEnabled(result.enabled);
      if (result.enabled) {
        setTopUp(result.monthly_top_up_pence);
      } else {
        // Switched off: go back to showing the suggestion
        const rateData = await getPersonalRate(accountId);
        setTopUp(rateData.suggested_monthly_top_up_pence);
      }
    } catch (e) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  }

  // Why the top-up might be £0. Only claim "interest beats inflation"
  // when we actually have a rate; otherwise there's no spending to go on.
  function zeroTopUpMessage() {
    if (!rate) {
      return "We need more spending history before we can suggest a top-up.";
    }
    return "No top-up needed right now. Either your savings interest beats your inflation rate, or there's nothing saved yet.";
  }

  // Show the button whenever there's something to turn on, or it's already on
  const showButton = topUp !== null && (topUp > 0 || enabled);

  return (
    <section className="card" style={{ display: "flex", gap: 24, alignItems: "center" }}>
      <CoinStack />
      <div style={{ flex: 1 }}>
      <h2>Inflation-proof my savings</h2>

      {topUp === null && !error && <p>Loading…</p>}

      {topUp === 0 && !enabled && <p style={{ marginTop: 0 }}>{zeroTopUpMessage()}</p>}

      {showButton && (
        <>
          <p style={{ marginTop: 0, fontWeight: 600, lineHeight: 1.6 }}>
            {enabled ? (
              <>On: <span className="highlight">{pounds(topUp)} a month</span> moves into your Inflation-proof Space.</>
            ) : (
              <>Add <span className="highlight">{pounds(topUp)} a month</span> so your savings keep their value at your rate.</>
            )}
          </p>
          <button
            className={enabled ? "btn btn-outline" : "btn"}
            onClick={toggle}
            disabled={saving}
          >
            {saving ? "Saving…" : enabled ? "Turn off" : "Turn on"}
          </button>
        </>
      )}

      {error && <p style={{ color: "var(--bad)" }}>Something went wrong: {error}</p>}
      </div>
    </section>
  );
}
