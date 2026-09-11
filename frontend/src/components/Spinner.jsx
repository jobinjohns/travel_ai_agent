// components/Spinner.jsx
// ---------------------------------------------------------
// A small spinning indicator with a label, shown while the backend
// is running the full agent graph (a few seconds, since it makes
// real LLM calls).
// ---------------------------------------------------------
export default function Spinner({ label }) {
  return (
    <div className="flex items-center gap-3 text-ink/70 font-mono text-sm">
      <span className="w-4 h-4 border-2 border-signal border-t-transparent rounded-full animate-spin" />
      {label}
    </div>
  );
}
