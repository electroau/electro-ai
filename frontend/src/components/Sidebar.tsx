import Link from "next/link";

const navItems = [
  { href: "/", label: "Dashboard" },
  { href: "/upload", label: "File Upload" },
  { href: "/chat", label: "AI Assistant" },
  { href: "/logs", label: "Activity Logs" },
  { href: "/admin", label: "Admin" }
];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <h2>Electro AI</h2>
      <p style={{ opacity: 0.7 }}>Enterprise Intelligence</p>
      <nav>
        {navItems.map((item) => (
          <p key={item.href}>
            <Link href={item.href}>{item.label}</Link>
          </p>
        ))}
      </nav>
    </aside>
  );
}
