<template lang="pug">
  div.distrochooser
    div.top-logo-container
      a(href="/")
        img.top-logo(src='/logo.min.svg')
    div.calculation-loading(v-if="isLoading || $store.state.isSubmitted") 
      div.spinner
    categories(:language="language",v-if="!isLoading && !$store.state.isSubmitted")
    div(v-if="!isLoading && !isFinished && !$store.state.isSubmitted")
      question(:language="language")
    div(v-if="!isLoading && isFinished&& !$store.state.isSubmitted")
      result(:language="language")
    div.footer(v-if="!isLoading")
      a(target="_blank", :href="'/info/imprint/'+ infoPageLanguage" )  {{ __i("imprint") }}
      a(target="_blank", :href="'/info/privacy/'+ infoPageLanguage" ) {{ __i("privacy") }}
      a(target="_blank", :href="'/info/about/'+ infoPageLanguage" ) {{ __i("about") }}
      a(target="_blank", href="https://chmr.eu") {{ __i("vendor-text") }}
    
    div.languages(v-if="!isLoading")
      span(v-for="(locale, locale_key) in $store.state.locales", :key="locale_key", v-on:click="switchLanguage(locale)")
        i.flag-icon(:class="'flag-icon-'+locale", v-if="locale !== 'en'")
   
</template>
<script>
import '@uiw/icons/fonts/w-icon.css'
import categories from '~/components/categories'
import question from '~/components/question'
import result from '~/components/result'
import i18n from '~/mixins/i18n'
export default {
  components: {
    categories,
    question,
    result
  },
  mixins: [i18n],
  data: function() {
    return {
      language: 'en',
      isLoading: true
    }
  },
  computed: {
    isFinished: function() {
      return this.$store.state.result !== null
    },
    infoPageLanguage: function() {
      // as the info pages are only available in de and en
      return ['de', 'en'].indexOf(this.language) !== -1 ? this.language : 'en'
    }
  },
  async mounted() {
    this.prepareLanguageData()
    var testSlug =
      typeof this.$route.params.slug !== 'undefined'
        ? this.$route.params.slug
        : null

    const _t = this
    if (testSlug !== null) {
      await this.$store.dispatch('getOldAnswers', {
        params: {
          slug: testSlug
        }
      })
      this.$store.commit('setOldTestData')
    }
    await this.$store.dispatch('startTest', {
      params: {
        language: _t.language,
        refLinkEncoded: document.referrer ? btoa(document.referrer) : '-'
      }
    })
    this.isLoading = false
  },
  methods: {
    prepareLanguageData: function() {
      if (typeof this.$route.params.language === 'undefined') {
        // only apply the browser language if no language flag is set
        var browserLanguage = window.navigator.language.toLowerCase()
        if (this.$store.state.locales.indexOf(browserLanguage) !== -1) {
          this.language = browserLanguage
        }
      } else {
        var lang =
          typeof this.$route.params.language !== 'undefined' &&
          this.$store.state.locales.indexOf(this.$route.params.language) !== -1
            ? this.$route.params.language
            : 'en'
        this.language = lang
      }
    },
    switchLanguage: async function(locale) {
      this.language = locale
      await this.$store.dispatch('switchLanguage', {
        params: {
          language: this.language
        }
      })
      console.log(this.$store.state.isSubmitted)
      // resubmit result to get translated values (if needed)
      if (this.isFinished) {
        this.$store.dispatch('submitAnswers', {
          params: {
            token: this.$store.state.token,
            language: this.language,
            method: this.$store.state.method
          },
          data: {
            answers: this.$store.state.givenAnswers
          }
        })
      }
    }
  },
  head: function() {
    return {
      titleTemplate: 'Distrochooser',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          hid: 'description',
          name: 'description',
          content: this.welcomeText(this.language)
        },
        {
          name: 'keywords',
          content:
            'Linux, Distrochooser, Linux Chooser, Linux Distribution Chooser, Linux Auswahlhilfe, Linux Auswahl, Alternative to Windows, Linux Comparison, Linux Vergleich, Vergleich, Auswahlhilfe, Alternative zu Windows'
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
          content: this.$store.state.rootUrl + 'logo.min.svg'
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
          content: this.$store.state.rootUrl + '/logo.min.svg'
        },
        {
          name: 'generator',
          content: 'LDC 2019'
        }
      ]
    }
  }
}
</script>
<style lang="scss">
@import '~/scss/variables.scss';
@import '~/node_modules/spinkit/scss/spinners/3-wave.scss';
@import '~/node_modules/flag-icon-css/css/flag-icon.min.css';
/* roboto-slab-regular - latin */
@font-face {
  font-family: 'Roboto Slab';
  font-style: normal;
  font-weight: 400;
  src: url('/fonts/Roboto/roboto-slab-v8-latin-regular.eot'); /* IE9 Compat Modes */
  src: local('Roboto Slab Regular'), local('RobotoSlab-Regular'),
    url('/fonts/Roboto/roboto-slab-v8-latin-regular.eot?#iefix')
      format('embedded-opentype'),
    /* IE6-IE8 */ url('/fonts/Roboto/roboto-slab-v8-latin-regular.woff2')
      format('woff2'),
    /* Super Modern Browsers */
      url('/fonts/Roboto/roboto-slab-v8-latin-regular.woff') format('woff'),
    /* Modern Browsers */ url('/fonts/Roboto/roboto-slab-v8-latin-regular.ttf')
      format('truetype'),
    /* Safari, Android, iOS */
      url('/fonts/Roboto/roboto-slab-v8-latin-regular.svg#RobotoSlab')
      format('svg'); /* Legacy iOS */
}
/* archivo-regular - latin */
@font-face {
  font-family: 'Archivo';
  font-style: normal;
  font-weight: 400;
  src: url('/fonts/Archivo/archivo-v4-latin-regular.eot'); /* IE9 Compat Modes */
  src: local('Archivo Regular'), local('Archivo-Regular'),
    url('/fonts/Archivo/archivo-v4-latin-regular.eot?#iefix')
      format('embedded-opentype'),
    /* IE6-IE8 */ url('/fonts/Archivo/archivo-v4-latin-regular.woff2')
      format('woff2'),
    /* Super Modern Browsers */
      url('/fonts/Archivo/archivo-v4-latin-regular.woff') format('woff'),
    /* Modern Browsers */ url('/fonts/Archivo/archivo-v4-latin-regular.ttf')
      format('truetype'),
    /* Safari, Android, iOS */
      url('/fonts/Archivo/archivo-v4-latin-regular.svg#Archivo') format('svg'); /* Legacy iOS */
}
/* open-sans-regular - latin */
@font-face {
  font-family: 'Open Sans';
  font-style: normal;
  font-weight: 400;
  src: url('/fonts/OpenSans/open-sans-v16-latin-regular.eot'); /* IE9 Compat Modes */
  src: local('Open Sans Regular'), local('OpenSans-Regular'),
    url('/fonts/OpenSans/open-sans-v16-latin-regular.eot?#iefix')
      format('embedded-opentype'),
    /* IE6-IE8 */ url('/fonts/OpenSans/open-sans-v16-latin-regular.woff2')
      format('woff2'),
    /* Super Modern Browsers */
      url('/fonts/OpenSans/open-sans-v16-latin-regular.woff') format('woff'),
    /* Modern Browsers */ url('/fonts/OpenSans/open-sans-v16-latin-regular.ttf')
      format('truetype'),
    /* Safari, Android, iOS */
      url('/fonts/OpenSans/open-sans-v16-latin-regular.svg#OpenSans')
      format('svg'); /* Legacy iOS */
}
.footer {
  position: fixed;
  top: 1em;
  padding-bottom: 1em;
  text-align: right;
  right: 0px;
  padding-left: 2em;
  z-index: 0;
}
.footer a {
  color: $linkColor;
  text-decoration: none;
  padding-right: 1em;
  font-size: small;
}
.spin-parent {
  text-align: center;
  margin-top: 3em;
}
.languages {
  position: fixed;
  right: 1em;
  bottom: 1em;
}
.language {
  margin-right: 1em;
}
.flag-icon {
  cursor: pointer;
  font-size: 13pt;
}

/* CAUTION: IE hackery ahead */
select::-ms-expand {
  display: none; /* remove default arrow on ie10 and ie11 */
}

/* target Internet Explorer 9 to undo the custom arrow */
@media screen and (min-width: 0\0) {
  select {
    background: none\9;
    padding: 5px\9;
  }
}
.calculation-loading {
  text-align: center;
  margin-top: 15%;
  font-size: large;
}
.calculation-text {
  padding-top: 2em;
}

.spinner {
  display: inline-block;
  width: 100px;
  height: 100px;
  border: 5px solid lightgray;
  border-radius: 50%;
  border-top-color: $spinColor;
  animation: spin 1s infinite;
  -webkit-animation: spin 1s infinite;
  margin: 100px auto;
  text-align: center;
  font-size: 10px;
}

@keyframes spin {
  to {
    -webkit-transform: rotate(360deg);
  }
}
@-webkit-keyframes spin {
  to {
    -webkit-transform: rotate(360deg);
  }
}
</style>
