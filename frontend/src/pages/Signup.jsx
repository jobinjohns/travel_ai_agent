// pages/Signup.jsx
// ---------------------------------------------------------
// Account creation form. Country decides which currency the user
// sees everywhere else in the app (see backend/currency.py).
// ---------------------------------------------------------
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import Logo from "../components/Logo";

export default function Signup() {
  const { signup } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({ name: "", email: "", password: "", country: "", city: "" });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  function update(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (form.password.length < 6) {
      setError("Password needs to be at least 6 characters.");
      return;
    }

    setSubmitting(true);
    try {
      await signup({ ...form, city: form.city || null });
      navigate("/plan");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-5 py-10">
      <div className="max-w-sm w-full">
        <div className="mb-6">
          <Logo />
        </div>
        <div className="bg-white rounded-2xl shadow-sm border border-ink/10 p-6">
          <h1 className="font-display text-xl font-semibold text-ink mb-1">Create your account</h1>
          <p className="text-sm text-ink/50 mb-5">Your country sets which currency you'll see prices in.</p>

          <form onSubmit={handleSubmit} className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-ink/60 mb-1">Full name</label>
              <input
                required
                value={form.name}
                onChange={update("name")}
                className="w-full px-3 py-2.5 rounded-lg border border-ink/15 focus:outline-none focus:ring-2 focus:ring-signal/40 focus:border-signal"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-ink/60 mb-1">Email</label>
              <input
                type="email"
                required
                value={form.email}
                onChange={update("email")}
                className="w-full px-3 py-2.5 rounded-lg border border-ink/15 focus:outline-none focus:ring-2 focus:ring-signal/40 focus:border-signal"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-ink/60 mb-1">Password</label>
              <input
                type="password"
                required
                minLength={6}
                value={form.password}
                onChange={update("password")}
                className="w-full px-3 py-2.5 rounded-lg border border-ink/15 focus:outline-none focus:ring-2 focus:ring-signal/40 focus:border-signal"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-ink/60 mb-1">Country</label>
              <input
                required
                placeholder="e.g. India, USA"
                value={form.country}
                onChange={update("country")}
                className="w-full px-3 py-2.5 rounded-lg border border-ink/15 focus:outline-none focus:ring-2 focus:ring-signal/40 focus:border-signal"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-ink/60 mb-1">City (optional)</label>
              <input
                value={form.city}
                onChange={update("city")}
                className="w-full px-3 py-2.5 rounded-lg border border-ink/15 focus:outline-none focus:ring-2 focus:ring-signal/40 focus:border-signal"
              />
            </div>

            {error && <p className="text-sm text-approach">{error}</p>}

            <button
              type="submit"
              disabled={submitting}
              className="w-full py-2.5 rounded-lg bg-signal text-white font-medium hover:bg-signal-dark transition disabled:opacity-60"
            >
              {submitting ? "Creating account…" : "Sign up"}
            </button>
          </form>

          <p className="text-sm text-ink/50 mt-4 text-center">
            Already have an account?{" "}
            <Link to="/login" className="text-signal font-medium hover:text-signal-dark">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
