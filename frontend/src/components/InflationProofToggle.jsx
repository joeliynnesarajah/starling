// Owner: Person 4
// One switch: "Inflation-proof my savings". Shows the monthly top-up when on.
// Data: setInflationProof(accountId, enabled), suggested_monthly_top_up_pence from getPersonalRate

export default function InflationProofToggle({ accountId }) {
  // TODO(Person 4)
  return (
    <section className="card">
      <h2>Inflation-proof my savings</h2>
      <div className="todo">TODO(Person 4): toggle for {accountId}</div>
    </section>
  );
}
