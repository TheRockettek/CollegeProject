/** @type {import('tailwindcss').Config} */

import defaultTheme from "tailwindcss/defaultTheme";
import forms from "@tailwindcss/forms";
import typography from "@tailwindcss/typography";

export default {
  content: ["./src/**/*.vue"],
  safelist: [
    'text-red-500',
    'bg-red-100',
    'text-green-500',
    'bg-green-100',
  ],
  darkMode: "class", // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        sans: ["Balsamiq Sans", ...defaultTheme.fontFamily.sans],
      },
      colors: {
        primary: {
          // 100: "#f0f4ff",
          // 200: "#d9e4ff",
          // 300: "#a6c1ff",
          // 400: "#598bff",
          500: "#3366ff",
          // 600: "#274bdb",
          700: "#1a34b8",
          // 800: "#102694",
          // 900: "#091a7a",
        },
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [forms, typography],
};
