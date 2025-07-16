/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#2563EB",
        primaryDark: "#1E40AF",
        accent: "#F59E0B",
        bgLight: "#F9FAFB",
        bgDark: "#0F172A",
        text: "#1F2937",
        muted: "#9CA3AF",
        success: "#10B981",
        warning: "#FACC15",
        danger: "#EF4444"
      },
    },
  },
  plugins: [],
}
