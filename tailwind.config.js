/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        night: '#050816',
        panel: '#0f1738',
        accent: '#f5b700',
        accentBlue: '#29b6f6',
        played: '#2b325f'
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(41, 182, 246, 0.2), 0 10px 45px rgba(0, 0, 0, 0.45)',
        accent: '0 0 28px rgba(245, 183, 0, 0.35)'
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        pulseSoft: {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.02)' }
        }
      },
      animation: {
        fadeInUp: 'fadeInUp 350ms ease-out',
        pulseSoft: 'pulseSoft 2.4s ease-in-out infinite'
      }
    }
  },
  plugins: []
};
