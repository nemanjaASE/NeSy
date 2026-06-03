import type { PropsWithChildren } from "react";
import { BackToTop } from "../BackToTop";
import "./AppShell.css";

export function AppShell({ children }: PropsWithChildren) {
  return (
    <main className="nesy-app">
      <div className="bg-wash" />
      <div className="bg-glow" />
      <div className="bg-grid" />
      <div className="page">{children}</div>
      <BackToTop />
    </main>
  );
}
