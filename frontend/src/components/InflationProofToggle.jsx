// Owner: Person 4
// One switch: "Inflation-proof my savings". Shows the monthly top-up when on.
// On load it asks the backend whether inflation-proofing is already on,
// so the button shows the real state after a page refresh.

import { useEffect, useState } from "react";
import { getInflationProof, getPersonalRate, setInflationProof } from "../api.js";

const pounds = (pence) => `£${(pence / 100).toFixed(2)}`;

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
    <section className="card">
      <h2>Inflation-proof my savings</h2>

      {topUp === null && !error && <p>Loading…</p>}

      {topUp === 0 && !enabled && <p style={{ marginTop: 0 }}>{zeroTopUpMessage()}</p>}

      {showButton && (
        <>
          <p style={{ marginTop: 0 }}>
            {enabled
              ? `On: ${pounds(topUp)} moves into your Inflation-proof Space every month.`
              : `Add ${pounds(topUp)} a month so your savings keep their value at your rate.`}
          </p>
          <button
            onClick={toggle}
            disabled={saving}
            style={{
              padding: "10px 18px",
              borderRadius: 999,
              border: "none",
              cursor: saving ? "wait" : "pointer",
              fontWeight: 600,
              color: "white",
              background: enabled ? "var(--muted)" : "var(--accent)",
            }}
          >
            {saving ? "Saving…" : enabled ? "Turn off" : "Turn on"}
          </button>
        </>
      )}

      {error && <p style={{ color: "var(--bad)" }}>Something went wrong: {error}</p>}
    </section>
  );
}