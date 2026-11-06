import { defineNuxtConfig } from "nuxt/config";
import type { MetaTags } from "./sdk";

const apiBasePath = () => process.env.NUXT_PUBLIC_BASE_PATH || "http://localhost:8000"

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  site: {
    name: "Distrochooser",
  },
  modules: [
    '@nuxtjs/sitemap',
    '@pinia/nuxt',
    '@nuxt/icon',
  ],
  icon: {
    provider: 'none',
    clientBundle: {
      scan: true,
      icons: [
        "ion:arrow-forward-circle-outline",
        "ion:git-branch",
        "ion:stats-chart",
        "ion:monitor",
        "ion:ios-list",
        "ion:extension-puzzle",
        "ion:md-help-circle",
        "ion:logo-windows",
        "ion:ios-cart",
        "ion:checkbox-sharp",
        "ion:md-globe",
        "ion:shield-checkmark-sharp",
        "ion:settings-outline",
        "ion:md-cloud-download",
        "ion:ios-settings-strong",
        "ion:ios-arrow-dropright-circle"]
    },
  },
  sitemap: {
    urls: async () => {
      const response = await fetch(apiBasePath() + "/rest/metatags?lang=en")
      const metaTags = await response.json()
      const languages: string[] = metaTags.languages.sort()

      let urls = []
      urls.push({
        "loc": metaTags.base_url + "/",
        "lastmod": new Date().toISOString(),
        "alternatives": languages.map(l => {
          return {
            "hreflang": l,
            "href": metaTags.base_url + "/" + l
          }
        })
      })
      urls.push({
        "loc": metaTags.base_url + "/pages/about/en",
        "lastmod": new Date().toISOString(),
        "alternatives": languages.filter(l => l != "en").map(l => {
          return {
            "hreflang": l,
            "href": metaTags.base_url + "/pages/about/" + l
          }
        })
      })
      return urls
    }
  },
  app: {
    loadingIndicator: true
  },
  css: ["~/style/main.scss", "flag-icons/css/flag-icons.min.css"],
  runtimeConfig: {
    public: {
      basePath: apiBasePath()
    }
  },
  vite: {
    optimizeDeps: {
      include: [
        '@vue/devtools-core',
        '@vue/devtools-kit',
        'bootstrap/dist/js/bootstrap.bundle', // CJS
      ]
    },
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