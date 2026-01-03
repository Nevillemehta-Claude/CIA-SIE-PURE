/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Signal direction colors (CONSTITUTIONAL: equal visual weight)
        // Saturation and brightness matched across all directions
        signal: {
          bullish: '#22c55e',    // green-500
          bearish: '#ef4444',    // red-500
          neutral: '#6b7280',    // gray-500
        },
        // Freshness status colors
        freshness: {
          current: '#22c55e',    // green-500
          recent: '#eab308',     // yellow-500
          stale: '#f97316',      // orange-500
          unavailable: '#6b7280', // gray-500
        },
        // UI theme colors
        surface: {
          primary: '#0f172a',    // slate-900
          secondary: '#1e293b',  // slate-800
          tertiary: '#334155',   // slate-700
        },
        accent: {
          primary: '#3b82f6',    // blue-500
          secondary: '#8b5cf6',  // violet-500
        },
      },
      fontFamily: {
        sans: ['Geist Mono', 'JetBrains Mono', 'SF Mono', 'ui-monospace', 'monospace'],
        display: ['Bricolage Grotesque', 'Space Grotesk', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

