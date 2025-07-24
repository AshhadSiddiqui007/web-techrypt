/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  safelist: [
    'group',
    'group-hover',
    'group-hover/nested',
    'group-hover:opacity-100',
    'group-hover:pointer-events-auto'
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
        primary: "#C4D322",
        primaryLight: "#D3DC5A",
        black: "#0f0f0f"
      },
      backgroundImage: {
        'mask1': "url('./src/assets/svgs/mask1.svg')",
        'mask2': "url('./src/assets/svgs/mask2.svg')",
        'mask3': "url('./src/assets/svgs/mask3.svg')",
        'mask4': "url('./src/assets/svgs/mask4.svg')",
        'mask5': "url('./src/assets/svgs/mask5.svg')",
      },
      screens: {
        'xs': '320px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
        'mobile': {'max': '767px'},
        'tablet': {'min': '768px', 'max': '1023px'},
        'desktop': {'min': '1024px'},
      },
      spacing: {
        'safe-top': 'env(safe-area-inset-top)',
        'safe-bottom': 'env(safe-area-inset-bottom)',
        'safe-left': 'env(safe-area-inset-left)',
        'safe-right': 'env(safe-area-inset-right)',
      },
      fontSize: {
        'responsive-xs': 'clamp(0.75rem, 2vw, 0.875rem)',
        'responsive-sm': 'clamp(0.875rem, 2.5vw, 1rem)',
        'responsive-base': 'clamp(1rem, 3vw, 1.125rem)',
        'responsive-lg': 'clamp(1.125rem, 4vw, 1.25rem)',
        'responsive-xl': 'clamp(1.25rem, 5vw, 1.5rem)',
        'responsive-2xl': 'clamp(1.5rem, 6vw, 2rem)',
        'responsive-3xl': 'clamp(1.875rem, 7vw, 2.5rem)',
        'responsive-4xl': 'clamp(2.25rem, 8vw, 3rem)',
        'responsive-5xl': 'clamp(3rem, 10vw, 4rem)',
      }
    },
  },
  plugins: [],
}

