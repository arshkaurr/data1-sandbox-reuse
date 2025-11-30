export type CounterCardProps = {
  label: string;
  value: number | null | undefined;
  caption?: string;
  max?: number;
  highlight?: "default" | "accent" | "warning";
  unit?: string;
};

export const CounterCard = ({
  label,
  value,
  caption,
  max,
  highlight = "default",
  unit,
}: CounterCardProps) => {
  const safeValue = typeof value === "number" && !Number.isNaN(value) ? value : 0;
  const percent = typeof max === "number" && max > 0 ? Math.min(100, Math.round((safeValue / max) * 100)) : null;
  const classes = ["vd-card"];
  if (highlight && highlight !== "default") {
    classes.push(`vd-card-${highlight}`);
  }

  return (
    <article className={classes.join(" ")}>
      <p className="vd-card-label">{label}</p>
      <div className="vd-card-value">
        {safeValue}
        {unit ? <span className="vd-card-unit">{unit}</span> : null}
      </div>
      {caption && <p className="vd-card-caption">{caption}</p>}
      {percent !== null && (
        <div className="vd-progress">
          <div className="vd-progress-track">
            <span className="vd-progress-bar" style={{ width: `${percent}%` }} />
          </div>
          <span className="vd-progress-label">{percent}% of capacity</span>
        </div>
      )}
    </article>
  );
};

export type CounterPanelProps = {
  items: CounterCardProps[];
};

export default function CounterPanel({ items }: CounterPanelProps) {
  return (
    <div className="vd-counter-grid">
      {items.map((item) => (
        <CounterCard key={item.label} {...item} />
      ))}
    </div>
  );
}
