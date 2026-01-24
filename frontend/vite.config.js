import { defineConfig } from 'vite';

export default defineConfig({
    build: {
        lib: {
            entry: 'src/main.js',
            formats: ['es'],
        },
        rollupOptions: {
            external: /^lit/,
        },
    },
    server: {
        port: 3000,
        proxy: {
            '/api': {
                target: 'http://localhost:24502',
                changeOrigin: true,
            },
        },
    },
});
