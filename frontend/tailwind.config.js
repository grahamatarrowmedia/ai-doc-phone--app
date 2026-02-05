/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#1a1a1a',
        'bg-secondary': '#242424',
        'bg-sidebar': '#1e1e1e',
        'bg-elevated': '#2a2a2a',
        'bg-input': '#333333',
        'accent-red': '#e53e3e',
        'accent-red-dark': '#c53030',
        'accent-blue': '#4299e1',
        'accent-green': '#48bb78',
        'accent-orange': '#ed8936',
        'text-primary': '#f5f5f0',
        'text-secondary': '#a0a0a0',
        'text-tertiary': '#666666',
        'border-subtle': '#333333',
        'border-medium': '#444444',
        'bg-detail': '#f5f0e8',
        'text-detail': '#1a1a1a',
        'text-detail-muted': '#666666',
      },
      fontFamily: {
        'heading': ['Space Grotesk', 'sans-serif'],
        'body': ['Crimson Pro', 'serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      }
    },
  },
  plugins: [],
}
