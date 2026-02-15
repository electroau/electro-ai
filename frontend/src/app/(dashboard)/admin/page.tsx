export default function AdminPage() {
  return (
    <section className="card">
      <h1>Admin Panel</h1>
      <p>Manage user roles and compliance settings.</p>
      <div className="grid">
        <article className="card">
          <h3>Role Controls</h3>
          <p>Promote or demote users between Employee and Admin.</p>
        </article>
        <article className="card">
          <h3>Policy Settings</h3>
          <p>Configure retention, audit policies, and access restrictions.</p>
        </article>
      </div>
    </section>
  );
}
