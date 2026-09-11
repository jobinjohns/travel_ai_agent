// pages/TripPlanner.jsx
// ---------------------------------------------------------
// The protected main page: a trip request form (origin -> destination),
// then the resulting itinerary (as a boarding-pass card) and the
// agent reasoning trace (as a departures-board timeline) once the
// backend responds.
// ---------------------------------------------------------
import { useState } from "react";
import { useAuth } from "../AuthContext";
import { api } from "../api";
import Navbar from "../components/Navbar";
import Spinner from "../components/Spinner";
import ItineraryTicket from "../components/ItineraryTicket";
import TraceTimeline from "../components/TraceTimeline";

export default function TripPlanner() {
  const { user, token } = useAuth();

  const [form, setForm] = useState({ origin: "", destination: "", start_date: "", end_date: "", budget_cap: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  function update(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    const budget_cap = parseFloat(form.budget_cap);

    // Client-side validation before hitting the network at all
    if (!form.origin || !form.destination || !form.start_date || !form.end_date || isNaN(budget_cap) || budget_cap <= 0) {
      setError("Please fill in where you're flying from, a destination, both dates, and a budget greater than 0.");
      return;
    }
    if (form.origin.trim().toLowerCase() === form.destination.trim().toLowerCase()) {
      setError("Origin and destination can't be the same place.");
      return;
    }
    if (new Date(form.end_date) < new Date(form.start_date)) {
      setError("End date can't be before the start date.");
      return;
    }

    setLoading(true);
    setResult(null);
    try {
      const data = await api.planTrip(
        {
          origin: form.origin,
          destination: form.destination,
          start_date: form.start_date,
          end_date: form.end_date,
          budget_cap,
        },
        token
      );
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const currencySymbol = user?.currency === "INR" ? "₹" : "$";

  return (
    <div className="min-h-screen">
      <Navbar />

      <main className="max-w-3xl mx-auto px-5 py-8 space-y-6">
        <div className="bg-white rounded-2xl shadow-sm border border-ink/10 p-6">
          <h1 className="font-display text-xl font-semibold text-ink mb-4">Plan your trip</h1>

          <form onSubmit={handleSubmit} className="grid sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-ink/60 mb-1">From</label>
              <input
                required
                value={form.origin}
                onChange={update("origin")}
                placeholder="e.g. Bangalore"
                className="w-full px-3 py-2.5 rounded-lg border border-ink/15 focus:outline-none focus:ring-2 focus:ring-signal/40 focus:border-signal"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-ink/60 mb-1">To</label>
              <input
                required
                value={form.destination}
                onChange={update("destination")}
                placeholder="e.g. Amsterdam"
                className="w-full px-3 py-2.5 rounded-lg border border-ink/15 focus:outline-none focus:ring-2 focus:ring-signal/40 focus:border-signal"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-ink/60 mb-1">Start date</label>
              <input
                type="date"
                required
                value={form.start_date}
                onChange={update("start_date")}
                className="w-full px-3 py-2.5 rounded-lg border border-ink/15 focus:outline-none focus:ring-2 focus:ring-signal/40 focus:border-signal"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-ink/60 mb-1">End date</label>
              <input
                type="date"
                required
                value={form.end_date}
                onChange={update("end_date")}
                className="w-full px-3 py-2.5 rounded-lg border border-ink/15 focus:outline-none focus:ring-2 focus:ring-signal/40 focus:border-signal"
              />
            </div>
            <div className="sm:col-span-2">
              <label className="block text-xs font-medium text-ink/60 mb-1">
                Budget cap ({currencySymbol})
              </label>
              <input
                type="number"
                required
                min="1"
                step="0.01"
                value={form.budget_cap}
                onChange={update("budget_cap")}
                className="w-full px-3 py-2.5 rounded-lg border border-ink/15 focus:outline-none focus:ring-2 focus:ring-signal/40 focus:border-signal"
              />
            </div>

            {error && <p className="sm:col-span-2 text-sm text-approach">{error}</p>}

            <div className="sm:col-span-2">
              <button
                type="submit"
                disabled={loading}
                className="w-full sm:w-auto px-6 py-2.5 rounded-lg bg-signal text-white font-medium hover:bg-signal-dark transition disabled:opacity-60"
              >
                {loading ? "Planning…" : "Plan my trip"}
              </button>
            </div>
          </form>
        </div>

        {loading && (
          <div className="bg-white rounded-2xl shadow-sm border border-ink/10 p-6">
            <Spinner label="Searching flights, hotels, and activities, then negotiating your budget…" />
          </div>
        )}

        {result && !loading && (
          <>
            <ItineraryTicket itinerary={result.itinerary} />

            <div className="bg-white rounded-2xl shadow-sm border border-ink/10 p-6">
              <h2 className="font-display text-lg font-semibold text-ink mb-1">Agent reasoning trace</h2>
              <p className="text-sm text-ink/50 mb-2">What each agent found and decided, in order.</p>
              <TraceTimeline steps={result.trace} />
            </div>
          </>
        )}
      </main>
    </div>
  );
}
