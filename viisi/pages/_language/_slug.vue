<template lang="pug">
  div.distrochooser
    div.top-logo-container
      a(href="/")
        img.top-logo(src='~/assets/logo.png')
    categories(:language="language",v-if="!isSubPageShown")
    div(v-if="!isFinished && !isSubPageShown")
      question(:language="language")
    div(v-if="isFinished && !isSubPageShown")
      result(:language="language")
    div(v-if="isSubPageShown")
      page(:language="language", :content="content")
    div.footer 
      a(href="#", v-on:click.prevent="showSubPage('imprint')")  {{ __i("imprint") }}
      a(href="/privacy", v-on:click.prevent="showSubPage('privacy')") {{ __i("privacy") }}
      a(href="/about", v-on:click.prevent="showSubPage('about')") {{ __i("about") }}
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
      isSubPageShown: false
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
  },
  methods: {
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
    width: 50%;
    margin-left: 25%;
    margin-right: 25%;
  }
  .top-logo-container .top-logo {
    width: 25%;
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
  color: #4484ce;
  text-decoration: none;
  padding-right: 1em;
}
</style>
