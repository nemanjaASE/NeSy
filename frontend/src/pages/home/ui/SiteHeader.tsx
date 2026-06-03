import nesyLogo from "@/assets/nesy-logo.svg";
import { Link, useLocation } from "react-router-dom";
import { navItems } from "../model/content";

export function SiteHeader() {
  const location = useLocation();

  const isActive = (href: string) => {
    const [path, hash = ""] = href.split("#");

    if (path !== location.pathname) {
      return false;
    }

    if (!hash) {
      return location.hash === "";
    }

    return (
      location.hash === `#${hash}` ||
      (hash === "platform" && location.hash === "")
    );
  };

  return (
    <header className="topbar">
      <Link className="brand" to="/">
        <img className="brand-logo" src={nesyLogo} alt="NeSy" />
      </Link>

      <nav className="nav-links">
        {navItems.map((item) => (
          <Link
            className={isActive(item.href) ? "is-active" : undefined}
            key={item.label}
            to={item.href}
          >
            {item.label}
          </Link>
        ))}
      </nav>

      <div className="top-actions">
        <Link className="primary-link" to="/diagnosis">
          Launch
        </Link>
      </div>
    </header>
  );
}
