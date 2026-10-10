// Owners: Person 3 (headline line) and Person 4 (your line)
// You vs the headline rate over the last 12 months.
// Data: getInflationHistory() for the headline, getPersonalHistory(accountId) for you.
// Colours: var(--you) and var(--headline) from styles.css
// Chart library: recharts (LineChart)

export default function HistoryChart({ accountId }) {
  // TODO(Person 3): headline line
  // TODO(Person 4): personal line
  return (
    <section className="card">
      <h2>You vs the headline</h2>
      <div className="todo">TODO(Person 3 + 4): history chart for {accountId}</div>
    </section>
  );
}
