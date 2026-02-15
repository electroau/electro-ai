const logs = [
  "admin@electro.ai approved role update",
  "employee@electro.ai ingested Q4-grid-report.pdf",
  "admin@electro.ai exported audit logs"
];

export default function LogsPage() {
  return (
    <section className="card">
      <h1>Activity Logs</h1>
      <ul>
        {logs.map((entry) => <li key={entry}>{entry}</li>)}
      </ul>
    </section>
  );
}
