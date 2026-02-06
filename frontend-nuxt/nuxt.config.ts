// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: false, // Disable Server Side Rendering (makes it a purely static SPA)
  runtimeConfig: {
    public: {
      apiBase: 'https://qr-backend.onrender.com' // PASTE YOUR BACKEND URL HERE
    }
  }
})
