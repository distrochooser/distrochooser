<template lang="pug">
  div.distrochooser(v-bind:class="{ 'visually-impaired-mode': $store.state.visuallyImpairedMode, 'rtl': isRTL }")
    div.beta-banner(v-if="isBeta") Development version: For testing purposes only. For the online version, use  
      a(href="https://distrochooser.de") distrochooser.de
    div.top-logo-container(aria-role="banner",v-if="!$store.state.visuallyImpairedMode")
      a(href="/")
        img.top-logo(src='/logo.min.svg', alt="Distrochooser.de Logo")
    div.calculation-loading(v-if="isLoading || $store.state.isSubmitted") 
      div.spinner(v-if="!$store.state.visuallyImpairedMode")
      div.spinner-text(v-else) {{ __i("loading") }}
    categories(:language="language",v-if="!isLoading && !$store.state.isSubmitted")
    div(v-if="!isLoading && !isFinished && !$store.state.isSubmitted")
      question(:language="language")
    div(v-if="!isLoading && isFinished&& !$store.state.isSubmitted")
      result(:language="language")
    div.language-select(v-if="!$store.state.isStarted")
      label(for="language") {{ __i("language") }}
      select(v-if="!isLoading", v-model="language",id="language",:title="__i('language')")
        option(v-for="(locale, locale_key) in $store.state.locales", :key="locale_key", v-bind:value="locale_key") {{locale}}
    footernav(v-if="!isLoading && this.$store.state.result === null",:language="infoPageLanguage")
</template>
<script>
import viisiConfig from '~/distrochooser.json'
import '@uiw/icons/fonts/w-icon.css'
import categories from '~/components/categories'
import question from '~/components/question'
import result from '~/components/result'
import footernav from '~/components/footer'
import i18n from '~/mixins/i18n'
export default {
  components: {
    categories,
    question,
    result,
    footernav
  },
  mixins: [i18n],
  data: function() {
    return {
      language: 'en',
      isLoading: true,
      languageChanged: false
    }
  },
  computed: {
    isBeta: function() {
      return viisiConfig.frontend.frontendUrl.indexOf("localhost") !== -1 || viisiConfig.frontend.frontendUrl.indexOf("beta.distrochooser.de")  !== -1
    },
    isFinished: function() {
      return this.$store.state.result !== null
    },
    infoPageLanguage: function() {
      // as the info pages are only available in de and en
      return ['de', 'en'].indexOf(this.language) !== -1 ? this.language : 'en'
    },
    isRTL() {
      return ['he'].indexOf(this.language) !== -1
    }
  },
  watch: {
    language: async function(val) {    
      this.languageChanged = true
      await this.switchLanguage(val)
    }
  },
  async mounted() {
    if (this.$route.fullPath.toLowerCase().indexOf('vim=true') !== -1) {
      this.$store.dispatch('setVisuallyImpairedMode', true)
    }
    const _t = this
    await this.$store.dispatch('startTest', {
      params: {
        language: _t.language
      },
      data: {
        referrer: document.referrer ? document.referrer : null
      }
    })
    await this.setOldDataIfNeeded();
    this.isLoading = false
  },
  methods: {
    setOldDataIfNeeded: async function() {

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
    },
    prepareLanguageData: function() {
      if (this.languageChanged) {
        /* If there was already a language change -> don't do anything. /*/
        return;
      }
      var allLocales = Object.keys(this.$store.state.locales)
      if (typeof this.$route.params.language === 'undefined') {
        if (typeof window === 'undefined') {
          return "en"; /* No browser detectable (SSR) */
        }
        // only apply the browser language if no language flag is set
        var browserLanguage = window.navigator.language.toLowerCase()
        if (allLocales.indexOf(browserLanguage) !== -1) {
          this.language = browserLanguage
        }
      } else {
        var lang =
          typeof this.$route.params.language !== 'undefined' &&
          allLocales.indexOf(this.$route.params.language) !== -1
            ? this.$route.params.language
            : 'en'
        this.language = lang
      }
    },
    switchLanguage: async function(locale) {
      this.language = locale
      var slug = typeof this.$route.params.slug !== 'undefined' ? "/" + this.$route.params.slug : "" /* Also push the old result, if there is any */
      this.$router.push("/" + this.language + slug)
      await this.$store.dispatch('switchLanguage', {
        params: {
          language: this.language
        }
      })

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
    this.prepareLanguageData()
    var description_meta = {
      "de": "Die Linux Auswahlhilfe hilft Anfängern und Umsteigern in der Menge von Linux-Distributionen die passende Linux-Distribution zu finden.",
      "en": "The Distrochooser helps you to find the suitable Linux distribution based on your needs!",
      "es": "El Distrochooser le ayuda a encontrar la distribución de Linux adecuada según sus necesidades.",
      "fi": "Distrochooser auttaa sinua löytämään sopivan Linux-jakelun tarpeidesi mukaan!",
      "fr": "Le Distrochooser vous aide à trouver la distribution Linux appropriée en fonction de vos besoins !",
      "gsw": "Die Linux Auswahlhilfe hilft Anfängern und Umsteigern in der Menge von Linux-Distributionen die passende Linux-Distribution zu finden.",
      "he": "ה-Distrochooser עוזר לך למצוא את הפצת הלינוקס המתאימה בהתבסס על הצרכים שלך!",
      "it": "Il Distrochooser vi aiuta a trovare la distribuzione Linux più adatta alle vostre esigenze!",
      "nl": "De Distrochooser helpt u de geschikte Linux-distributie te vinden op basis van uw behoeften!",
      "pt-br": "O Distrochooser ajuda você a encontrar a distribuição Linux adequada com base em suas necessidades!",
      "ru": "Distrochooser поможет вам найти подходящий дистрибутив Linux в соответствии с вашими потребностями!",
      "tr": "Distrochooser, ihtiyaçlarınıza göre uygun Linux dağıtımını bulmanıza yardımcı olur!",
      "vn": "Distrochooser giúp bạn tìm bản phân phối Linux phù hợp dựa trên nhu cầu của bạn!",
      "id": "Distrochooser membantu Anda menemukan distribusi Linux yang sesuai dengan kebutuhan Anda!",
      "zh-hans":"Distrochooser 可帮助您根据需要找到合适的 Linux 发行版！",
      "zh-hant":"Distrochooser可以帮助你根据你的需要找到合适的Linux发行版"
    }
    var result = {
      titleTemplate: 'Distrochooser',
      htmlAttrs: {
        lang: this.language
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'keywords',
          content:
            'Linux, Distrochooser, Linux Chooser, Linux Distribution Chooser, Linux Auswahlhilfe, Linux Auswahl, Alternative to Windows, Linux Comparison, Linux Vergleich, Vergleich, Auswahlhilfe, Alternative zu Windows'
        },
        {
          name: 'description',
          content: description_meta[this.language]
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
          content: this.$store.state.rootUrl + 'logo.png'
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
          name: 'twitter:description',
          content: description_meta[this.language]
        },
        {
          name: 'twitter:image',
          content: this.$store.state.rootUrl + '/logo.png'
        },
        {
          name: 'generator',
          content: 'LDC 2019'
        }
      ]
    }
    if (this.isBeta) {
      result["meta"].push({
        "name": "robots",
        "content": "noindex"
      })
    }
    return result
  }
}
</script>
<style lang="scss">
@import '~/scss/variables.scss';
@import '~/node_modules/spinkit/spinkit.min.css';
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
.beta-banner {
  position: fixed;
  bottom: 0px;
  left: 0px;
  text-align: center;
  width: 100%;
  padding: 1em;
  background: red;
  z-index: -10000000;
  color: white;
  a {
    color: white;
    font-weight: bold;
  }
}
.spin-parent {
  text-align: center;
  margin-top: 3em;
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

.rtl {
  direction: rtl;

  .question {
    .question-content {
      padding-right: 1em;
    }
    .answer-remark {
      left: unset !important;
      right: 5%;
    }
  }
  .welcome-text {
    i.w-icon-right-square-o::before {
      content: '\ea64' !important;
    }

    .w-icon-d-arrow-right::before {
      content: '\ea30';
    }
  }
  /* Icon margins */
  .breadcrumb-horizontal {
    ul li i {
      margin-left: 0.5em;
    }

    .w-icon-login::before {
      content: '\ea62';
    }

    .floating-button {
      margin-left: unset;
      margin-right: 11px;
      a i {
        margin-left: 0.5em;
      }
    }
  }

  .floating-button {
    i.w-icon-right-square-o::before {
      content: '\ea64' !important;
    }
  }

  .welcome-text {
    div i {
      margin-left: 0.5em;
    }
  }

  .footer a i.w-icon-github {
    margin-left: 0.5em;
    margin-right: unset;
  }

  /* result page */

  .remarks .remarks-header {
    margin-right: -1.5%;
    text-align: right;
  }

  .distribution .meta .actions {
    padding-right: 0em;
    .vote-actions {
      margin-right: -0.5em;
    }
  }

  .distribution .meta .url {
    text-align: left;
    padding-left: 1em;
  }

  .distribution {
    .description {
      padding-right: 1em;

      .reason-list div div i,
      .blocking-list div div i {
        margin-left: 0.5em;
        margin-right: 0px;
      }
    }
  }
}
.visually-impaired-mode {
  font-size: x-large;
  margin-top: 2em;
  .distribution {
      .reason-list {
        .w-icon-plus {
          font-weight: bold;
          color: #034603 !important;
        }
      }
      #negative-list {
        .w-icon-minus {
          font-weight: bold;
          color: #b00202 !important;
        }
      }
  }
  .question .question-content .welcome-text {
    font-size: x-large;
    i {
      display: none;
    }
  }
  .warning-icon {
    display: none;
  }
  .answers .answer input {
    width: 30px;
    height: 30px;
  }
  button.step {
    font-size: x-large;
  }
  .question-text {
    font-size: larger;
  }
  .answer-remark {
    font-size: x-large;
  }
  .important-visually-impaired {
    margin-left: 1em;
  }
  .hide-reasons {
    display: none;
  }
  .footer {
    width: auto;
    right: 1em !important;
    text-align: left !important;
    position: fixed !important;
    bottom: 1em;
    color: darkblue !important;
  }
  .footer a {
    display: block;
    margin-bottom: 0.5em;
  }
  .footer a,
  .footer select {
    font-size: x-large !important;
  }
  .footer i {
    display: none;
  }
  .breadcrumb-horizontal {
    top: 0px;
    ul li i {
      color: black !important;
      font-size: 1.5em;
    }
    ul li a{

      span {
        color: black !important;
        font-size: 1.5em;

        &.active {
          font-weight: bold;
          border: 3px solid black;
        }
      }
    }
    ul li a.recommendation-link {
      color: black !important;
      font-size: 1.5em;
    }
  }
}

.language-select {
  width: fit-content;
  right: 1em;
  position: fixed;
  top: 0px;
  margin-top: 0.5em;

  label {
    display: block;
    text-align: left;
    margin-right: 1.5em;
  }
}
</style>
