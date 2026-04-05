import { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';

export default function Layout({ children }) {
  const [theme, setTheme] = useState(() => localStorage.getItem('gwa-theme') || 'dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('gwa-theme', theme);
  }, [theme]);

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="topbar-inner">
          <NavLink to="/" className="brand">
            <div className="brand-mark">GI</div>
            <div className="brand-text">
              <strong>Greenwash Auditor</strong>
              <span>Agentic ESG Integrity Lab</span>
            </div>
          </NavLink>

          <nav className="nav">
            <NavLink to="/" end className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
              Audit Intake
            </NavLink>
            <NavLink
              to="/report/adani"
              className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
            >
              Demo Report
            </NavLink>
            <NavLink
              to="/compare"
              className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
            >
              Compare
            </NavLink>
            <button
              type="button"
              className="theme-toggle"
              onClick={() => setTheme((current) => (current === 'dark' ? 'light' : 'dark'))}
              aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
            >
              <span>{theme === 'dark' ? 'Light' : 'Dark'}</span>
            </button>
          </nav>
        </div>
      </header>

      <main className="page-container">{children}</main>
    </div>
  );
}
