import { MetricCard } from "@/shared/ui/MetricCard/MetricCard";
import { Link } from "react-router-dom";
import { heroMetrics } from "../model/content";

export function HeroSection() {
  return (
    <div className="hero-copy">
      <h1>Clinical reasoning you can actually trust.</h1>

      <p className="hero-text">
        A smart diagnostic interface that doesn't hide behind a black box. Input
        patient symptoms, map them to standard medical ontologies, and get
        ranked, fully explainable disease candidates.
      </p>

      <div className="hero-actions">
        <Link className="primary-button" to="/diagnosis">
          Start diagnosis
        </Link>
        <a className="secondary-button" href="#workflow">
          See how it works
        </a>
      </div>

      <div className="metrics">
        {heroMetrics.map((metric) => (
          <MetricCard key={metric.label} {...metric} />
        ))}
      </div>
    </div>
  );
}
