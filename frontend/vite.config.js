import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Todas as requisições para /users serão encaminhadas para o backend
      '/users': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/auth': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/products': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/orders': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/restaurants': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
