// components/StatusChip.jsx
// ---------------------------------------------------------
// A small colored label for a trace step's outcome — styled like an
// airport departures-board status (ON TIME / DELAYED), reused here
// for our own agent decisions.
// ---------------------------------------------------------
const STYLES = {
  request_understood: "bg-signal/10 text-signal",
  options_found: "bg-signal/10 text-signal",
  within_budget: "bg-taxiway/10 text-taxiway",
  over_budget: "bg-beacon/20 text-amber-700",
  best_effort: "bg-approach/10 text-approach",
  itinerary_ready: "bg-taxiway/10 text-taxiway",
};

export default function StatusChip({ decision }) {
  const style = STYLES[decision] || "bg-ink/10 text-ink";
  return (
    <span className={`inline-block px-2 py-0.5 rounded font-mono text-xs font-medium uppercase tracking-wide ${style}`}>
      {decision.replace(/_/g, " ")}
    </span>
  );
}
