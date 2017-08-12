let locales = ['de', 'en']
let descriptions = {
  'de': 'Der Distrochooser hilft, im Dschungel der Linux-Distributionen die persönlich passende Distribution zu finden.',
  'en': 'The distrochooser helps you to find the suitable Distribution for you!'
}

module.exports = {
  /*
  ** Headers of the page
  */
  globals: {
    i18n: null,
    distrochooser: null,
    questions: null,
    backend: 'http://127.0.0.1:8181/',
    lang: locales[0],
    distros: [],
    useragent: null,
    referrer: null,
    dnt: false,
    visitor: -1,
    test: -1,
    locales: locales,
    descriptions: descriptions,
    description: null,
    mainInstance: null,
    preloadInfos: null
  },
  head: {
    title: 'Distrochooser',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        name: 'keywords',
        content: 'Linux, Distrochooser, Linux Chooser, Linux Distribution Chooser, Linux Auswahlhilfe, Linux Auswahl, Alternative to Windows, Linux Comparison, Linux Vergleich, Vergleich, Auswahlhilfe, Alternative zu Windows'
      },
      {
        name: 'theme-color',
        content: '#158cba'
      },
      {
        property: 'og:type',
        content: 'website'
      },
      {
        property: 'og:title',
        content: 'Distrochooser'
      },
      {
        property: 'og:url',
        content: 'https://distrochooser.de'
      },
      {
        property: 'og:image',
        content: 'https://distrochooser.de/assets/tux.png'
      },
      {
        property: 'og:image:type',
        content: 'image/png'
      },
      {
        property: 'og:image:width',
        content: '500'
      },
      {
        property: 'og:image:height',
        content: '253'
      },
      {
        name: 'twitter:card',
        content: 'summary'
      },
      {
        name: 'twitter:site',
        content: '@distrochooser'
      },
      {
        name: 'twitter:title',
        content: 'Distrochooser'
      },
      {
        name: 'twitter:image',
        content: 'https://distrochooser.de/assets/tux.png'
      },
      {
        name: 'google-site-verification',
        content: 'nqtoKAtXX7xTNyddaEGkkYtgpc0pc0b-wigel0Acy5c'
      },
      {
        name: 'msvalidate.01',
        content: '8165DC81CC6E5D6805201B58C5596403'
      },
      {
        name: 'generator',
        content: 'LDC 2018'
      }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        'rel': 'stylesheet',
        'href': '/spectre-exp.min.css'
      },
      {
        'rel': 'stylesheet',
        'href': '/spectre.min.css'
      },
      {
        'rel': 'stylesheet',
        'href': '/spectre-icons.min.css'
      }
    ],
    script: [
      { src: 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#3B8070' },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** Run ESLINT on save
    */
    extend (config, ctx) {
      if (ctx.isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    }
  }
}
