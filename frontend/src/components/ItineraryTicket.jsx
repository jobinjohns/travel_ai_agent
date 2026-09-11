// components/ItineraryTicket.jsx
// ---------------------------------------------------------
// Shows the final itinerary as a boarding-pass-style card: trip
// details on the left "stub," total price + budget status on the
// right, separated by a perforated divider (two circular notches
// colored to match the page background, cut into the card edge).
// ---------------------------------------------------------
import { Plane, Building2, MapPin, ExternalLink } from "lucide-react";

export default function ItineraryTicket({ itinerary }) {
  const isOverBudget = Boolean(itinerary.over_by_display);

  return (
    <div className="rounded-2xl bg-white shadow-sm border border-ink/10 overflow-hidden">
      <div
        className={`px-5 py-3 text-sm font-medium ${
          isOverBudget ? "bg-approach/10 text-approach" : "bg-taxiway/10 text-taxiway"
        }`}
      >
        {itinerary.message}
      </div>

      <div className="flex flex-col sm:flex-row">
        {/* Left stub: trip details */}
        <div className="flex-1 p-6 space-y-4">
          <div>
            <p className="text-xs font-mono uppercase tracking-wide text-ink/40">Route</p>
            <p className="font-display text-xl font-semibold text-ink">
              {itinerary.origin} <span className="text-ink/30">→</span> {itinerary.destination}
            </p>
            <p className="text-sm text-ink/50">{itinerary.dates}</p>
          </div>

          <div className="flex items-start gap-3">
            <Plane size={18} className="text-signal mt-0.5 shrink-0" />
            <div className="min-w-0">
              <p className="text-sm font-medium text-ink">{itinerary.flight.airline}</p>
              <p className="text-sm text-ink/60">{itinerary.flight.price_display}</p>
              <a
                href={itinerary.flight.link}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-xs text-signal hover:text-signal-dark font-medium"
              >
                View flights <ExternalLink size={11} />
              </a>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Building2 size={18} className="text-signal mt-0.5 shrink-0" />
            <div className="min-w-0">
              <p className="text-sm font-medium text-ink">{itinerary.hotel.name}</p>
              <p className="text-sm text-ink/60">{itinerary.hotel.price_display}</p>
              <a
                href={itinerary.hotel.link}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-xs text-signal hover:text-signal-dark font-medium"
              >
                View hotel <ExternalLink size={11} />
              </a>
            </div>
          </div>

          {itinerary.activities.length > 0 && (
            <div className="flex items-start gap-3">
              <MapPin size={18} className="text-signal mt-0.5 shrink-0" />
              <div className="min-w-0 space-y-1.5">
                {itinerary.activities.map((a) => (
                  <div key={a.name}>
                    <p className="text-sm font-medium text-ink">
                      {a.name} <span className="text-ink/50 font-normal">— {a.price_display}</span>
                    </p>
                    <a
                      href={a.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs text-signal hover:text-signal-dark font-medium"
                    >
                      More info <ExternalLink size={11} />
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Perforated divider */}
        <div className="relative hidden sm:block w-0 border-l-2 border-dashed border-ink/15">
          <span className="absolute -top-2.5 -left-2.5 w-5 h-5 rounded-full bg-paper" />
          <span className="absolute -bottom-2.5 -left-2.5 w-5 h-5 rounded-full bg-paper" />
        </div>
        <div className="sm:hidden border-t-2 border-dashed border-ink/15" />

        {/* Right stub: price + status */}
        <div className="sm:w-48 p-6 flex sm:flex-col justify-between sm:justify-center items-center sm:items-start gap-2 bg-paper/50">
          <div>
            <p className="text-xs font-mono uppercase tracking-wide text-ink/40">Budget cap</p>
            <p className="font-mono text-sm text-ink/70">{itinerary.budget_cap_display}</p>
          </div>
          <div>
            <p className="text-xs font-mono uppercase tracking-wide text-ink/40">Total</p>
            <p className="font-display text-2xl font-semibold text-ink">{itinerary.total_display}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
