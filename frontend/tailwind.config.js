/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: "#f4f7f5",
          raised: "#ffffff",
          muted: "#e8efeb",
        },
        ink: {
          DEFAULT: "#17211d",
          muted: "#5d6d66",
          subtle: "#7c8b85",
        },
        brand: {
          DEFAULT: "#1f6f5b",
          dark: "#17352e",
          accent: "#d7f45d",
        },
        danger: {
          DEFAULT: "#b42318",
          soft: "#ffe1dc",
        },
      },
      borderRadius: {
        panel: "8px",
      },
      boxShadow: {
        panel: "0 18px 45px rgba(23, 53, 46, 0.08)",
      },
    },
  },
  plugins: [],
};
