/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,html}", // Ajusta esta ruta según la estructura de tu proyecto
  ],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
}
