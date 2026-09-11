// components/Logo.jsx
// ---------------------------------------------------------
// The plane-mark + wordmark, reused on every page.
// ---------------------------------------------------------
import { Plane } from "lucide-react";

export default function Logo({ light = false }) {
  return (
    <div className="flex items-center gap-2">
      <span className="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-beacon text-ink">
        <Plane size={16} strokeWidth={2.5} />
      </span>
      <span className={`font-display font-semibold tracking-tight ${light ? "text-white" : "text-ink"}`}>
        AI Travel Ops
      </span>
    </div>
  );
}
