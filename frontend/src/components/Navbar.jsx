// components/Navbar.jsx
// ---------------------------------------------------------
// The persistent dark "control strip" shown on the trip-planner
// page: logo, who's signed in, which currency they're seeing, and
// a log-out button.
// ---------------------------------------------------------
import { LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import Logo from "./Logo";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/");
  }

  return (
    <header className="bg-ink text-white">
      <div className="max-w-3xl mx-auto px-5 py-4 flex items-center justify-between">
        <Logo light />
        <div className="flex items-center gap-4">
          <span className="hidden sm:block text-sm text-white/70 font-mono">
            {user?.name} · prices in {user?.currency}
          </span>
          <button
            onClick={handleLogout}
            className="flex items-center gap-1.5 text-sm text-white/80 hover:text-white transition"
          >
            <LogOut size={15} />
            Log out
          </button>
        </div>
      </div>
    </header>
  );
}
