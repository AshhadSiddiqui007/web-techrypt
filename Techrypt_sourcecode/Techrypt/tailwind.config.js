/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        five: "#0158A6",
        six: "#121212",
        seven: "#3D550C",
        eight: "#FF56A5",
        nine: "#0a0f14",
        ten: "#CFE5FF",
        primary: "#AEBB1E",
        primaryLight: "#D3DC5A",
        black: "#0f0f0f"
      },
      backgroundImage: {
        'mask1': "url('./src/assets/svgs/mask1.svg')",
        'mask2': "url('./src/assets/svgs/mask2.svg')",
        'mask3': "url('./src/assets/svgs/mask3.svg')",
        'mask4': "url('./src/assets/svgs/mask4.svg')",
        'mask5': "url('./src/assets/svgs/mask5.svg')",
      }
    },
  },
  plugins: [],
}

