/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        // "Flight ops" palette — deliberately not the default AI-generated
        // cream+terracotta or near-black+neon looks. ink = structure/text,
        // signal = actions, beacon = the one sparing accent for "live" /
        // in-progress states, taxiway/approach = budget status.
        ink: "#12172B",
        paper: "#F5F6F8",
        signal: {
          DEFAULT: "#2F6FED",
          dark: "#1D4FC4",
        },
        beacon: "#F2A93B",
        taxiway: "#1E8E5A",
        approach: "#C4442C",
      },
      fontFamily: {
        display: ['"Space Grotesk"', "sans-serif"],
        sans: ["Inter", "sans-serif"],
        mono: ['"IBM Plex Mono"', "monospace"],
      },
      keyframes: {
        fadeInUp: {
          "0%": { opacity: "0", transform: "translateY(6px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        fadeInUp: "fadeInUp 0.35s ease-out both",
      },
    },
  },
  plugins: [],
}
