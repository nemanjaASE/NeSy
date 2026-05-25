import type { PropsWithChildren } from "react";
import "./AppShell.css";

export function AppShell({ children }: PropsWithChildren) {
  return (
    <main className="nesy-app">
      <div className="bg-wash" />
      <div className="bg-glow" />
      <div className="page">{children}</div>
    </main>
  );
}
