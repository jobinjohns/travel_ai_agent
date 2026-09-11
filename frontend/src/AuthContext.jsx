// AuthContext.jsx
// ---------------------------------------------------------
// Holds the signed-in user + JWT token in shared React state, so any
// page can read them with useAuth() instead of passing props down
// through every component. Also persists the session to
// localStorage, so refreshing the page doesn't sign you out.
// ---------------------------------------------------------
import { createContext, useContext, useState } from "react";
import { api } from "./api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem("user");
    return raw ? JSON.parse(raw) : null;
  });

  function saveSession(data) {
    // data = { access_token, user } — the shape both signup and login return
    setToken(data.access_token);
    setUser(data.user);
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));
  }

  async function signup(payload) {
    const data = await api.signup(payload);
    saveSession(data);
  }

  async function login(payload) {
    const data = await api.login(payload);
    saveSession(data);
  }

  function logout() {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }

  const value = { token, user, signup, login, logout, isAuthenticated: Boolean(token) };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Lets any component just call useAuth() instead of importing
// useContext + AuthContext everywhere
export function useAuth() {
  return useContext(AuthContext);
}
