// ProtectedRoute.jsx
// ---------------------------------------------------------
// Wraps a page that requires sign-in. If nobody's authenticated, it
// redirects to the landing page instead of rendering the page.
// ---------------------------------------------------------
import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

export default function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  return children;
}
