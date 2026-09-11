// components/TraceTimeline.jsx
// ---------------------------------------------------------
// Renders the agentic AI trace as a "departures board" style log:
// one row per agent decision, with a mono timestamp, the agent name,
// a colored status chip, and the reasoning. For the three search
// agents, instead of just a count and one generic link, each ACTUAL
// option found is listed with its own cost and its own link — the
// real detail, not just a pointer to go look elsewhere.
// ---------------------------------------------------------
import { ExternalLink } from "lucide-react";
import StatusChip from "./StatusChip";

function formatTime(iso) {
  const d = new Date(iso);
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

export default function TraceTimeline({ steps }) {
  return (
    <div className="divide-y divide-ink/10">
      {steps.map((step, i) => (
        <div
          key={`${step.node}-${i}`}
          className="py-3 flex flex-col sm:flex-row sm:items-start gap-1 sm:gap-4 animate-fadeInUp"
          style={{ animationDelay: `${i * 70}ms` }}
        >
          <span className="font-mono text-xs text-ink/40 sm:w-20 shrink-0 pt-0.5">
            {formatTime(step.timestamp)}
          </span>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-mono text-xs font-semibold text-ink/70 uppercase tracking-wide">
                {step.node.replace(/_/g, " ")}
              </span>
              <StatusChip decision={step.decision} />
            </div>
            <p className="text-sm text-ink/80 mt-1">{step.reasoning}</p>

            {/* Itemized options: each thing this agent actually found,
                with its real cost and its own link */}
            {step.options && step.options.length > 0 && (
              <ul className="mt-2 space-y-1">
                {step.options.map((opt) => (
                  <li
                    key={opt.name}
                    className="flex items-center justify-between gap-3 text-xs bg-paper rounded-lg px-2.5 py-1.5"
                  >
                    <span className="text-ink/80 font-medium truncate">{opt.name}</span>
                    <span className="flex items-center gap-2 shrink-0">
                      <span className="font-mono text-ink/60">{opt.price_display}</span>
                      <a
                        href={opt.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-signal hover:text-signal-dark inline-flex items-center"
                        aria-label={`View ${opt.name}`}
                      >
                        <ExternalLink size={12} />
                      </a>
                    </span>
                  </li>
                ))}
              </ul>
            )}

            {/* Fallback single link, for any step that isn't one of
                the itemized search agents */}
            {step.link && (
              <a
                href={step.link}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-xs text-signal hover:text-signal-dark mt-1 font-medium"
              >
                View options <ExternalLink size={12} />
              </a>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
