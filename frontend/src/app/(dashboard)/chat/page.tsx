export default function ChatPage() {
  return (
    <section className="card">
      <h1>AI Assistant</h1>
      <p>Ask organization-specific questions to the assistant.</p>
      <textarea className="textarea" rows={6} placeholder="How can I reduce transformer maintenance downtime?" />
      <button className="button" style={{ marginTop: 12 }}>Send</button>
    </section>
  );
}
