import { useEffect, useMemo, useState } from "react";

type RotationKey = "pricing" | "hold" | "25" | "50" | "75" | "reset";
type RotationMap = Record<RotationKey, string>;

type ColorMeta = {
  name: string;
  hex: string;
};

const COLOR_META: Record<string, ColorMeta> = {
  B: { name: "Blue", hex: "#1D4ED8" },
  Y: { name: "Yellow", hex: "#FACC15" },
  O: { name: "Orange", hex: "#EA580C" },
  R: { name: "Red", hex: "#DC2626" },
  G: { name: "Green", hex: "#059669" },
  L: { name: "Lavender", hex: "#A855F7" },
  W: { name: "White", hex: "#E5E7EB" },
};

const ROTATION_ORDER: RotationKey[] = [
  "pricing",
  "hold",
  "25",
  "50",
  "75",
  "reset",
];

const STATUS_DESCRIPTION: Record<RotationKey, string> = {
  pricing: "Active tags on the floor this week.",
  hold: "Items waiting a week before the first markdown.",
  "25": "First markdown: 25% off tag color listed.",
  "50": "Second markdown: 50% off tag color listed.",
  "75": "Third markdown: 75% off tag color listed.",
  reset: "Final step before tags cycle back into hold.",
};

type ApiResponse = {
  date: string;
  color_rotations: RotationMap;
};

type QueueItem = {
  handle: string;
  title: string;
  classification: string;
  color: string;
  quantity: number;
};

export type ColorWheelProps = {
  initialDate?: string;
};

const formatDateInput = (value: string | undefined) => {
  if (!value) {
    return new Date().toISOString().slice(0, 10);
  }
  return value;
};

export default function ColorWheel({ initialDate }: ColorWheelProps) {
  const [selectedDate, setSelectedDate] = useState(
    formatDateInput(initialDate)
  );
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(
          `/pricing/update_pos/color_wheel/?format=json&date=${selectedDate}`,
          {
            credentials: "include",
            headers: { Accept: "application/json" },
          }
        );
        if (!response.ok) {
          throw new Error("Unable to load color wheel data.");
        }
        const json: ApiResponse = await response.json();
        if (isMounted) {
          setData(json);
        }
      } catch (err) {
        if (isMounted) {
          setError(err instanceof Error ? err.message : "Unexpected error");
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };
    fetchData();
    return () => {
      isMounted = false;
    };
  }, [selectedDate]);

  const queuePreview = useMemo(() => {
    if (!data) return [];
    return ROTATION_ORDER.map((key) => ({
      key,
      colorCode: data.color_rotations[key],
      meta: COLOR_META[data.color_rotations[key]] ?? {
        name: data.color_rotations[key],
        hex: "#CBD5F5",
      },
      description: STATUS_DESCRIPTION[key],
    }));
  }, [data]);

  const mockQueue: QueueItem[] = [
    {
      handle: "furniture-sofa",
      title: "Mid-Century Sofa",
      classification: "Furniture",
      color: "pricing",
      quantity: 12,
    },
    {
      handle: "electronics-laptop",
      title: "Refurbished Laptop Lot",
      classification: "Electronics",
      color: "hold",
      quantity: 6,
    },
    {
      handle: "housewares-mix",
      title: "Assorted Housewares Bin",
      classification: "Housewares",
      color: "25",
      quantity: 18,
    },
    {
      handle: "seasonal-holiday",
      title: "Holiday Decor Pallet",
      classification: "Seasonal",
      color: "50",
      quantity: 10,
    },
    {
      handle: "computers-periph",
      title: "Computer Peripherals Box",
      classification: "Computers",
      color: "75",
      quantity: 22,
    },
    {
      handle: "textiles-clothing",
      title: "Clothing Rack",
      classification: "Textiles",
      color: "reset",
      quantity: 30,
    },
  ];

  return (
    <section className="cw-panel">
      <header className="cw-header">
        <div>
          <h2>Color Wheel</h2>
          <p>Track this week&apos;s tagging color and markdown queue.</p>
        </div>
        <label className="cw-date-picker">
          <span>Week of</span>
          <input
            type="date"
            value={selectedDate}
            onChange={(event) => setSelectedDate(event.target.value)}
          />
        </label>
      </header>

      {loading && (
        <div className="cw-state-text" role="status">
          Loading color assignments…
        </div>
      )}
      {error && (
        <div className="cw-state-text cw-error" role="alert">
          {error}
        </div>
      )}

      {data && (
        <>
          <div className="cw-current">
            <strong>Current pricing color</strong>
            <div className="cw-current-chip">
              <span
                className="cw-swatch"
                style={{
                  backgroundColor:
                    COLOR_META[data.color_rotations.pricing]?.hex ??
                    "var(--cw-fallback)",
                }}
              />
              <div>
                <div className="cw-chip-label">
                  {COLOR_META[data.color_rotations.pricing]?.name ??
                    data.color_rotations.pricing}
                </div>
                <small>
                  Tag code: {data.color_rotations.pricing} • Effective{" "}
                  {data.date}
                </small>
              </div>
            </div>
            <p className="cw-instructions">
              Apply this color to all new barcodes. The queue below shows how
              tags advance as weeks progress so you can confirm markdown signage
              on the floor.
            </p>
          </div>

          <div className="cw-queue-grid">
            {queuePreview.map((item) => (
              <article key={item.key} className="cw-queue-card">
                <div className="cw-status">
                  <span className="cw-status-label">{item.key.toUpperCase()}</span>
                  <span className="cw-status-desc">{item.description}</span>
                </div>
                <div className="cw-swatch-row">
                  <span
                    className="cw-swatch large"
                    style={{ backgroundColor: item.meta.hex }}
                  />
                  <div>
                    <div className="cw-color-name">{item.meta.name}</div>
                    <small>Tag code: {item.colorCode}</small>
                  </div>
                </div>
              </article>
            ))}
          </div>

          <div className="cw-footer-note">
            <h3>How to read this queue</h3>
            <p>
              Items move down this queue each week. If you see a tag on the
              floor, match its color code to this list to understand whether it
              should be full price or discounted (25%, 50%, 75%) or ready for
              reset.
            </p>
          </div>

          <div className="cw-product-queue">
            <div className="cw-product-queue-header">
              <div>
                <h3>Product Queue Preview</h3>
                <p>Sample of items currently aligned with the color schedule.</p>
              </div>
              <button type="button" className="cw-expand">
                Expand
              </button>
            </div>
            <div className="cw-product-list">
              {mockQueue.slice(0, 4).map((item) => (
                <article key={item.handle} className="cw-product-card">
                  <div>
                    <p className="cw-product-title">{item.title}</p>
                    <p className="cw-product-meta">
                      <span>{item.classification}</span>
                      <span>Qty: {item.quantity}</span>
                    </p>
                  </div>
                  <span className={`cw-chip cw-chip-${item.color}`}>
                    {item.color.toUpperCase()}
                  </span>
                </article>
              ))}
            </div>
          </div>
        </>
      )}
    </section>
  );
}
