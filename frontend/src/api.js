// api.js
// ---------------------------------------------------------
// A thin wrapper around fetch() that knows the API's base URL and
// attaches the signed-in user's JWT (when we have one) to every
// request, so components never repeat that logic themselves.
// ---------------------------------------------------------
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function request(path, { method = "GET", body, token } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    // Surface the backend's own error message (e.g. "Incorrect email
    // or password.") instead of a generic failure
    const message = data?.detail || "Something went wrong. Please try again.";
    throw new Error(message);
  }

  return data;
}

export const api = {
  signup: (payload) => request("/auth/signup", { method: "POST", body: payload }),
  login: (payload) => request("/auth/login", { method: "POST", body: payload }),
  planTrip: (payload, token) => request("/plan/", { method: "POST", body: payload, token }),
};
