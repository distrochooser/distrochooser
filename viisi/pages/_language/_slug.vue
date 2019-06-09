<template lang="pug">
  div.distrochooser
    div.top-logo-container
      a(href="/")
        img.top-logo(src='~/assets/logo.min.svg')
    div.spin-parent(v-if="isLoading" )
      span {{ __i("loading") }}
      div.spinner
        div.rect1
        div.rect2
        div.rect3
        div.rect4
        div.rect5
    div.spin-parent(v-if="$store.state.isSubmitted" )
      h1 {{ __i("result-submitted-hint") }}
    categories(:language="language",v-if="!isLoading && !isSubPageShown")
    div(v-if="!isLoading && !isFinished && !isSubPageShown && !$store.state.isSubmitted")
      question(:language="language")
    div(v-if="!isLoading && isFinished && !isSubPageShown")
      result(:language="language")
    div(v-if="!isLoading && isSubPageShown")
      page(:language="language", :content="content")

    div.footer 
      a(href="#", v-on:click.prevent="showSubPage('imprint')")  {{ __i("imprint") }}
      a(href="/privacy", v-on:click.prevent="showSubPage('privacy')") {{ __i("privacy") }}
      a(href="/about", v-on:click.prevent="showSubPage('about')") {{ __i("about") }}
      a(href="https://chmr.eu") {{ __i("vendor-text") }}
    
    div.languages
      select
        option(v-for="(locale, locale_key) in $store.state.locales", :key="locale_key", v-on:click="switchLanguage(locale)") {{ locale }}
       
</template>
<script>
import categories from '~/components/categories'
import question from '~/components/question'
import result from '~/components/result'
import i18n from '~/mixins/i18n'
import page from '~/components/page'
export default {
  components: {
    categories,
    question,
    result,
    page
  },
  mixins: [i18n],
  data: function() {
    return {
      language: 'en',
      content: 'about', //about page content
      isSubPageShown: false,
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
    },
    showSubPage: function(what) {
      this.content = what
      this.isSubPageShown = true
    },
    hideSubPage: function() {
      this.content = 'about'
      this.isSubPageShown = false
    }
  }
}
</script>
<style lang="scss">
@import '~/scss/variables.scss';
@import '~/node_modules/spinkit/scss/spinners/3-wave.scss';
@import '~/node_modules/flag-icon-css/css/flag-icon.min.css';
body {
  background: $background;
}
@media only screen and (max-width: $mobileWidth) {
  .distrochooser {
    width: 100%;
    margin-left: 0px;
    margin-right: 0px;
  }
  .top-logo-container .top-logo {
    width: 50%;
  }
}
@media only screen and (min-width: $mobileWidth) {
  .distrochooser {
    width: 60%;
    margin-left: 20%;
    margin-right: 20%;
    margin-top: 2em;
  }
  .top-logo-container .top-logo {
    width: 25%;
    margin-bottom: 2em;
  }
}
.top-logo-container {
  text-align: center;
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
</style>
