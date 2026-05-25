import { AppShell } from "@/shared/ui/AppShell";
import { HeroSection } from "./ui/HeroSection";
import { SiteFooter } from "./ui/SiteFooter";
import { SiteHeader } from "./ui/SiteHeader";
import { WorkflowSection } from "./ui/WorkflowSection";
import { WorkspacePreview } from "./ui/WorkspacePreview";
import "./HomePage.css";

export function HomePage() {
  return (
    <AppShell>
      <SiteHeader />
      <section className="hero">
        <HeroSection />
        <WorkspacePreview />
      </section>
      <WorkflowSection />
      <SiteFooter />
    </AppShell>
  );
}
