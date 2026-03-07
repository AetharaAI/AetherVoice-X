import { NavLink, Outlet } from "react-router-dom";

const navItems = [
  ["Dashboard", "/"],
  ["ASR Live", "/asr-live"],
  ["ASR File", "/asr-file"],
  ["TTS Live", "/tts-live"],
  ["TTS File", "/tts-file"],
  ["Triage", "/triage"],
  ["Sessions", "/sessions"],
  ["Models", "/models"],
  ["Metrics", "/metrics"]
] as const;

export function ShellLayout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <p>Aether Voice</p>
          <span>Voice infrastructure substrate</span>
        </div>
        <nav className="nav-grid">
          {navItems.map(([label, path]) => (
            <NavLink key={path} to={path} className={({ isActive }) => `nav-card${isActive ? " active" : ""}`}>
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
