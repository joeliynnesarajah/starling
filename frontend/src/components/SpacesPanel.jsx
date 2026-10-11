// Owner: Person 1
// The savings Space balance, its monthly top-up, and a "Simulate next month"
// button that makes the balance visibly go up.
// Data: getSpaces(accountId), simulateNextMonth()

import { useCallback, useEffect, useState } from "react";
import { getSpaces, simulateNextMonth } from "../api.js";

const pounds = (pence) =>
  (pence / 100).toLocaleString("en-GB", { style: "currency", currency: "GBP" });

export default function SpacesPanel({ accountId }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [lastRun, setLastRun] = useState(null); // response from simulateNextMonth
  const [busy, setBusy] = useState(false);

  const load = useCallback(
    () => getSpaces(accountId).then(setData).catch((e) => setError(e.message || "Could not load Spaces")),
    [accountId],
  );

  useEffect(() => {
    setData(null);
    setError(null);
    setLastRun(null);
    load();
  }, [load]);

  async function nextMonth() {
    setBusy(true);
    try {
      setLastRun(await simulateNextMonth());
      await load();
    } catch (e) {
      setError(e.message || "Could not simulate next month");
    } finally {
      setBusy(false);
    }
  }

  const title = <h2>Your Spaces</h2>;
  if (error) return <section className="card">{title}<p style={{ color: "var(--bad)" }}>{error}</p></section>;
  if (!data) return <section className="card">{title}<p>Loading…</p></section>;

  return (
    <section className="card">
      {title}

      {data.spaces.length === 0 ? (
        <p style={{ color: "var(--muted)" }}>No Spaces yet. Turn on inflation-proofing to create one.</p>
      ) : (
        data.spaces.map((space) => {
          const orders = data.standing_orders.filter((o) => o.space_id === space.id);
          const paidIn = lastRun?.ran
            .filter((r) => r.space_id === space.id)
            .reduce((sum, r) => sum + r.amount_pence, 0);
          return (
            <div key={space.id} style={{ marginBottom: 12 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
                <span>{space.name}</span>
                <strong style={{ fontSize: "1.4rem" }}>{pounds(space.balance_pence)}</strong>
              </div>
              {orders.map((o) => (
                <div key={o.id} style={{ color: "var(--muted)", fontSize: "0.9rem" }}>
                  {pounds(o.amount_pence)} {o.frequency} top-up, next on {o.next_run_date}
                </div>
              ))}
              {paidIn > 0 && (
                <div style={{ color: "var(--good)", fontSize: "0.9rem" }}>+{pounds(paidIn)} this month</div>
              )}
            </div>
          );
        })
      )}

      <div style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 8 }}>
        <button onClick={nextMonth} disabled={busy}>
          {busy ? "Simulating…" : "Simulate next month"}
        </button>
        {lastRun && <span style={{ color: "var(--muted)", fontSize: "0.9rem" }}>Today is {lastRun.today}</span>}
      </div>
    </section>
  );
}
