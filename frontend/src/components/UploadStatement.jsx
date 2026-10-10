// Owner: Person 2
// Upload a bank statement CSV, then switch to the new account.
// Data: uploadStatement(file, accountName) -> { account_id, inserted, summary }
// Call onImported(account_id) when done.

export default function UploadStatement({ onImported }) {
  // TODO(Person 2)
  void onImported;
  return (
    <section className="card">
      <h2>Try it with your own statement</h2>
      <div className="todo">TODO(Person 2): CSV upload</div>
    </section>
  );
}
