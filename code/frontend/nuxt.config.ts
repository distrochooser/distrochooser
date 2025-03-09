import { defineNuxtConfig } from "nuxt/config";
import { deprecations } from "sass";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: [
    '@pinia/nuxt',
    '@nuxt/icon',
    '@nuxtjs/robots'
  ],
  css: ["./style/main.scss", "flag-icons/css/flag-icons.min.css"],
  runtimeConfig: {
    public: {
      basePath: process.env.NUXT_PUBLIC_BASE_PATH || "http://localhost:8000"
    }
  },
  robots: {
    disallow: ['/pages/contact', '/pages/privacy'],
  },
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          silenceDeprecations: [
            "import" // FIXME: This mutes the deprecation. Requires research
          ],
          quietDeps: true,
          api: 'modern-compiler', // or 'modern'
        },
      },
    }
  }
})
