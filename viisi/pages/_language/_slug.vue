<template lang="pug">
  div.distrochooser
    div.top-logo-container
      a(href="/")
        img.top-logo(src='/logo.min.svg')
    div.spin-parent(v-if="isLoading" )
      span {{ __i("loading") }}
      div.spinner
        div.rect1(style="background-color: black")
        div.rect2(style="background-color: #e4ae4c")
        div.rect3(style="background-color: #1c105a")
        div.rect4(style="background-color: #ebeef3; border-color: black") 
        div.rect5(style="background-color: #39BA95")    
    div.calculation-loading(v-if="$store.state.isSubmitted && $store.state.sessionStatus !== null") 
      div.spinner
        div.rect1(style="background-color: black")
        div.rect2(style="background-color: #e4ae4c")
        div.rect3(style="background-color: #1c105a")
        div.rect4(style="background-color: #ebeef3; border-color: black") 
        div.rect5(style="background-color: #39BA95")  
      h1.calculation-header {{ __i("searching-criteria") }}
      div.calculation-text {{ $store.state.sessionStatus.done }} {{ __i("checked-criteria-count") }}
    categories(:language="language",v-if="!isLoading && !$store.state.isSubmitted")
    div(v-if="!isLoading && !isFinished && !$store.state.isSubmitted")
      question(:language="language")
    div(v-if="!isLoading && isFinished&& !$store.state.isSubmitted")
      result(:language="language")
    div.footer(v-if="!isLoading")
      a(target="_blank", :href="'/info/imprint/'+ language" )  {{ __i("imprint") }}
      a(target="_blank", :href="'/info/privacy/'+ language" ) {{ __i("privacy") }}
      a(target="_blank", :href="'/info/about/'+ language" ) {{ __i("about") }}
      a(target="_blank", href="https://chmr.eu") {{ __i("vendor-text") }}
    
    div.languages(v-if="!isLoading")
      select
        option(v-for="(locale, locale_key) in $store.state.locales", :key="locale_key", v-on:click="switchLanguage(locale)") {{ __i('language') }}: {{ locale }}
       
</template>
<script>
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
    }
  },
  async mounted() {
    const _t = this
    await this.$store.dispatch('getLocales')
    var lang =
      typeof this.$route.params.language !== 'undefined' &&
      this.$store.state.locales.indexOf(this.$route.params.language) !== -1
        ? this.$route.params.language
        : 'en'
    var testSlug =
      typeof this.$route.params.slug !== 'undefined'
        ? this.$route.params.slug
        : null
    _t.language = lang
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
        language: _t.language
      }
    })
    this.isLoading = false
  },
  methods: {
    switchLanguage: function(locale) {
      //TODO: Implement proper method with reloading the language data on the fly
      window.location.href = '/' + locale
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
          content: '/logo.min.svg'
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
@import '~/node_modules/@fortawesome/fontawesome-free/css/all.min.css';
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
.fa-facebook {
  color: #3b5998;
}
.fa-twitter {
  color: #1da1f2;
}
.footer {
  position: fixed;
  bottom: 0px;
  padding-bottom: 1em;
  text-align: left;
  width: 100%;
  left: 0px;
  padding-left: 1em;
}
.footer a {
  color: $linkColor;
  text-decoration: none;
  padding-right: 1em;
}
// loader
.spinner {
  margin: 100px auto;
  width: 200px;
  height: 14em;
  text-align: center;
  font-size: 10px;
}

.spinner > div {
  background-color: $spinColor;
  height: 100%;
  width: 10px;
  display: inline-block;

  -webkit-animation: sk-stretchdelay 1.2s infinite ease-in-out;
  animation: sk-stretchdelay 1.2s infinite ease-in-out;
  margin: 1em;
}

.spinner .rect2 {
  -webkit-animation-delay: -1.1s;
  animation-delay: -1.1s;
}

.spinner .rect3 {
  -webkit-animation-delay: -1s;
  animation-delay: -1s;
}

.spinner .rect4 {
  -webkit-animation-delay: -0.9s;
  animation-delay: -0.9s;
}

.spinner .rect5 {
  -webkit-animation-delay: -0.8s;
  animation-delay: -0.8s;
}

@-webkit-keyframes sk-stretchdelay {
  0%,
  40%,
  100% {
    -webkit-transform: scaleY(0.4);
  }
  20% {
    -webkit-transform: scaleY(1);
  }
}

@keyframes sk-stretchdelay {
  0%,
  40%,
  100% {
    transform: scaleY(0.4);
    -webkit-transform: scaleY(0.4);
  }
  20% {
    transform: scaleY(1);
    -webkit-transform: scaleY(1);
  }
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
.language select {
  position: absolute;
  bottom: 1em;
}
select {
  padding: 5px 5px 5px 5px;
  font-size: 16px;
  border: 1px solid #1c105a;
  height: 34px;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-color: #1c105a;
  color: white;
  border-radius: 4px;
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
div.calculation-text {
  padding-top: 2em;
}
h1.calculation-header {
  padding-top: 1em;
}
</style>
