// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: [
    '@pinia/nuxt'
  ],
  css: ["bootstrap/dist/css/bootstrap.min.css", "flag-icons/css/flag-icons.min.css"]
})
