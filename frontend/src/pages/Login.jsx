// pages/Login.jsx
// ---------------------------------------------------------
// Sign-in form. On success, saves the session (via AuthContext) and
// routes to the trip planner.
// ---------------------------------------------------------
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import Logo from "../components/Logo";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login({ email, password });
      navigate("/plan");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-5">
      <div className="max-w-sm w-full">
        <div className="mb-6">
          <Logo />
        </div>
        <div className="bg-white rounded-2xl shadow-sm border border-ink/10 p-6">
          <h1 className="font-display text-xl font-semibold text-ink mb-1">Sign in</h1>
          <p className="text-sm text-ink/50 mb-5">Welcome back — plan your next trip.</p>

          <form onSubmit={handleSubmit} className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-ink/60 mb-1">Email</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2.5 rounded-lg border border-ink/15 focus:outline-none focus:ring-2 focus:ring-signal/40 focus:border-signal"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-ink/60 mb-1">Password</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2.5 rounded-lg border border-ink/15 focus:outline-none focus:ring-2 focus:ring-signal/40 focus:border-signal"
              />
            </div>

            {error && <p className="text-sm text-approach">{error}</p>}

            <button
              type="submit"
              disabled={submitting}
              className="w-full py-2.5 rounded-lg bg-signal text-white font-medium hover:bg-signal-dark transition disabled:opacity-60"
            >
              {submitting ? "Signing in…" : "Sign in"}
            </button>
          </form>

          <p className="text-sm text-ink/50 mt-4 text-center">
            New here?{" "}
            <Link to="/signup" className="text-signal font-medium hover:text-signal-dark">
              Create an account
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
