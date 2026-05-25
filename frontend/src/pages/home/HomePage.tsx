import { AppShell } from "@/shared/ui/AppShell";
import { HeroSection } from "./ui/HeroSection";
import { HeroVisualCarousel } from "./ui/HeroVisualCarousel";
import { SiteFooter } from "./ui/SiteFooter";
import { SiteHeader } from "./ui/SiteHeader";
import { WorkspacePreview } from "./ui/WorkspacePreview";
import "./HomePage.css";

export function HomePage() {
  return (
    <AppShell>
      <SiteHeader />
      <section className="hero">
        <div className="hero-top">
          <HeroSection />
          <HeroVisualCarousel />
        </div>
        <WorkspacePreview />
      </section>
      <SiteFooter />
    </AppShell>
  );
}
