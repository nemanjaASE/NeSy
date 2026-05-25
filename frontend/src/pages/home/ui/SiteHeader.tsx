import { navItems } from "../model/content";

export function SiteHeader() {
  return (
    <header className="topbar">
      <a className="brand" href="/">
        <div className="brand-mark">
          <svg
            width="28"
            height="28"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2.35"
          >
            <circle cx="12" cy="12" r="3" />
            <circle cx="19" cy="5" r="3" />
            <circle cx="5" cy="19" r="3" />
            <line x1="16.5" y1="7.5" x2="14.5" y2="9.5" />
            <line x1="9.5" y1="14.5" x2="7.5" y2="16.5" />
          </svg>
        </div>
        <span>
          <strong>NeSy</strong>
          <small>Diagnostic AI</small>
        </span>
      </a>

      <nav className="nav-links">
        {navItems.map((item) => (
          <a className={item === "Platform" ? "is-active" : undefined} href="/" key={item}>
            {item}
          </a>
        ))}
      </nav>

      <div className="top-actions">
        <a className="ghost-link" href="/">
          Sign in
        </a>
        <a className="primary-link" href="#workspace">
          Launch
        </a>
      </div>
    </header>
  );
}
