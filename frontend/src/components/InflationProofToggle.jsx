// Owner: Person 4
// One switch: "Inflation-proof my savings". Shows the monthly top-up when on.

import { useEffect, useState } from "react";
import { getPersonalRate, setInflationProof } from "../api.js";

const pounds = (pence) => `£${(pence / 100).toFixed(2)}`;

export default function InflationProofToggle({ accountId }) {
  const [enabled, setEnabled] = useState(false);
  const [topUp, setTopUp] = useState(null); // suggested amount, in pence
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  // Load the suggested top-up whenever the persona changes
  useEffect(() => {
    setEnabled(false);
    setTopUp(null);
    setError(null);
    getPersonalRate(accountId)
      .then((data) => setTopUp(data.suggested_monthly_top_up_pence))
      .catch((e) => setError(e.message));
  }, [accountId]);

  async function toggle() {
    setSaving(true);
    setError(null);
    try {
      const result = await setInflationProof(accountId, !enabled);
      setEnabled(result.enabled);
      if (result.enabled) setTopUp(result.monthly_top_up_pence);
    } catch (e) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="card">
      <h2>Inflation-proof my savings</h2>

      {topUp === null && !error && <p>Loading…</p>}

      {topUp !== null && topUp === 0 && (
        <p>Your savings interest already beats your inflation rate. Nothing to top up.</p>
      )}

      {topUp !== null && topUp > 0 && (
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