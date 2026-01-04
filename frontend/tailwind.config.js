/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Surface colors
        'surface-primary': '#0f172a',
        'surface-secondary': '#1e293b',
        'surface-tertiary': '#334155',
        // Accent
        'accent-primary': '#3b82f6',
        'accent-secondary': '#8b5cf6',
        // Signal colors (EQUAL visual weight)
        'signal-bullish': '#22c55e',
        'signal-bearish': '#ef4444',
        'signal-neutral': '#94a3b8',
        // Freshness colors (descriptive only)
        'freshness-current': '#22c55e',
        'freshness-recent': '#f59e0b',
        'freshness-stale': '#ef4444',
        'freshness-unavailable': '#64748b',
      },
      fontFamily: {
        display: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}

