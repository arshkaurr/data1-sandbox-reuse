import { useCallback, useEffect, useMemo, useState } from "react";
import CounterPanel, { type CounterCardProps } from "./CounterPanel";

type HourlyRow = {
  label: string;
  count: number;
};

type VisitorsResponse = {
  location: string;
  capacity: number;
  current: number;
  total_today: number;
  hourly: HourlyRow[];
};

type VisitorsDashboardProps = {
  endpoint: string;
  submitUrl: string;
  csrfToken: string;
  location: string;
  userEmail?: string;
  homeUrl?: string;
};

export default function VisitorsDashboard({
  endpoint,
  submitUrl,
  csrfToken,
  location,
  userEmail,
  homeUrl,
}: VisitorsDashboardProps) {
  const [data, setData] = useState<VisitorsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [delta, setDelta] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(endpoint, {
        credentials: "include",
        headers: { Accept: "application/json" },
      });
      if (!response.ok) {
        throw new Error("Unable to load visitor data.");
      }
      const payload: VisitorsResponse = await response.json();
      setData(payload);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error loading data.");
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const adjustDelta = (change: number) => {
    setDelta((prev) => {
      const next = prev + change;
      if (next > 10) return 10;
      if (next < -10) return -10;
      return next;
    });
  };

  const handleSubmit = async () => {
    if (!delta) {
      setStatusMessage("Select a change before submitting.");
      return;
    }
    setSubmitting(true);
    setStatusMessage(null);
    try {
      const formData = new FormData();
      formData.append("location", location);
      formData.append("count", String(delta));
      const response = await fetch(submitUrl, {
        method: "POST",
        credentials: "include",
        headers: {
          "X-CSRFToken": csrfToken,
          Accept: "application/json",
        },
        body: formData,
      });
      if (!response.ok) {
        throw new Error("Unable to submit change.");
      }
      setStatusMessage("Update submitted. Refreshing counts…");
      setDelta(0);
      await fetchData();
    } catch (err) {
      setStatusMessage(err instanceof Error ? err.message : "Submission failed.");
    } finally {
      setSubmitting(false);
    }
  };

  const counterItems: CounterCardProps[] = useMemo(() => {
    if (!data) return [];
    return [
      {
        label: "Maximum Capacity",
        value: data.capacity,
        caption: `Location: ${data.location}`,
        highlight: "default",
      },
      {
        label: "Visitors On Floor",
        value: data.current,
        caption: "Live count",
        max: data.capacity,
        highlight: data.current >= data.capacity * 0.9 ? "warning" : "accent",
      },
      {
        label: "Total Visitors Today",
        value: data.total_today,
        caption: "Entries since open",
        highlight: "default",
      },
    ];
  }, [data]);

  return (
    <section className="vd-shell">
      <header className="vd-header">
        <div>
          <p className="vd-eyebrow">Capacity dashboard</p>
          <h1>{location} Visitors</h1>
          {userEmail && (
            <p className="vd-user">
              Signed in as <strong>{userEmail}</strong>
              {homeUrl ? (
                <>
                  {" "}
                  <a href={homeUrl} className="vd-link">
                    (switch)
                  </a>
                </>
              ) : null}
            </p>
          )}
        </div>
        <button className="vd-refresh" onClick={fetchData} disabled={loading}>
          Refresh
        </button>
      </header>

      {loading && <div className="vd-state">Loading latest counts…</div>}
      {error && <div className="vd-state vd-error">{error}</div>}

      {data && (
        <>
          <CounterPanel items={counterItems} />

          <div className="vd-controls">
            <div>
              <p className="vd-control-label">Adjust count</p>
              <div className="vd-stepper">
                <button type="button" onClick={() => adjustDelta(-1)} disabled={delta <= -10 || submitting}>
                  −
                </button>
                <span className="vd-stepper-value">{delta}</span>
                <button type="button" onClick={() => adjustDelta(1)} disabled={delta >= 10 || submitting}>
                  +
                </button>
              </div>
              <p className="vd-hint">Range −10 to +10 per submission</p>
            </div>
            <div className="vd-actions">
              <button
                type="button"
                className="vd-submit"
                onClick={handleSubmit}
                disabled={submitting || delta === 0}
              >
                {submitting ? "Submitting…" : "Submit Change"}
              </button>
              {statusMessage && <p className="vd-status">{statusMessage}</p>}
            </div>
          </div>

          <div className="vd-hourly">
            <div className="vd-hourly-header">
              <h2>Visitors by Hour (Today)</h2>
              <p>Track peak times to align staffing and signage.</p>
            </div>
            {data.hourly && data.hourly.length > 0 ? (
              <table className="vd-hourly-table">
                <thead>
                  <tr>
                    <th>Hour</th>
                    <th>Visitors Entered</th>
                  </tr>
                </thead>
                <tbody>
                  {data.hourly.map((row) => (
                    <tr key={row.label}>
                      <td>{row.label}</td>
                      <td>{row.count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="vd-state">No visitor entries recorded yet today.</div>
            )}
          </div>
        </>
      )}
    </section>
  );
}
