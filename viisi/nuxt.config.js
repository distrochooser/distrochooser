const pkg = require('./package')

module.exports = {

  /*
  ** Headers of the page
  */
  head: {
    meta: [{hid: "google-site-verification", name: "google-site-verification", content:"nqtoKAtXX7xTNyddaEGkkYtgpc0pc0b-wigel0Acy5c"}],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/icon.svg' }, {rel: 'canonical', href: 'https://distrochooser.de'}]
  },

  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },

  /*
  ** Global CSS
  */
  css: [],

  /*
  ** Plugins to load before mounting the App
  */
  plugins: [],

  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://github.com/nuxt-community/axios-module#usage
    '@nuxtjs/axios',
    "@nuxtjs/sitemap",
  ],
  /*
  ** Axios module configuration
  */
  axios: {
    // See https://github.com/nuxt-community/axios-module#options
  },
  sitemap: {
    hostname: 'https://distrochooser.de',
    gzip: true,
    exclude: [
      '/info/privacy/*',
      '/info/imprint/*'
    ],
    routes: [
      '/',
      '/de',
      '/en',
      '/es',
      '/fi',
      '/fr',
      '/ch',
      '/he',
      '/it',
      '/nl',
      '/pt-br',
      '/ru',
      '/tr',
      '/vn',
      '/zh-hans',
      '/zh-hant',
      '/info/about/de',
      '/info/about/en',
      '/info/about/es',
      '/info/about/fi',
      '/info/about/fr',
      '/info/about/ch',
      '/info/about/he',
      '/info/about/it',
      '/info/about/nl',
      '/info/about/pt-br',
      '/info/about/ru',
      '/info/about/tr',
      '/info/about/vn',
      '/info/about/zh-hans',
      '/info/about/zh-hant',
    ]
  }
}
