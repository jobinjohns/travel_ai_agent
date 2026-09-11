// pages/Landing.jsx
// ---------------------------------------------------------
// The landing page. The hero previews what actually happens when
// you use the product — a short strip of agent status chips — rather
// than a generic headline + stock art.
// ---------------------------------------------------------
import { Link } from "react-router-dom";
import Logo from "../components/Logo";

const PREVIEW_STEPS = [
  { label: "FLIGHT AGENT", status: "FOUND" },
  { label: "HOTEL AGENT", status: "FOUND" },
  { label: "BUDGET AGENT", status: "OPTIMIZING" },
  { label: "FINAL PLANNER", status: "CONFIRMED" },
];

const STATUS_COLOR = {
  FOUND: "text-signal",
  OPTIMIZING: "text-beacon",
  CONFIRMED: "text-taxiway",
};

export default function Landing() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="px-5 py-5">
        <Logo />
      </header>

      <main className="flex-1 flex items-center justify-center px-5 pb-16">
        <div className="max-w-md w-full">
          <div className="mb-8">
            <h1 className="font-display text-3xl sm:text-4xl font-semibold text-ink leading-tight">
              Multi-agent trip planning, orchestrated end to end.
            </h1>
            <p className="text-ink/60 mt-3">
              Specialist agents search flights, hotels, and activities, negotiate
              against your budget, and hand you a finished itinerary — with every
              decision shown along the way.
            </p>
          </div>

          {/* Signature element: a small "ops board" preview of a real run */}
          <div className="rounded-xl bg-ink text-white p-4 mb-8 font-mono text-xs space-y-2">
            {PREVIEW_STEPS.map((step) => (
              <div key={step.label} className="flex items-center justify-between">
                <span className="text-white/60 tracking-wide">{step.label}</span>
                <span className={STATUS_COLOR[step.status]}>{step.status}</span>
              </div>
            ))}
          </div>

          <div className="flex flex-col gap-3">
            <Link
              to="/login"
              className="w-full py-3 rounded-xl bg-signal text-white text-center font-medium hover:bg-signal-dark transition"
            >
              Sign in
            </Link>
            <Link
              to="/signup"
              className="w-full py-3 rounded-xl bg-white border border-ink/15 text-ink text-center font-medium hover:bg-ink/5 transition"
            >
              Create an account
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
