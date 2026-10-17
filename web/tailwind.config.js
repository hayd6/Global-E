/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        slateBg: "#F8FAFC",
        midnightNavy: "#0F172A",
        emeraldGreen: "#0D9488",
        coralRed: "#E11D48",
        borderSlate: "#E2E8F0",
      },
    },
  },
  plugins: [],
};
