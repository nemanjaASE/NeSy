import { useEffect, useState } from "react";

type MetricCardProps = {
  countTo?: number;
  label: string;
  suffix?: string;
  tone?: "blue" | "teal" | "violet";
  value: string;
};

function formatMetricValue(value: number, suffix = ""): string {
  if (value >= 1000) {
    return `${Math.floor(value / 1000)}k${suffix}`;
  }

  return `${value}${suffix}`;
}

export function MetricCard({
  countTo,
  label,
  suffix,
  tone = "blue",
  value,
}: MetricCardProps) {
  const [animatedValue, setAnimatedValue] = useState(0);

  useEffect(() => {
    if (!countTo) {
      return;
    }

    const targetValue = countTo;
    const duration = 2200;
    const start = performance.now();
    let frameId = 0;

    function tick(now: number) {
      const progress = Math.min((now - start) / duration, 1);
      const easedProgress = 1 - Math.pow(1 - progress, 3);
      const currentValue = Math.round(targetValue * easedProgress);

      setAnimatedValue(currentValue);

      if (progress < 1) {
        frameId = requestAnimationFrame(tick);
      }
    }

    frameId = requestAnimationFrame(tick);

    return () => cancelAnimationFrame(frameId);
  }, [countTo]);

  const displayValue = countTo
    ? formatMetricValue(animatedValue, suffix)
    : value;

  return (
    <article className={`metric-card metric-card-${tone}`}>
      <span>{label}</span>
      <div>
        <strong>{displayValue}</strong>
      </div>
    </article>
  );
}
