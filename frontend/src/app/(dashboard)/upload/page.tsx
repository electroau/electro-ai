export default function UploadPage() {
  return (
    <section className="card">
      <h1>File Upload Center</h1>
      <p>Upload enterprise PDF/Excel documents for ingestion.</p>
      <input className="input" type="file" />
      <button className="button" style={{ marginTop: 12 }}>Ingest File</button>
    </section>
  );
}
